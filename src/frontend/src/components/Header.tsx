import { Link } from 'react-router-dom'
import { Book, Edit, Home } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <Book className="h-8 w-8 text-blue-600 mr-3" />
            <h1 className="text-2xl font-bold text-gray-900">MailMind Docs</h1>
          </div>
          <nav className="flex items-center space-x-4">
            <Link
              to="/"
              className="flex items-center text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              <Home className="h-4 w-4 mr-2" />
              Home
            </Link>
            <Link
              to="/docs"
              className="flex items-center text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              <Book className="h-4 w-4 mr-2" />
              Documentation
            </Link>
            <Link
              to="/edit"
              className="flex items-center text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              <Edit className="h-4 w-4 mr-2" />
              Editor
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}