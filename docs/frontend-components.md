# Frontend Component Library

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Übersicht](#übersicht)
- [Design System](#design-system)
- [Core Components](#core-components)
- [Email-Specific Components](#email-specific-components)
- [Form Components](#form-components)
- [Loading & Error States](#loading--error-states)
- [Accessibility](#accessibility)
- [Performance Patterns](#performance-patterns)
- [Testing Components](#testing-components)
- [Storybook Integration](#storybook-integration)
- [Best Practices](#best-practices)
- [Migration Guide](#migration-guide)

### Verwandte Dokumente
- [🎨 Frontend-Architektur](./frontend-architecture.md) - UI-Architektur
- [📊 Frontend State Management](./frontend-state-management.md) - Zustand-Verwaltung
- [🌍 Internationalisierung](./internationalization.md) - i18n-System und Übersetzungen
- [📐 UI-Mockups](./ui-mockups.md) - Design-Entwürfe
- [📘 Benutzerhandbuch](./user-guide.md) - Bedienungsanleitung

## Übersicht

Detaillierte Dokumentation der MailMind UI-Komponenten-Bibliothek mit Verwendungsbeispielen, Props und Best Practices.

## Design System

### Design Tokens

```typescript
// design-tokens.ts
export const tokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      900: '#1e3a8a'
    },
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      500: '#6b7280',
      900: '#111827'
    },
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6'
  },
  spacing: {
    xs: '0.5rem',
    sm: '1rem',
    md: '1.5rem',
    lg: '2rem',
    xl: '3rem'
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace']
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem'
    }
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    full: '9999px'
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
  }
};
```

### Theme Provider

```tsx
// contexts/ThemeContext.tsx
interface ThemeConfig {
  mode: 'light' | 'dark' | 'auto';
  primaryColor: string;
  fontSize: 'small' | 'medium' | 'large';
  density: 'comfortable' | 'compact' | 'spacious';
  animations: boolean;
}

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<ThemeConfig>(defaultTheme);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div className={`theme-${theme.mode} density-${theme.density}`}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
};
```

## Core Components

### Button

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  onClick?: () => void;
  children: ReactNode;
}

// Verwendung
<Button 
  variant="primary" 
  size="md" 
  leftIcon={<PlusIcon />}
  loading={isSubmitting}
>
  Neue E-Mail
</Button>
```

### Input

```tsx
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'search' | 'number';
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  placeholder?: string;
  helperText?: string;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  leftAddon?: ReactNode;
  rightAddon?: ReactNode;
  onChange?: (value: string) => void;
}

// Verwendung
<Input
  type="email"
  label="E-Mail-Adresse"
  placeholder="name@beispiel.de"
  error={errors.email}
  required
  onChange={handleEmailChange}
/>
```

### Modal

```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEsc?: boolean;
  showCloseButton?: boolean;
  footer?: ReactNode;
  children: ReactNode;
}

// Verwendung
<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="E-Mail verfassen"
  size="lg"
  footer={
    <>
      <Button variant="ghost" onClick={handleClose}>
        Abbrechen
      </Button>
      <Button variant="primary" onClick={handleSend}>
        Senden
      </Button>
    </>
  }
>
  <ComposeEmailForm />
</Modal>
```

### Toast/Notification

```tsx
interface ToastProps {
  type?: 'success' | 'error' | 'warning' | 'info';
  title: string;
  description?: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// Verwendung
const { showToast } = useToast();

showToast({
  type: 'success',
  title: 'E-Mail gesendet',
  description: 'Ihre Nachricht wurde erfolgreich versendet.',
  duration: 5000
});
```

### Dropdown Menu

```tsx
interface DropdownProps {
  trigger: ReactNode;
  align?: 'start' | 'center' | 'end';
  items: DropdownItem[];
}

interface DropdownItem {
  label: string;
  icon?: ReactNode;
  onClick?: () => void;
  divider?: boolean;
  disabled?: boolean;
  danger?: boolean;
}

// Verwendung
<Dropdown
  trigger={<Button variant="ghost"><MoreIcon /></Button>}
  items={[
    { label: 'Bearbeiten', icon: <EditIcon />, onClick: handleEdit },
    { label: 'Duplizieren', icon: <CopyIcon />, onClick: handleDuplicate },
    { divider: true },
    { label: 'Löschen', icon: <TrashIcon />, onClick: handleDelete, danger: true }
  ]}
/>
```

## Email-Specific Components

### EmailListItem

```tsx
interface EmailListItemProps {
  email: Email;
  isSelected?: boolean;
  isRead?: boolean;
  showCheckbox?: boolean;
  onClick?: () => void;
  onSelect?: (selected: boolean) => void;
}

// Features:
- Swipe-Aktionen (mobile)
- Kontextmenü (desktop)
- Quick Actions (Archiv, Löschen, Markieren)
- AI-Tags Anzeige
- Anhang-Indikator
```

### EmailComposer

```tsx
interface EmailComposerProps {
  mode?: 'compose' | 'reply' | 'forward';
  originalEmail?: Email;
  defaultRecipients?: string[];
  onSend: (email: DraftEmail) => Promise<void>;
  onSaveDraft: (draft: DraftEmail) => void;
  onCancel: () => void;
}

// Features:
- Rich Text Editor (Markdown/WYSIWYG)
- Datei-Upload mit Drag & Drop
- Empfänger-Autovervollständigung
- AI-Schreibassistent
- Vorlagen-System
- Geplantes Senden
```

### EmailViewer

```tsx
interface EmailViewerProps {
  email: Email;
  showThread?: boolean;
  onReply?: () => void;
  onForward?: () => void;
  onDelete?: () => void;
  onArchive?: () => void;
}

// Features:
- Threaded Conversations
- Inline-Bilder
- Anhang-Preview
- Code-Highlighting
- Link-Preview
- Übersetzung
```

## Form Components

### FormField

```tsx
interface FormFieldProps {
  name: string;
  label?: string;
  required?: boolean;
  error?: string;
  helperText?: string;
  children: ReactElement;
}

// Mit React Hook Form
<FormField
  name="subject"
  label="Betreff"
  required
  error={errors.subject?.message}
>
  <Input {...register('subject', { required: 'Betreff erforderlich' })} />
</FormField>
```

### Validation

```typescript
// validation-schemas.ts
import { z } from 'zod';

export const emailSchema = z.object({
  to: z.array(z.string().email()).min(1, 'Mindestens ein Empfänger'),
  subject: z.string().min(1, 'Betreff erforderlich'),
  body: z.string().min(1, 'Nachricht erforderlich'),
  cc: z.array(z.string().email()).optional(),
  bcc: z.array(z.string().email()).optional(),
  attachments: z.array(z.instanceof(File)).optional()
});

// Verwendung mit React Hook Form
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(emailSchema)
});
```

## Loading & Error States

### LoadingSpinner

```tsx
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  fullScreen?: boolean;
  label?: string;
}

// Verwendung
<LoadingSpinner size="lg" label="E-Mails werden geladen..." />
```

### ErrorBoundary

```tsx
class ErrorBoundary extends Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error reporting service
    logErrorToService(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback
          error={this.state.error}
          resetError={() => this.setState({ hasError: false })}
        />
      );
    }
    
    return this.props.children;
  }
}
```

### EmptyState

```tsx
interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// Verwendung
<EmptyState
  icon={<InboxIcon />}
  title="Keine E-Mails"
  description="Ihr Posteingang ist leer"
  action={{
    label: "E-Mail verfassen",
    onClick: handleCompose
  }}
/>
```

## Accessibility

### Focus Management

```tsx
// hooks/useFocusTrap.ts
export const useFocusTrap = (ref: RefObject<HTMLElement>) => {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    firstElement?.focus();
    
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };
    
    element.addEventListener('keydown', handleKeyDown);
    return () => element.removeEventListener('keydown', handleKeyDown);
  }, [ref]);
};
```

### Keyboard Navigation

```tsx
// hooks/useKeyboardShortcuts.ts
export const useKeyboardShortcuts = () => {
  useEffect(() => {
    const shortcuts = {
      'cmd+k': () => openSearchModal(),
      'cmd+n': () => openComposeModal(),
      'cmd+shift+a': () => selectAllEmails(),
      'j': () => navigateToNext(),
      'k': () => navigateToPrevious(),
      'x': () => toggleSelection(),
      'e': () => archiveSelected(),
      'd': () => deleteSelected(),
    };
    
    // Implementation...
  }, []);
};
```

### Screen Reader Support

```tsx
// Verwendung von ARIA-Attributen
<button
  aria-label="E-Mail als gelesen markieren"
  aria-pressed={isRead}
  aria-describedby="mark-read-tooltip"
>
  <EnvelopeIcon aria-hidden="true" />
</button>

<div role="status" aria-live="polite" aria-atomic="true">
  {loading && <span>E-Mails werden geladen...</span>}
  {!loading && <span>{emails.length} E-Mails gefunden</span>}
</div>
```

## Performance Patterns

### Lazy Loading

```tsx
// Komponenten lazy laden
const EmailEditor = lazy(() => import('./components/EmailEditor'));
const SettingsPanel = lazy(() => import('./components/SettingsPanel'));
const ReportsDashboard = lazy(() => import('./components/ReportsDashboard'));

// Bilder lazy laden
const LazyImage: React.FC<{ src: string; alt: string }> = ({ src, alt }) => {
  const [imageSrc, setImageSrc] = useState<string>('');
  const imgRef = useRef<HTMLImageElement>(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setImageSrc(src);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );
    
    if (imgRef.current) {
      observer.observe(imgRef.current);
    }
    
    return () => observer.disconnect();
  }, [src]);
  
  return <img ref={imgRef} src={imageSrc || placeholder} alt={alt} />;
};
```

### Debouncing & Throttling

```tsx
// hooks/useDebounce.ts
export const useDebounce = <T,>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(handler);
  }, [value, delay]);
  
  return debouncedValue;
};

// Verwendung in Suche
const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 300);
  
  useEffect(() => {
    if (debouncedSearch) {
      performSearch(debouncedSearch);
    }
  }, [debouncedSearch]);
};
```

### Virtualization

```tsx
// Große Listen virtualisieren
import { VariableSizeList } from 'react-window';

const VirtualEmailList: React.FC<{ emails: Email[] }> = ({ emails }) => {
  const getItemSize = (index: number) => {
    // Variable Höhe basierend auf Inhalt
    const email = emails[index];
    return email.preview.length > 100 ? 120 : 80;
  };
  
  const Row = ({ index, style }) => (
    <div style={style}>
      <EmailListItem email={emails[index]} />
    </div>
  );
  
  return (
    <VariableSizeList
      height={window.innerHeight - 200}
      itemCount={emails.length}
      itemSize={getItemSize}
      width="100%"
      overscanCount={5}
    >
      {Row}
    </VariableSizeList>
  );
};
```

## Testing Components

### Unit Tests

```tsx
// __tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });
  
  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
  
  it('is disabled when loading', () => {
    render(<Button loading onClick={jest.fn()}>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Visual Regression Testing

```typescript
// visual-tests/Button.visual.test.tsx
import { test } from '@playwright/test';

test.describe('Button Visual Tests', () => {
  test('default button', async ({ page }) => {
    await page.goto('/storybook/button-default');
    await expect(page).toHaveScreenshot('button-default.png');
  });
  
  test('button hover state', async ({ page }) => {
    await page.goto('/storybook/button-default');
    await page.hover('button');
    await expect(page).toHaveScreenshot('button-hover.png');
  });
  
  test('button variants', async ({ page }) => {
    await page.goto('/storybook/button-variants');
    await expect(page).toHaveScreenshot('button-variants.png');
  });
});
```

## Storybook Integration

```tsx
// stories/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../components/Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'ghost', 'danger'],
    },
    size: {
      control: { type: 'select' },
      options: ['xs', 'sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};

export const WithIcon: Story = {
  args: {
    variant: 'primary',
    leftIcon: <PlusIcon />,
    children: 'Neue E-Mail',
  },
};

export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Wird geladen...',
  },
};
```

## Best Practices

### Component Guidelines

1. **Single Responsibility**: Jede Komponente hat eine klare Aufgabe
2. **Composition over Inheritance**: Komponenten zusammensetzen statt vererben
3. **Props Interface**: Klare TypeScript-Interfaces für alle Props
4. **Default Props**: Sinnvolle Standardwerte definieren
5. **Error Boundaries**: Fehler graceful behandeln
6. **Accessibility**: ARIA-Labels und Keyboard-Navigation
7. **Performance**: Memoization wo sinnvoll
8. **Testing**: Unit-Tests für alle Komponenten

### Naming Conventions

```typescript
// Komponenten: PascalCase
Button.tsx
EmailListItem.tsx

// Props Interfaces: ComponentNameProps
interface ButtonProps { }
interface EmailListItemProps { }

// Hooks: use + Funktionsname
useDebounce()
useKeyboardShortcuts()

// Event Handlers: handle + Event
handleClick()
handleSubmit()

// Boolean Props: is/has/should + Adjektiv
isLoading
hasError
shouldAutoFocus
```

### Folder Structure

```
components/
├── common/           # Wiederverwendbare UI-Komponenten
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx
│   │   └── index.ts
│   ├── Input/
│   └── Modal/
├── email/           # E-Mail-spezifische Komponenten
│   ├── EmailList/
│   ├── EmailViewer/
│   └── EmailComposer/
├── layout/          # Layout-Komponenten
│   ├── Header/
│   ├── Sidebar/
│   └── Footer/
└── ai/              # KI-Feature-Komponenten
    ├── AIAssistant/
    ├── SmartCompose/
    └── SuggestionPanel/
```

## Migration Guide

### Von Class zu Function Components

```tsx
// Alt (Class Component)
class EmailList extends Component<Props, State> {
  state = { emails: [] };
  
  componentDidMount() {
    this.fetchEmails();
  }
  
  fetchEmails = async () => {
    const emails = await api.getEmails();
    this.setState({ emails });
  }
  
  render() {
    return <div>{/* ... */}</div>;
  }
}

// Neu (Function Component mit Hooks)
const EmailList: React.FC<Props> = () => {
  const [emails, setEmails] = useState<Email[]>([]);
  
  useEffect(() => {
    const fetchEmails = async () => {
      const data = await api.getEmails();
      setEmails(data);
    };
    fetchEmails();
  }, []);
  
  return <div>{/* ... */}</div>;
};
```

---

*Diese Dokumentation wird kontinuierlich erweitert. Für Beispiele siehe Storybook unter http://localhost:6006*