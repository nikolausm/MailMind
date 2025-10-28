import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import MDEditor from '@uiw/react-md-editor'
import { Save, X, Eye, Edit } from 'lucide-react'
import axios from 'axios'

export default function DocEditor() {
  const params = useParams()
  const navigate = useNavigate()
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [previewMode, setPreviewMode] = useState(false)
  
  const docPath = params['*'] || ''

  useEffect(() => {
    if (docPath) {
      fetchDocument()
    } else {
      setLoading(false)
    }
  }, [docPath])

  const fetchDocument = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`/api/docs/${docPath}`)
      setContent(response.data.content)
      setOriginalContent(response.data.content)
    } catch (err) {
      console.error('Error fetching document:', err)
      // For demo, try local fetch
      try {
        const localResponse = await fetch(`/${docPath}`)
        if (localResponse.ok) {
          const text = await localResponse.text()
          setContent(text)
          setOriginalContent(text)
        }
      } catch (localErr) {
        console.error('Local fetch also failed:', localErr)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!docPath) {
      alert('Please specify a file path')
      return
    }
    
    setSaving(true)
    try {
      await axios.put(`/api/docs/${docPath}`, {
        content,
      })
      setOriginalContent(content)
      alert('Document saved successfully!')
    } catch (err) {
      console.error('Error saving document:', err)
      alert('Error saving document. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    if (content !== originalContent) {
      if (confirm('You have unsaved changes. Are you sure you want to cancel?')) {
        navigate(-1)
      }
    } else {
      navigate(-1)
    }
  }

  const hasChanges = content !== originalContent

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading document...</div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      <div className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-gray-900">
              {docPath ? `Editing: ${docPath}` : 'New Document'}
            </h1>
            {hasChanges && (
              <span className="ml-3 text-sm text-orange-600">• Unsaved changes</span>
            )}
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setPreviewMode(!previewMode)}
              className="inline-flex items-center px-3 py-1.5 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200"
            >
              {previewMode ? (
                <>
                  <Edit className="h-4 w-4 mr-1" />
                  Edit
                </>
              ) : (
                <>
                  <Eye className="h-4 w-4 mr-1" />
                  Preview
                </>
              )}
            </button>
            <button
              onClick={handleSave}
              disabled={saving || !hasChanges}
              className="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Save className="h-4 w-4 mr-1" />
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancel}
              className="inline-flex items-center px-3 py-1.5 bg-gray-600 text-white text-sm rounded-md hover:bg-gray-700"
            >
              <X className="h-4 w-4 mr-1" />
              Cancel
            </button>
          </div>
        </div>
        {!docPath && (
          <div className="mt-3">
            <input
              type="text"
              placeholder="Enter file path (e.g., docs/new-document.md)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              onChange={(e) => {
                // Update path for new document
                window.history.replaceState({}, '', `/edit/${e.target.value}`)
              }}
            />
          </div>
        )}
      </div>
      
      <div className="flex-1 bg-white" data-color-mode="light">
        <MDEditor
          value={content}
          onChange={(val) => setContent(val || '')}
          preview={previewMode ? 'preview' : 'live'}
          height="100%"
          visibleDragbar={false}
        />
      </div>
    </div>
  )
}