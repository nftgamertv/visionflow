'use client'

import { useState } from 'react'

interface ClassSelectorProps {
  classes: string[]
  selectedClass: string
  onClassSelect: (className: string) => void
  onClassAdd: (className: string) => void
}

export function ClassSelector({
  classes,
  selectedClass,
  onClassSelect,
  onClassAdd,
}: ClassSelectorProps) {
  const [isAdding, setIsAdding] = useState(false)
  const [newClassName, setNewClassName] = useState('')

  const handleAdd = () => {
    if (newClassName.trim()) {
      onClassAdd(newClassName.trim())
      setNewClassName('')
      setIsAdding(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-semibold mb-4">Classes</h3>

      <div className="space-y-2">
        {classes.map((className) => (
          <button
            key={className}
            onClick={() => onClassSelect(className)}
            className={`w-full text-left px-3 py-2 rounded transition-colors ${
              selectedClass === className
                ? 'bg-primary text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            {className}
          </button>
        ))}

        {isAdding ? (
          <div className="flex gap-2">
            <input
              type="text"
              value={newClassName}
              onChange={(e) => setNewClassName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
              placeholder="Class name"
              className="flex-1 px-3 py-2 border rounded"
              autoFocus
            />
            <button
              onClick={handleAdd}
              className="px-3 py-2 bg-primary text-white rounded hover:bg-primary/90"
            >
              Add
            </button>
            <button
              onClick={() => {
                setIsAdding(false)
                setNewClassName('')
              }}
              className="px-3 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            onClick={() => setIsAdding(true)}
            className="w-full px-3 py-2 border-2 border-dashed border-gray-300 rounded hover:border-gray-400 text-gray-600"
          >
            + Add Class
          </button>
        )}
      </div>
    </div>
  )
}
