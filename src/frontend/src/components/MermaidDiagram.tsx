import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

interface MermaidDiagramProps {
  chart: string
}

// Initialize mermaid with configuration
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  themeVariables: {
    primaryColor: '#3b82f6',
    primaryTextColor: '#fff',
    primaryBorderColor: '#2563eb',
    lineColor: '#6b7280',
    secondaryColor: '#f3f4f6',
    tertiaryColor: '#e5e7eb',
    background: '#ffffff',
    mainBkg: '#3b82f6',
    secondBkg: '#f3f4f6',
    tertiaryBkg: '#e5e7eb',
    primaryBorder: '#2563eb',
    secondBorder: '#d1d5db',
    tertiaryBorder: '#9ca3af',
    fontSize: '14px'
  },
  flowchart: {
    curve: 'basis',
    padding: 20,
    htmlLabels: true,
    useMaxWidth: true
  },
  sequence: {
    mirrorActors: false,
    messageMargin: 16,
    boxMargin: 10,
    boxTextMargin: 5,
    noteMargin: 10,
    messageAlign: 'center',
    useMaxWidth: true
  }
})

export default function MermaidDiagram({ chart }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const renderDiagram = async () => {
      if (!containerRef.current || !chart) return

      try {
        // Clear any previous content
        containerRef.current.innerHTML = ''
        setError(null)
        
        // Generate unique ID
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`
        
        // Create container for the diagram
        const div = document.createElement('div')
        div.id = id
        div.textContent = chart
        containerRef.current.appendChild(div)
        
        // Render the diagram
        await mermaid.run({
          nodes: [div],
          suppressErrors: false
        })
      } catch (err) {
        console.error('Mermaid rendering error:', err)
        setError(err instanceof Error ? err.message : 'Failed to render diagram')
      }
    }

    renderDiagram()
  }, [chart])

  if (error) {
    return (
      <div className="my-4 p-4 bg-red-50 border border-red-200 rounded">
        <p className="text-red-600 text-sm">Error rendering diagram:</p>
        <pre className="mt-2 text-xs text-red-500">{error}</pre>
        <details className="mt-2">
          <summary className="text-sm text-gray-600 cursor-pointer">Show source</summary>
          <pre className="mt-2 p-2 bg-gray-100 text-xs overflow-x-auto">{chart}</pre>
        </details>
      </div>
    )
  }

  return (
    <div className="my-4 overflow-x-auto">
      <div ref={containerRef} className="flex justify-center" />
    </div>
  )
}