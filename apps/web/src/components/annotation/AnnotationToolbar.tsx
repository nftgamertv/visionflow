'use client'

interface AnnotationToolbarProps {
  mode: 'select' | 'draw'
  onModeChange: (mode: 'select' | 'draw') => void
  onSave: () => void
  onUndo?: () => void
  onRedo?: () => void
}

export function AnnotationToolbar({
  mode,
  onModeChange,
  onSave,
  onUndo,
  onRedo,
}: AnnotationToolbarProps) {
  return (
    <div className="bg-white rounded-lg shadow p-4 flex items-center gap-4">
      <div className="flex gap-2">
        <button
          onClick={() => onModeChange('select')}
          className={`px-4 py-2 rounded transition-colors ${
            mode === 'select'
              ? 'bg-primary text-white'
              : 'bg-gray-100 hover:bg-gray-200'
          }`}
          title="Select and edit annotations (V)"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
          </svg>
        </button>

        <button
          onClick={() => onModeChange('draw')}
          className={`px-4 py-2 rounded transition-colors ${
            mode === 'draw'
              ? 'bg-primary text-white'
              : 'bg-gray-100 hover:bg-gray-200'
          }`}
          title="Draw bounding box (B)"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z" />
          </svg>
        </button>
      </div>

      <div className="h-6 w-px bg-gray-300" />

      <div className="flex gap-2">
        {onUndo && (
          <button
            onClick={onUndo}
            className="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            title="Undo (Ctrl+Z)"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
            </svg>
          </button>
        )}

        {onRedo && (
          <button
            onClick={onRedo}
            className="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded"
            title="Redo (Ctrl+Y)"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 10H11a8 8 0 00-8 8v2m18-10l-6 6m6-6l-6-6" />
            </svg>
          </button>
        )}
      </div>

      <div className="ml-auto">
        <button
          onClick={onSave}
          className="px-6 py-2 bg-primary text-white rounded hover:bg-primary/90 font-medium"
        >
          Save Annotations
        </button>
      </div>
    </div>
  )
}
