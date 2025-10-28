import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { ChevronDown, ChevronRight, FileText } from 'lucide-react'
import { navigation } from '../data/navigation'
import clsx from 'clsx'

export default function Sidebar() {
  const location = useLocation()
  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    'getting-started': true,
    'authentication': true,
  })

  const toggleExpand = (id: string) => {
    setExpanded(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const isActive = (path?: string) => {
    if (!path) return false
    return location.pathname === `/docs${path}` || location.pathname === `/edit${path}`
  }

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <nav className="p-4">
        <ul className="space-y-2">
          {navigation.map((section) => (
            <li key={section.id}>
              <button
                onClick={() => toggleExpand(section.id)}
                className="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md"
              >
                <span className="flex items-center">
                  {section.icon && <span className="mr-2">{section.icon}</span>}
                  {section.title}
                </span>
                {section.children && (
                  expanded[section.id] ? (
                    <ChevronDown className="h-4 w-4" />
                  ) : (
                    <ChevronRight className="h-4 w-4" />
                  )
                )}
              </button>
              {section.children && expanded[section.id] && (
                <ul className="ml-6 mt-2 space-y-1">
                  {section.children.map((item) => (
                    <li key={item.id}>
                      <Link
                        to={`/docs${item.path}`}
                        className={clsx(
                          'flex items-center px-3 py-2 text-sm rounded-md',
                          isActive(item.path)
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                        )}
                      >
                        <FileText className="h-4 w-4 mr-2" />
                        {item.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}