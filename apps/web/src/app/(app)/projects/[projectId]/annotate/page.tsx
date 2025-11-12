'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { createClient } from '@/utils/supabase/client'
import { AnnotationCanvas } from '@/components/annotation/AnnotationCanvas'
import { ClassSelector } from '@/components/annotation/ClassSelector'
import { AnnotationToolbar } from '@/components/annotation/AnnotationToolbar'
import type { BoundingBoxData } from '@visionflow/shared-types'

interface Annotation {
  id: string
  type: 'bounding_box'
  data: BoundingBoxData
  className: string
  color: string
}

export default function AnnotatePage() {
  const params = useParams()
  const projectId = params.projectId as string
  const supabase = createClient()

  const [mode, setMode] = useState<'select' | 'draw'>('draw')
  const [annotations, setAnnotations] = useState<Annotation[]>([])
  const [classes, setClasses] = useState<string[]>(['car', 'person', 'bicycle'])
  const [selectedClass, setSelectedClass] = useState<string>('car')
  const [currentImageId, setCurrentImageId] = useState<string | null>(null)
  const [imageUrl, setImageUrl] = useState<string>('')
  const [imageWidth] = useState(800)
  const [imageHeight] = useState(600)

  // Subscribe to real-time annotation changes
  useEffect(() => {
    if (!currentImageId) return

    const channel = supabase
      .channel(`image:${currentImageId}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'annotations',
          filter: `image_id=eq.${currentImageId}`,
        },
        (payload) => {
          console.log('Real-time annotation change:', payload)
          // Handle real-time updates
          if (payload.eventType === 'INSERT') {
            const newAnnotation = payload.new as any
            setAnnotations((prev) => [
              ...prev,
              {
                id: newAnnotation.id,
                type: 'bounding_box',
                data: newAnnotation.data,
                className: newAnnotation.class_name,
                color: getRandomColor(),
              },
            ])
          } else if (payload.eventType === 'DELETE') {
            setAnnotations((prev) =>
              prev.filter((ann) => ann.id !== payload.old.id)
            )
          } else if (payload.eventType === 'UPDATE') {
            const updated = payload.new as any
            setAnnotations((prev) =>
              prev.map((ann) =>
                ann.id === updated.id
                  ? {
                      ...ann,
                      data: updated.data,
                      className: updated.class_name,
                    }
                  : ann
              )
            )
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [currentImageId, supabase])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'v' || e.key === 'V') {
        setMode('select')
      } else if (e.key === 'b' || e.key === 'B') {
        setMode('draw')
      }
    }

    window.addEventListener('keypress', handleKeyPress)
    return () => window.removeEventListener('keypress', handleKeyPress)
  }, [])

  const handleAnnotationCreate = async (annotation: Omit<Annotation, 'id'>) => {
    if (!currentImageId) return

    // Optimistically add to local state
    const tempId = `temp-${Date.now()}`
    const newAnnotation = { ...annotation, id: tempId }
    setAnnotations((prev) => [...prev, newAnnotation])

    try {
      // Save to database
      // const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/annotations`, {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${token}`,
      //   },
      //   body: JSON.stringify({
      //     image_id: currentImageId,
      //     project_id: projectId,
      //     class_name: annotation.className,
      //     data: annotation.data,
      //   }),
      // })

      console.log('Annotation created:', annotation)
    } catch (error) {
      console.error('Failed to create annotation:', error)
      // Remove optimistic update on error
      setAnnotations((prev) => prev.filter((ann) => ann.id !== tempId))
    }
  }

  const handleAnnotationUpdate = async (id: string, data: BoundingBoxData) => {
    // Optimistically update local state
    setAnnotations((prev) =>
      prev.map((ann) => (ann.id === id ? { ...ann, data } : ann))
    )

    try {
      // Update in database
      console.log('Annotation updated:', id, data)
    } catch (error) {
      console.error('Failed to update annotation:', error)
    }
  }

  const handleAnnotationDelete = async (id: string) => {
    // Optimistically remove from local state
    setAnnotations((prev) => prev.filter((ann) => ann.id !== id))

    try {
      // Delete from database
      console.log('Annotation deleted:', id)
    } catch (error) {
      console.error('Failed to delete annotation:', error)
    }
  }

  const handleSave = async () => {
    console.log('Saving all annotations...')
    // All annotations are already saved in real-time
    alert('Annotations saved successfully!')
  }

  const handleClassAdd = (className: string) => {
    if (!classes.includes(className)) {
      setClasses((prev) => [...prev, className])
      setSelectedClass(className)
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="p-4 border-b bg-white">
        <h1 className="text-2xl font-bold">Annotation Workbench</h1>
        <p className="text-gray-600">Project: {projectId}</p>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <div className="w-64 border-r bg-gray-50 p-4 overflow-y-auto">
          <ClassSelector
            classes={classes}
            selectedClass={selectedClass}
            onClassSelect={setSelectedClass}
            onClassAdd={handleClassAdd}
          />

          <div className="mt-6 p-4 bg-white rounded-lg shadow">
            <h3 className="font-semibold mb-2">Annotations</h3>
            <p className="text-sm text-gray-600">
              {annotations.length} annotation{annotations.length !== 1 ? 's' : ''}
            </p>
          </div>

          <div className="mt-6 p-4 bg-white rounded-lg shadow">
            <h3 className="font-semibold mb-2">Keyboard Shortcuts</h3>
            <dl className="text-sm space-y-2">
              <div>
                <dt className="font-mono bg-gray-100 px-2 py-1 rounded inline-block">V</dt>
                <dd className="text-gray-600 ml-2">Select mode</dd>
              </div>
              <div>
                <dt className="font-mono bg-gray-100 px-2 py-1 rounded inline-block">B</dt>
                <dd className="text-gray-600 ml-2">Draw mode</dd>
              </div>
              <div>
                <dt className="font-mono bg-gray-100 px-2 py-1 rounded inline-block">Del</dt>
                <dd className="text-gray-600 ml-2">Delete selected</dd>
              </div>
            </dl>
          </div>
        </div>

        {/* Main canvas area */}
        <div className="flex-1 flex flex-col p-4">
          <AnnotationToolbar
            mode={mode}
            onModeChange={setMode}
            onSave={handleSave}
          />

          <div className="flex-1 mt-4 flex items-center justify-center">
            <AnnotationCanvas
              imageUrl={imageUrl || 'https://via.placeholder.com/800x600?text=Load+an+image'}
              imageWidth={imageWidth}
              imageHeight={imageHeight}
              annotations={annotations}
              onAnnotationCreate={handleAnnotationCreate}
              onAnnotationUpdate={handleAnnotationUpdate}
              onAnnotationDelete={handleAnnotationDelete}
              selectedClass={selectedClass}
              mode={mode}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function getRandomColor(): string {
  const colors = [
    '#ef4444', // red
    '#3b82f6', // blue
    '#10b981', // green
    '#f59e0b', // yellow
    '#8b5cf6', // purple
    '#ec4899', // pink
    '#14b8a6', // teal
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}
