# Frontend Architecture

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Component Architecture](#component-architecture)
- [State Management](#state-management)
- [Routing](#routing)
- [API Integration](#api-integration)
- [Real-time Features](#real-time-features)
- [UI/UX Features](#uiux-features)
- [Performance Optimization](#performance-optimization)
- [Testing](#testing)
- [Build & Deployment](#build--deployment)
- [Internationalization (i18n)](#internationalization-i18n)
- [Future Enhancements](#future-enhancements)

### Verwandte Dokumente
- [🧩 Frontend-Komponenten](./frontend-components.md) - Komponenten-Bibliothek
- [📊 Frontend State Management](./frontend-state-management.md) - Zustand-Verwaltung
- [🌍 Internationalisierung](./internationalization.md) - i18n-System und Übersetzungen
- [📐 UI-Mockups](./ui-mockups.md) - Design-Entwürfe
- [📘 Benutzerhandbuch](./user-guide.md) - Bedienungsanleitung

## Overview

MailMind's frontend is built with React and TypeScript, providing a modern, responsive interface for email management with real-time updates and AI-powered features.

## Technology Stack

### Core Technologies
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling

### State Management
- **Zustand**: Lightweight state management
- **React Query**: Server state synchronization
- **Context API**: Theme and auth state

### UI Components
- **Headless UI**: Accessible component primitives
- **React Markdown**: Markdown rendering
- **Lucide Icons**: Modern icon set
- **Highlight.js**: Syntax highlighting

## Project Structure

```
src/frontend/
├── src/
│   ├── components/        # Reusable components
│   │   ├── common/        # Generic components
│   │   ├── email/         # Email-specific components
│   │   ├── ai/            # AI feature components
│   │   └── layout/        # Layout components
│   ├── pages/             # Route pages
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API services
│   ├── stores/            # Zustand stores
│   ├── types/             # TypeScript types
│   ├── utils/             # Utility functions
│   └── styles/            # Global styles
├── public/                # Static assets
└── index.html            # Entry HTML
```

## Component Architecture

### Component Hierarchy

```
App
├── Layout
│   ├── Header
│   │   ├── SearchBar
│   │   ├── UserMenu
│   │   └── NotificationBell
│   ├── Sidebar
│   │   ├── Navigation
│   │   ├── FolderList
│   │   └── TagCloud
│   └── MainContent
│       └── <Routes>
├── EmailList
│   ├── EmailFilters
│   ├── EmailItem
│   └── Pagination
├── EmailView
│   ├── EmailHeader
│   ├── EmailBody
│   ├── AttachmentList
│   └── AIInsights
└── ComposeEmail
    ├── RecipientField
    ├── Editor
    └── AIAssistant
```

### Component Design Patterns

#### Smart vs Presentational Components
```tsx
// Smart Component (Container)
const EmailListContainer: React.FC = () => {
  const { emails, loading, error } = useEmails();
  const { filters } = useFilters();
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return <EmailList emails={emails} filters={filters} />;
};

// Presentational Component
interface EmailListProps {
  emails: Email[];
  filters: FilterOptions;
}

const EmailList: React.FC<EmailListProps> = ({ emails, filters }) => {
  return (
    <div className="email-list">
      {emails.map(email => (
        <EmailItem key={email.id} email={email} />
      ))}
    </div>
  );
};
```

#### Custom Hooks Pattern
```tsx
// hooks/useEmails.ts
export const useEmails = (filters?: FilterOptions) => {
  const { data, error, loading, refetch } = useQuery(
    ['emails', filters],
    () => emailService.fetchEmails(filters),
    {
      staleTime: 30000,
      cacheTime: 300000,
    }
  );
  
  return {
    emails: data?.emails || [],
    totalCount: data?.totalCount || 0,
    loading,
    error,
    refetch
  };
};
```

## State Management

### Zustand Store Structure

```tsx
// stores/emailStore.ts
interface EmailStore {
  emails: Email[];
  selectedEmail: Email | null;
  filters: FilterOptions;
  
  // Actions
  setEmails: (emails: Email[]) => void;
  selectEmail: (email: Email) => void;
  updateFilters: (filters: Partial<FilterOptions>) => void;
  deleteEmail: (id: string) => void;
}

export const useEmailStore = create<EmailStore>((set) => ({
  emails: [],
  selectedEmail: null,
  filters: defaultFilters,
  
  setEmails: (emails) => set({ emails }),
  selectEmail: (email) => set({ selectedEmail: email }),
  updateFilters: (filters) => set((state) => ({
    filters: { ...state.filters, ...filters }
  })),
  deleteEmail: (id) => set((state) => ({
    emails: state.emails.filter(e => e.id !== id)
  }))
}));
```

### React Query Integration

```tsx
// services/emailService.ts
export const emailService = {
  fetchEmails: async (filters?: FilterOptions): Promise<EmailResponse> => {
    const response = await api.get('/emails', { params: filters });
    return response.data;
  },
  
  searchEmails: async (query: string): Promise<Email[]> => {
    const response = await api.get('/search', { params: { q: query } });
    return response.data;
  },
  
  sendEmail: async (email: EmailCreate): Promise<Email> => {
    const response = await api.post('/emails', email);
    return response.data;
  }
};
```

## Routing

### Route Configuration

```tsx
// App.tsx
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="inbox" element={<Inbox />} />
          <Route path="email/:id" element={<EmailView />} />
          <Route path="compose" element={<ComposeEmail />} />
          <Route path="search" element={<SearchResults />} />
          <Route path="settings/*" element={<Settings />} />
          <Route path="docs/*" element={<DocViewer />} />
        </Route>
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Protected Routes

```tsx
const ProtectedRoute: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  return <>{children}</>;
};
```

## API Integration

### Axios Configuration

```tsx
// services/api.ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:9000/api',
  timeout: 10000,
});

// Request interceptor for auth
api.interceptors.request.use(
  (config) => {
    const token = authStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await authStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Real-time Features

### WebSocket Integration

```tsx
// hooks/useWebSocket.ts
export const useWebSocket = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:9000/ws');
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setSocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Implement reconnection logic
    };
    
    return () => ws.close();
  }, []);
  
  return socket;
};
```

### Real-time Updates

```tsx
const handleWebSocketMessage = (data: WebSocketMessage) => {
  switch (data.type) {
    case 'NEW_EMAIL':
      queryClient.invalidateQueries(['emails']);
      showNotification('New email received');
      break;
      
    case 'EMAIL_PROCESSED':
      queryClient.setQueryData(['email', data.emailId], data.email);
      break;
      
    case 'AI_SUGGESTION':
      updateAISuggestions(data.suggestions);
      break;
  }
};
```

## UI/UX Features

### Dark Mode Support

```tsx
// contexts/ThemeContext.tsx
export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### Responsive Design

```tsx
// components/EmailList.tsx
const EmailList: React.FC = () => {
  return (
    <div className="flex flex-col lg:flex-row">
      {/* Mobile: Stack vertically, Desktop: Side by side */}
      <div className="w-full lg:w-1/3 xl:w-1/4">
        <EmailListSidebar />
      </div>
      <div className="w-full lg:w-2/3 xl:w-3/4">
        <EmailListContent />
      </div>
    </div>
  );
};
```

### Accessibility

```tsx
// components/common/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  'aria-label'?: string;
  onClick?: () => void;
  children: ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  'aria-label': ariaLabel,
  onClick,
  children
}) => {
  return (
    <button
      className={cn(
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        buttonVariants[variant],
        buttonSizes[size],
        disabled && 'opacity-50 cursor-not-allowed'
      )}
      disabled={disabled}
      aria-label={ariaLabel}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## Performance Optimization

### Code Splitting

```tsx
// Lazy load heavy components
const EmailEditor = lazy(() => import('./components/EmailEditor'));
const AIInsights = lazy(() => import('./components/AIInsights'));
const Settings = lazy(() => import('./pages/Settings'));

// Use with Suspense
<Suspense fallback={<LoadingSpinner />}>
  <EmailEditor />
</Suspense>
```

### Memoization

```tsx
// Memoized component
const EmailItem = memo<EmailItemProps>(({ email, isSelected, onClick }) => {
  return (
    <div 
      className={cn('email-item', isSelected && 'selected')}
      onClick={() => onClick(email.id)}
    >
      <h3>{email.subject}</h3>
      <p>{email.preview}</p>
    </div>
  );
}, (prevProps, nextProps) => {
  return prevProps.email.id === nextProps.email.id &&
         prevProps.isSelected === nextProps.isSelected;
});

// Memoized calculations
const sortedEmails = useMemo(() => {
  return emails.sort((a, b) => b.timestamp - a.timestamp);
}, [emails]);
```

### Virtual Scrolling

```tsx
// components/VirtualEmailList.tsx
import { FixedSizeList } from 'react-window';

const VirtualEmailList: React.FC<{ emails: Email[] }> = ({ emails }) => {
  const Row = ({ index, style }) => (
    <div style={style}>
      <EmailItem email={emails[index]} />
    </div>
  );
  
  return (
    <FixedSizeList
      height={600}
      itemCount={emails.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
};
```

## Testing

### Unit Testing

```tsx
// __tests__/EmailItem.test.tsx
describe('EmailItem', () => {
  it('renders email subject and preview', () => {
    const email = mockEmail();
    render(<EmailItem email={email} />);
    
    expect(screen.getByText(email.subject)).toBeInTheDocument();
    expect(screen.getByText(email.preview)).toBeInTheDocument();
  });
  
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    const email = mockEmail();
    
    render(<EmailItem email={email} onClick={handleClick} />);
    fireEvent.click(screen.getByRole('article'));
    
    expect(handleClick).toHaveBeenCalledWith(email.id);
  });
});
```

### Integration Testing

```tsx
// __tests__/EmailList.integration.test.tsx
describe('EmailList Integration', () => {
  it('fetches and displays emails', async () => {
    const emails = [mockEmail(), mockEmail()];
    server.use(
      rest.get('/api/emails', (req, res, ctx) => {
        return res(ctx.json({ emails }));
      })
    );
    
    render(<EmailList />);
    
    await waitFor(() => {
      emails.forEach(email => {
        expect(screen.getByText(email.subject)).toBeInTheDocument();
      });
    });
  });
});
```

## Build & Deployment

### Build Configuration

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@headlessui/react', 'lucide-react'],
          editor: ['@uiw/react-md-editor'],
        }
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:9000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:9000',
        ws: true,
      }
    }
  }
});
```

### Environment Variables

```typescript
// env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_WS_URL: string;
  readonly VITE_PUBLIC_URL: string;
  readonly VITE_ENABLE_MOCK: string;
}
```

## Internationalization (i18n)

### i18n Architecture

```tsx
// i18n/config.ts
export const i18nConfig = {
  defaultLanguage: 'en',
  supportedLanguages: ['en', 'de', 'es', 'fr', 'it', 'pt', 'ja', 'zh'],
  fallbackLanguage: 'en',
  loadPath: '/locales/{{lng}}/{{ns}}.json',
  detection: {
    order: ['localStorage', 'navigator', 'htmlTag'],
    caches: ['localStorage']
  }
};
```

### Language Provider

```tsx
// contexts/LanguageContext.tsx
export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState(detectUserLanguage());
  
  const changeLanguage = async (lang: string) => {
    await i18n.changeLanguage(lang);
    localStorage.setItem('user_language', lang);
    setLanguage(lang);
    // Update document direction for RTL languages
    document.dir = isRTL(lang) ? 'rtl' : 'ltr';
  };
  
  return (
    <LanguageContext.Provider value={{ language, changeLanguage, t: i18n.t }}>
      {children}
    </LanguageContext.Provider>
  );
};
```

### Component Localization

```tsx
// components/LocalizedEmail.tsx
const LocalizedEmail: React.FC<{ email: Email }> = ({ email }) => {
  const { t, language } = useTranslation();
  const formattedDate = formatDate(email.date, language);
  
  return (
    <div className="email-card">
      <h3>{email.subject}</h3>
      <p className="email-meta">
        {t('email.from')}: {email.sender}
        {t('email.date')}: {formattedDate}
      </p>
      <div className="email-priority">
        {t(`priority.${email.priority}`)}
      </div>
    </div>
  );
};
```

### Dynamic Locale Loading

```tsx
// hooks/useLocale.ts
export const useLocale = () => {
  const [locale, setLocale] = useState<Locale | null>(null);
  const { language } = useLanguage();
  
  useEffect(() => {
    loadLocale(language).then(setLocale);
  }, [language]);
  
  return locale;
};

// Lazy load locale data
const loadLocale = async (lang: string): Promise<Locale> => {
  const module = await import(`../locales/${lang}/locale.js`);
  return module.default;
};
```

### RTL Support

```tsx
// utils/rtl.ts
export const isRTL = (language: string): boolean => {
  return ['ar', 'he', 'fa', 'ur'].includes(language);
};

// components/RTLWrapper.tsx
const RTLWrapper: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { language } = useLanguage();
  const isRtl = isRTL(language);
  
  return (
    <div dir={isRtl ? 'rtl' : 'ltr'} className={isRtl ? 'rtl' : ''}>
      {children}
    </div>
  );
};
```

## Future Enhancements

- Progressive Web App (PWA) support
- Offline functionality with service workers
- Advanced keyboard shortcuts
- Drag-and-drop email organization
- Rich text editor with AI assistance
- Voice commands integration
- Mobile app with React Native
- Electron desktop app
- Extended language support (20+ languages)
- AI-powered translation for unsupported languages