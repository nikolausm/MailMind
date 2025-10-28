# Frontend State Management

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Übersicht](#übersicht)
- [State-Architektur](#state-architektur)
- [Zustand Store](#zustand-store)
- [React Query Integration](#react-query-integration)
- [Context API](#context-api)
- [State Synchronization](#state-synchronization)
- [Performance Optimierung](#performance-optimierung)
- [DevTools Integration](#devtools-integration)
- [Testing State](#testing-state)
- [Best Practices](#best-practices)

### Verwandte Dokumente
- [🎨 Frontend-Architektur](./frontend-architecture.md) - UI-Architektur
- [🧩 Frontend-Komponenten](./frontend-components.md) - Komponenten-Bibliothek
- [🌍 Internationalisierung](./internationalization.md) - i18n-System und Übersetzungen
- [📐 UI-Mockups](./ui-mockups.md) - Design-Entwürfe
- [📘 Benutzerhandbuch](./user-guide.md) - Bedienungsanleitung

## Übersicht

MailMind verwendet eine Kombination aus Zustand, React Query und Context API für effizientes State Management.

## State-Architektur

```
┌─────────────────────────────────────────────┐
│                App State                     │
├─────────────┬─────────────┬─────────────────┤
│  Local UI   │   Server    │     Global      │
│   State     │    State    │     State       │
├─────────────┼─────────────┼─────────────────┤
│  useState   │ React Query │    Zustand      │
│  useReducer │   (Cache)   │  Context API    │
└─────────────┴─────────────┴─────────────────┘
```

## Zustand Store

### Store-Struktur

```typescript
// stores/index.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface AppStore {
  // User State
  user: User | null;
  isAuthenticated: boolean;
  
  // Email State
  selectedEmails: string[];
  currentFolder: string;
  filters: FilterState;
  
  // UI State
  sidebarOpen: boolean;
  theme: 'light' | 'dark' | 'auto';
  composeModalOpen: boolean;
  
  // Actions
  setUser: (user: User | null) => void;
  selectEmail: (id: string) => void;
  deselectEmail: (id: string) => void;
  toggleSidebar: () => void;
  setTheme: (theme: Theme) => void;
}

export const useStore = create<AppStore>()(
  devtools(
    persist(
      immer((set) => ({
        // Initial State
        user: null,
        isAuthenticated: false,
        selectedEmails: [],
        currentFolder: 'inbox',
        filters: defaultFilters,
        sidebarOpen: true,
        theme: 'auto',
        composeModalOpen: false,
        
        // Actions
        setUser: (user) =>
          set((state) => {
            state.user = user;
            state.isAuthenticated = !!user;
          }),
          
        selectEmail: (id) =>
          set((state) => {
            if (!state.selectedEmails.includes(id)) {
              state.selectedEmails.push(id);
            }
          }),
          
        deselectEmail: (id) =>
          set((state) => {
            state.selectedEmails = state.selectedEmails.filter(
              (emailId) => emailId !== id
            );
          }),
          
        toggleSidebar: () =>
          set((state) => {
            state.sidebarOpen = !state.sidebarOpen;
          }),
          
        setTheme: (theme) =>
          set((state) => {
            state.theme = theme;
          }),
      })),
      {
        name: 'mailmind-storage',
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen,
        }),
      }
    )
  )
);
```

### Store Slices

```typescript
// stores/emailStore.ts
interface EmailStore {
  emails: Email[];
  totalCount: number;
  loading: boolean;
  error: Error | null;
  
  // Derived State
  unreadCount: number;
  selectedEmail: Email | null;
  
  // Actions
  fetchEmails: (filters?: FilterOptions) => Promise<void>;
  markAsRead: (ids: string[]) => void;
  deleteEmails: (ids: string[]) => void;
  archiveEmails: (ids: string[]) => void;
  moveToFolder: (ids: string[], folder: string) => void;
}

// stores/aiStore.ts  
interface AIStore {
  suggestions: AISuggestion[];
  processing: boolean;
  autoTaggingEnabled: boolean;
  smartComposeEnabled: boolean;
  
  // Actions
  generateSuggestion: (context: string) => Promise<void>;
  applySuggestion: (suggestion: AISuggestion) => void;
  toggleAutoTagging: () => void;
}
```

## React Query Integration

### Query Configuration

```typescript
// services/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 2,
    },
  },
});

// Query Keys Management
export const queryKeys = {
  all: ['emails'] as const,
  lists: () => [...queryKeys.all, 'list'] as const,
  list: (filters: FilterOptions) => [...queryKeys.lists(), filters] as const,
  details: () => [...queryKeys.all, 'detail'] as const,
  detail: (id: string) => [...queryKeys.details(), id] as const,
  search: (query: string) => ['search', query] as const,
};
```

### Custom Hooks

```typescript
// hooks/useEmails.ts
export const useEmails = (filters?: FilterOptions) => {
  return useQuery({
    queryKey: queryKeys.list(filters || {}),
    queryFn: () => emailService.fetchEmails(filters),
    select: (data) => ({
      ...data,
      emails: data.emails.map(transformEmail),
    }),
  });
};

// hooks/useEmailMutations.ts
export const useMarkAsRead = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: emailService.markAsRead,
    onMutate: async (emailIds) => {
      // Optimistic Update
      await queryClient.cancelQueries({ queryKey: queryKeys.lists() });
      
      const previousEmails = queryClient.getQueryData(queryKeys.lists());
      
      queryClient.setQueryData(queryKeys.lists(), (old) => {
        return {
          ...old,
          emails: old.emails.map((email) =>
            emailIds.includes(email.id)
              ? { ...email, isRead: true }
              : email
          ),
        };
      });
      
      return { previousEmails };
    },
    onError: (err, emailIds, context) => {
      // Rollback on error
      if (context?.previousEmails) {
        queryClient.setQueryData(queryKeys.lists(), context.previousEmails);
      }
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: queryKeys.lists() });
    },
  });
};
```

### Infinite Queries

```typescript
// hooks/useInfiniteEmails.ts
export const useInfiniteEmails = (filters?: FilterOptions) => {
  return useInfiniteQuery({
    queryKey: ['emails', 'infinite', filters],
    queryFn: ({ pageParam = 0 }) =>
      emailService.fetchEmails({
        ...filters,
        offset: pageParam,
        limit: 20,
      }),
    getNextPageParam: (lastPage, pages) => {
      if (lastPage.emails.length < 20) return undefined;
      return pages.length * 20;
    },
    getPreviousPageParam: (firstPage, pages) => {
      if (pages.length <= 1) return undefined;
      return (pages.length - 2) * 20;
    },
  });
};

// Verwendung
const EmailList = () => {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteEmails();
  
  const emails = data?.pages.flatMap(page => page.emails) ?? [];
  
  return (
    <InfiniteScroll
      dataLength={emails.length}
      next={fetchNextPage}
      hasMore={hasNextPage}
      loader={<LoadingSpinner />}
    >
      {emails.map(email => (
        <EmailItem key={email.id} email={email} />
      ))}
    </InfiniteScroll>
  );
};
```

## Context API

### Auth Context

```typescript
// contexts/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Check for existing session
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const userData = await authService.validateToken(token);
          setUser(userData);
        }
      } catch (error) {
        localStorage.removeItem('access_token');
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, []);
  
  const login = async (credentials: LoginCredentials) => {
    const { user, token } = await authService.login(credentials);
    localStorage.setItem('access_token', token);
    setUser(user);
  };
  
  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    queryClient.clear();
  };
  
  if (isLoading) {
    return <LoadingScreen />;
  }
  
  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        logout,
        refreshToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
```

### WebSocket Context

```typescript
// contexts/WebSocketContext.tsx
interface WebSocketContextType {
  socket: WebSocket | null;
  isConnected: boolean;
  sendMessage: (message: WSMessage) => void;
  subscribe: (event: string, handler: (data: any) => void) => () => void;
}

export const WebSocketProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const handlers = useRef<Map<string, Set<Function>>>(new Map());
  
  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    
    ws.onopen = () => {
      setIsConnected(true);
      setSocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const eventHandlers = handlers.current.get(data.type);
      
      if (eventHandlers) {
        eventHandlers.forEach(handler => handler(data.payload));
      }
    };
    
    ws.onclose = () => {
      setIsConnected(false);
      // Implement reconnection logic
      setTimeout(() => {
        // Reconnect
      }, 5000);
    };
    
    return () => {
      ws.close();
    };
  }, []);
  
  const subscribe = (event: string, handler: (data: any) => void) => {
    if (!handlers.current.has(event)) {
      handlers.current.set(event, new Set());
    }
    
    handlers.current.get(event)!.add(handler);
    
    // Return unsubscribe function
    return () => {
      handlers.current.get(event)?.delete(handler);
    };
  };
  
  const sendMessage = (message: WSMessage) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify(message));
    }
  };
  
  return (
    <WebSocketContext.Provider
      value={{ socket, isConnected, sendMessage, subscribe }}
    >
      {children}
    </WebSocketContext.Provider>
  );
};
```

## State Synchronization

### Cross-Tab Synchronization

```typescript
// hooks/useCrossTabSync.ts
export const useCrossTabSync = () => {
  useEffect(() => {
    const channel = new BroadcastChannel('mailmind-sync');
    
    channel.onmessage = (event) => {
      const { type, payload } = event.data;
      
      switch (type) {
        case 'EMAIL_UPDATE':
          queryClient.setQueryData(
            queryKeys.detail(payload.id),
            payload.email
          );
          break;
          
        case 'LOGOUT':
          useStore.getState().setUser(null);
          break;
          
        case 'THEME_CHANGE':
          useStore.getState().setTheme(payload.theme);
          break;
      }
    };
    
    return () => channel.close();
  }, []);
  
  const broadcast = (type: string, payload: any) => {
    const channel = new BroadcastChannel('mailmind-sync');
    channel.postMessage({ type, payload });
    channel.close();
  };
  
  return { broadcast };
};
```

### Offline Support

```typescript
// hooks/useOfflineSync.ts
export const useOfflineSync = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingActions, setPendingActions] = useState<Action[]>([]);
  
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      // Sync pending actions
      syncPendingActions();
    };
    
    const handleOffline = () => {
      setIsOnline(false);
    };
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  const syncPendingActions = async () => {
    for (const action of pendingActions) {
      try {
        await executeAction(action);
        setPendingActions(prev => prev.filter(a => a.id !== action.id));
      } catch (error) {
        console.error('Failed to sync action:', action, error);
      }
    }
  };
  
  const queueAction = (action: Action) => {
    if (isOnline) {
      return executeAction(action);
    } else {
      setPendingActions(prev => [...prev, action]);
      // Store in IndexedDB for persistence
      offlineStorage.saveAction(action);
    }
  };
  
  return { isOnline, queueAction, pendingActions };
};
```

## Performance Optimierung

### Selektoren und Memoization

```typescript
// stores/selectors.ts
import { shallow } from 'zustand/shallow';

// Effiziente Selektoren
export const useSelectedEmails = () =>
  useStore((state) => state.selectedEmails, shallow);

export const useEmailById = (id: string) =>
  useStore((state) => state.emails.find(e => e.id === id));

// Memoized Selektoren
export const useFilteredEmails = () => {
  const emails = useStore((state) => state.emails);
  const filters = useStore((state) => state.filters);
  
  return useMemo(() => {
    return emails.filter(email => {
      if (filters.unread && email.isRead) return false;
      if (filters.starred && !email.isStarred) return false;
      if (filters.folder && email.folder !== filters.folder) return false;
      return true;
    });
  }, [emails, filters]);
};
```

### Lazy State Updates

```typescript
// Debounced Updates
const useDebounceUpdate = () => {
  const updateFilters = useStore((state) => state.updateFilters);
  
  const debouncedUpdate = useMemo(
    () => debounce(updateFilters, 300),
    [updateFilters]
  );
  
  return debouncedUpdate;
};

// Batched Updates
import { unstable_batchedUpdates } from 'react-dom';

const handleBulkSelection = (emailIds: string[]) => {
  unstable_batchedUpdates(() => {
    emailIds.forEach(id => {
      store.getState().selectEmail(id);
    });
    store.getState().setSelectionMode(true);
  });
};
```

## DevTools Integration

### Zustand DevTools

```typescript
// stores/devtools.ts
import { devtools } from 'zustand/middleware';

export const createStore = (name: string) => {
  return devtools(
    (set, get) => ({
      // Store implementation
    }),
    {
      name,
      trace: true,
      anonymousActionType: 'action',
    }
  );
};
```

### React Query DevTools

```tsx
// App.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        {/* App content */}
      </Router>
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}
```

## Testing State

### Store Testing

```typescript
// __tests__/emailStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useStore } from '../stores';

describe('EmailStore', () => {
  beforeEach(() => {
    useStore.setState({ emails: [], selectedEmails: [] });
  });
  
  it('should select email', () => {
    const { result } = renderHook(() => useStore());
    
    act(() => {
      result.current.selectEmail('email-1');
    });
    
    expect(result.current.selectedEmails).toContain('email-1');
  });
  
  it('should not duplicate selected emails', () => {
    const { result } = renderHook(() => useStore());
    
    act(() => {
      result.current.selectEmail('email-1');
      result.current.selectEmail('email-1');
    });
    
    expect(result.current.selectedEmails).toHaveLength(1);
  });
});
```

### Query Testing

```typescript
// __tests__/useEmails.test.ts
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderHook, waitFor } from '@testing-library/react';
import { useEmails } from '../hooks/useEmails';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useEmails', () => {
  it('should fetch emails', async () => {
    const { result } = renderHook(() => useEmails(), {
      wrapper: createWrapper(),
    });
    
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });
    
    expect(result.current.data?.emails).toBeDefined();
  });
});
```

## Best Practices

1. **State Colocation**: Halte State so lokal wie möglich
2. **Normalisierung**: Normalisiere komplexe State-Strukturen
3. **Optimistic Updates**: Nutze optimistische Updates für bessere UX
4. **Error Recovery**: Implementiere Rollback-Mechanismen
5. **Persist Selectively**: Speichere nur notwendige State-Teile
6. **Subscribe Granular**: Abonniere nur benötigte State-Teile
7. **Test State Logic**: Teste State-Transformationen isoliert

---

*Weitere Beispiele und Patterns in der [Component Library](./frontend-components.md)*