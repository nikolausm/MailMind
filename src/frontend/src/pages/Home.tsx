import { Link } from 'react-router-dom'
import { Book, Edit, FileText, FolderOpen } from 'lucide-react'

export default function Home() {
  const quickLinks = [
    { title: 'Overview', path: '/docs/README.md', icon: FileText },
    { title: 'Architecture', path: '/docs/CLAUDE.md', icon: FolderOpen },
    { title: 'Authentication', path: '/docs/docs/AUTHENTICATION.md', icon: FileText },
    { title: 'Auth Flows', path: '/docs/docs/AUTH_FLOWS.md', icon: FileText },
  ]

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          MailMind Documentation
        </h1>
        <p className="text-lg text-gray-600 mb-6">
          Comprehensive documentation for the MailMind intelligent email client system.
          Browse documentation, view formatted markdown files, and edit content directly in the browser.
        </p>
        <div className="flex space-x-4">
          <Link
            to="/docs/README.md"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Book className="h-5 w-5 mr-2" />
            Browse Docs
          </Link>
          <Link
            to="/edit"
            className="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            <Edit className="h-5 w-5 mr-2" />
            Edit Documentation
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Features</h2>
          <ul className="space-y-2 text-gray-600">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Hierarchical documentation structure
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Markdown rendering with syntax highlighting
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Live markdown editor with preview
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              Support for Mermaid diagrams
            </li>
          </ul>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Links</h2>
          <div className="space-y-2">
            {quickLinks.map((link) => {
              const Icon = link.icon
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className="flex items-center p-2 text-gray-600 hover:bg-gray-50 rounded-md"
                >
                  <Icon className="h-5 w-5 mr-3 text-gray-400" />
                  {link.title}
                </Link>
              )
            })}
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-yellow-900 mb-2">
          Documentation Structure
        </h3>
        <p className="text-yellow-800 mb-4">
          The documentation is organized hierarchically:
        </p>
        <ul className="text-yellow-700 space-y-1 text-sm">
          <li>• <strong>Getting Started</strong> - Overview, installation, quick start</li>
          <li>• <strong>Architecture</strong> - System design and components</li>
          <li>• <strong>Authentication</strong> - Auth flows, OAuth providers, security</li>
          <li>• <strong>AI & RAG</strong> - Agent system, email processing, vector DB</li>
          <li>• <strong>API Reference</strong> - Endpoints, WebSocket, error codes</li>
          <li>• <strong>Deployment</strong> - Development, production, Docker</li>
        </ul>
      </div>
    </div>
  )
}