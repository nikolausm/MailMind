export interface NavItem {
  id: string
  title: string
  icon?: string
  path?: string
  children?: NavItem[]
}

export const navigation: NavItem[] = [
  {
    id: 'getting-started',
    title: 'Getting Started',
    icon: '🏠',
    children: [
      {
        id: 'overview',
        title: 'Overview',
        path: '/README.md'
      },
      {
        id: 'installation',
        title: 'Installation',
        path: '/docs/installation.md'
      },
      {
        id: 'quick-start',
        title: 'Quick Start',
        path: '/docs/quick-start.md'
      }
    ]
  },
  {
    id: 'architecture',
    title: 'Architecture',
    icon: '🏗️',
    children: [
      {
        id: 'system-overview',
        title: 'System Overview',
        path: '/CLAUDE.md'
      },
      {
        id: 'backend-arch',
        title: 'Backend Architecture',
        path: '/docs/backend-architecture.md'
      },
      {
        id: 'frontend-arch',
        title: 'Frontend Architecture',
        path: '/docs/frontend-architecture.md'
      }
    ]
  },
  {
    id: 'authentication',
    title: 'Authentication',
    icon: '🔐',
    children: [
      {
        id: 'auth-overview',
        title: 'Overview',
        path: '/docs/AUTHENTICATION.md'
      },
      {
        id: 'auth-flows',
        title: 'Authentication Flows',
        path: '/docs/AUTH_FLOWS.md'
      },
      {
        id: 'oauth-providers',
        title: 'OAuth Providers',
        path: '/docs/oauth-providers.md'
      }
    ]
  },
  {
    id: 'ai-rag',
    title: 'AI & RAG System',
    icon: '🤖',
    children: [
      {
        id: 'agent-architecture',
        title: 'Agent Architecture',
        path: '/docs/agent-architecture.md'
      },
      {
        id: 'email-pipeline',
        title: 'Email Processing Pipeline',
        path: '/docs/email-pipeline.md'
      },
      {
        id: 'vector-db',
        title: 'Vector Database',
        path: '/docs/vector-database.md'
      }
    ]
  },
  {
    id: 'api',
    title: 'API Reference',
    icon: '🔌',
    children: [
      {
        id: 'rest-endpoints',
        title: 'REST Endpoints',
        path: '/docs/api/endpoints.md'
      },
      {
        id: 'websocket',
        title: 'WebSocket Events',
        path: '/docs/api/websocket.md'
      },
      {
        id: 'error-codes',
        title: 'Error Codes',
        path: '/docs/api/errors.md'
      }
    ]
  },
  {
    id: 'deployment',
    title: 'Deployment',
    icon: '🚀',
    children: [
      {
        id: 'dev-setup',
        title: 'Development Setup',
        path: '/docs/deployment/development.md'
      },
      {
        id: 'production',
        title: 'Production Deployment',
        path: '/docs/deployment/production.md'
      },
      {
        id: 'docker',
        title: 'Docker Configuration',
        path: '/docs/deployment/docker.md'
      }
    ]
  }
]