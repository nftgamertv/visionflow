'use client'

import { useEffect, useRef, useState } from 'react'
import { Stage, Layer, Rect, Image as KonvaImage, Transformer } from 'react-konva'
import Konva from 'konva'
import type { BoundingBoxData } from '@visionflow/shared-types'

interface Annotation {
  id: string
  type: 'bounding_box'
  data: BoundingBoxData
  className: string
  color: string
}

interface AnnotationCanvasProps {
  imageUrl: string
  imageWidth: number
  imageHeight: number
  annotations: Annotation[]
  onAnnotationCreate: (annotation: Omit<Annotation, 'id'>) => void
  onAnnotationUpdate: (id: string, data: BoundingBoxData) => void
  onAnnotationDelete: (id: string) => void
  selectedClass: string
  mode: 'select' | 'draw'
}

export function AnnotationCanvas({
  imageUrl,
  imageWidth,
  imageHeight,
  annotations,
  onAnnotationCreate,
  onAnnotationUpdate,
  onAnnotationDelete,
  selectedClass,
  mode,
}: AnnotationCanvasProps) {
  const [image, setImage] = useState<HTMLImageElement | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [newBox, setNewBox] = useState<BoundingBoxData | null>(null)
  const stageRef = useRef<Konva.Stage>(null)
  const transformerRef = useRef<Konva.Transformer>(null)

  // Load image
  useEffect(() => {
    const img = new window.Image()
    img.src = imageUrl
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      setImage(img)
    }
  }, [imageUrl])

  // Update transformer when selection changes
  useEffect(() => {
    if (!transformerRef.current) return

    if (selectedId) {
      const stage = stageRef.current
      if (!stage) return

      const selectedNode = stage.findOne(`#${selectedId}`)
      if (selectedNode) {
        transformerRef.current.nodes([selectedNode])
        transformerRef.current.getLayer()?.batchDraw()
      }
    } else {
      transformerRef.current.nodes([])
    }
  }, [selectedId])

  const handleMouseDown = (e: Konva.KonvaEventObject<MouseEvent>) => {
    if (mode !== 'draw') return

    const stage = e.target.getStage()
    if (!stage) return

    const pos = stage.getPointerPosition()
    if (!pos) return

    setIsDrawing(true)
    setNewBox({
      type: 'bounding_box',
      x: pos.x,
      y: pos.y,
      width: 0,
      height: 0,
    })
  }

  const handleMouseMove = (e: Konva.KonvaEventObject<MouseEvent>) => {
    if (!isDrawing || !newBox) return

    const stage = e.target.getStage()
    if (!stage) return

    const pos = stage.getPointerPosition()
    if (!pos) return

    setNewBox({
      ...newBox,
      width: pos.x - newBox.x,
      height: pos.y - newBox.y,
    })
  }

  const handleMouseUp = () => {
    if (!isDrawing || !newBox) return

    setIsDrawing(false)

    // Only create annotation if box has meaningful size
    if (Math.abs(newBox.width) > 5 && Math.abs(newBox.height) > 5) {
      // Normalize negative dimensions
      const normalized: BoundingBoxData = {
        type: 'bounding_box',
        x: newBox.width < 0 ? newBox.x + newBox.width : newBox.x,
        y: newBox.height < 0 ? newBox.y + newBox.height : newBox.y,
        width: Math.abs(newBox.width),
        height: Math.abs(newBox.height),
      }

      onAnnotationCreate({
        type: 'bounding_box',
        data: normalized,
        className: selectedClass,
        color: getRandomColor(),
      })
    }

    setNewBox(null)
  }

  const handleBoxClick = (id: string) => {
    if (mode === 'select') {
      setSelectedId(id)
    }
  }

  const handleTransformEnd = (id: string, node: Konva.Rect) => {
    const scaleX = node.scaleX()
    const scaleY = node.scaleY()

    // Reset scale and update width/height instead
    node.scaleX(1)
    node.scaleY(1)

    const updatedData: BoundingBoxData = {
      type: 'bounding_box',
      x: node.x(),
      y: node.y(),
      width: node.width() * scaleX,
      height: node.height() * scaleY,
    }

    onAnnotationUpdate(id, updatedData)
  }

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Delete' && selectedId) {
      onAnnotationDelete(selectedId)
      setSelectedId(null)
    }
  }

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [selectedId])

  return (
    <div className="relative border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-100">
      <Stage
        width={imageWidth}
        height={imageHeight}
        ref={stageRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onClick={(e) => {
          // Deselect when clicking on empty area
          if (e.target === e.target.getStage()) {
            setSelectedId(null)
          }
        }}
      >
        <Layer>
          {/* Background image */}
          {image && (
            <KonvaImage
              image={image}
              width={imageWidth}
              height={imageHeight}
            />
          )}

          {/* Existing annotations */}
          {annotations.map((annotation) => (
            <Rect
              key={annotation.id}
              id={annotation.id}
              x={annotation.data.x}
              y={annotation.data.y}
              width={annotation.data.width}
              height={annotation.data.height}
              stroke={annotation.color}
              strokeWidth={2}
              fill="transparent"
              draggable={mode === 'select'}
              onClick={() => handleBoxClick(annotation.id)}
              onTap={() => handleBoxClick(annotation.id)}
              onDragEnd={(e) => {
                const node = e.target as Konva.Rect
                onAnnotationUpdate(annotation.id, {
                  ...annotation.data,
                  x: node.x(),
                  y: node.y(),
                })
              }}
              onTransformEnd={(e) => {
                const node = e.target as Konva.Rect
                handleTransformEnd(annotation.id, node)
              }}
            />
          ))}

          {/* Drawing new box */}
          {newBox && isDrawing && (
            <Rect
              x={newBox.x}
              y={newBox.y}
              width={newBox.width}
              height={newBox.height}
              stroke="#3b82f6"
              strokeWidth={2}
              fill="rgba(59, 130, 246, 0.1)"
              dash={[5, 5]}
            />
          )}

          {/* Transformer for selected annotation */}
          {mode === 'select' && (
            <Transformer
              ref={transformerRef}
              boundBoxFunc={(oldBox, newBox) => {
                // Limit resize to minimum size
                if (newBox.width < 5 || newBox.height < 5) {
                  return oldBox
                }
                return newBox
              }}
            />
          )}
        </Layer>
      </Stage>

      {/* Instructions overlay */}
      <div className="absolute bottom-4 left-4 bg-black bg-opacity-75 text-white px-4 py-2 rounded text-sm">
        {mode === 'draw' ? (
          <p>Click and drag to draw bounding box</p>
        ) : (
          <p>Click to select | Drag to move | Delete key to remove</p>
        )}
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
