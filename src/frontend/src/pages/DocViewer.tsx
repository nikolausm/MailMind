import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import rehypeRaw from 'rehype-raw'
import { Edit, FileText, AlertCircle } from 'lucide-react'
import axios from 'axios'
import MermaidDiagram from '../components/MermaidDiagram'
import 'highlight.js/styles/github-dark.css'

export default function DocViewer() {
  const params = useParams()
  const navigate = useNavigate()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  const docPath = params['*'] || 'README.md'

  useEffect(() => {
    fetchDocument()
  }, [docPath])

  const fetchDocument = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`/api/docs/${docPath}`)
      setContent(response.data.content)
    } catch (err: any) {
      console.error('Error fetching document:', err)
      
      // Check if it's a 404 error
      if (err.response?.status === 404) {
        setError(`Document "${docPath}" not found`)
        setContent('')
      } else {
        setError('Error loading document')
        // Only try fallback for non-404 errors
        try {
          // If docPath doesn't end with .md, add it for the fallback
          const fallbackPath = docPath.endsWith('.md') ? docPath : `${docPath}.md`
          const localResponse = await fetch(`/${fallbackPath}`)
          if (localResponse.ok) {
            const text = await localResponse.text()
            // Check if response is HTML (which means it's the index.html fallback)
            if (!text.includes('<!DOCTYPE html>') && !text.includes('<html')) {
              setContent(text)
              setError(null)
            } else {
              setContent('')
              setError(`Document "${docPath}" not found`)
            }
          }
        } catch (localErr) {
          console.error('Local fetch also failed:', localErr)
          setContent('')
        }
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading document...</div>
      </div>
    )
  }

  if (error && !content) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center">
          <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
          <span className="text-red-800">{error}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm">
        <div className="border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <FileText className="h-5 w-5 text-gray-400 mr-2" />
              <h1 className="text-xl font-semibold text-gray-900">{docPath}</h1>
            </div>
            <Link
              to={`/edit/${docPath}`}
              className="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
            >
              <Edit className="h-4 w-4 mr-1" />
              Edit
            </Link>
          </div>
        </div>
        
        <div className="px-6 py-8">
          <article className="prose prose-lg max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight, rehypeRaw]}
              components={{
                // Custom components for better rendering
                h1: ({ children }) => (
                  <h1 className="text-3xl font-bold text-gray-900 mb-4 pb-2 border-b border-gray-200">
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">
                    {children}
                  </h3>
                ),
                code: ({ className, children, ...props }) => {
                  const match = /language-(\w+)/.exec(className || '')
                  const isInline = !match
                  
                  // Check if it's a mermaid diagram
                  if (match && match[1] === 'mermaid') {
                    return <MermaidDiagram chart={String(children).replace(/\n$/, '')} />
                  }
                  
                  return isInline ? (
                    <code className="bg-gray-100 text-red-600 px-1 py-0.5 rounded text-sm" {...props}>
                      {children}
                    </code>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  )
                },
                pre: ({ children }) => (
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                    {children}
                  </pre>
                ),
                table: ({ children }) => (
                  <table className="min-w-full divide-y divide-gray-200">
                    {children}
                  </table>
                ),
                th: ({ children }) => (
                  <th className="px-4 py-2 bg-gray-50 text-left text-sm font-medium text-gray-900">
                    {children}
                  </th>
                ),
                td: ({ children }) => (
                  <td className="px-4 py-2 text-sm text-gray-700 border-t border-gray-200">
                    {children}
                  </td>
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </article>
        </div>
      </div>
    </div>
  )
}