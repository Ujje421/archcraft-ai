import { useDesignStore } from '../store/designStore'

const levels = [
  { level: 0, label: 'L0', title: 'Beginner', color: 'bg-accent-green' },
  { level: 1, label: 'L1', title: 'Junior', color: 'bg-brand-400' },
  { level: 2, label: 'L2', title: 'Mid', color: 'bg-brand-500' },
  { level: 3, label: 'L3', title: 'Senior', color: 'bg-accent-amber' },
  { level: 4, label: 'L4', title: 'Principal', color: 'bg-accent-red' },
]

export default function LevelSelector() {
  const activeLevel = useDesignStore((s) => s.activeLevel)
  const setActiveLevel = useDesignStore((s) => s.setActiveLevel)

  return (
    <div className="bg-surface-800/90 backdrop-blur-sm border border-surface-500 rounded-xl p-2 flex items-center gap-1">
      {levels.map(({ level, label, title, color }) => (
        <button
          key={level}
          onClick={() => setActiveLevel(level)}
          title={`${title} (Level ${level})`}
          className={`
            relative px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all
            ${activeLevel === level
              ? 'bg-surface-600 text-white shadow-md'
              : 'text-gray-500 hover:text-gray-300 hover:bg-surface-700'
            }
          `}
        >
          {activeLevel === level && (
            <span className={`absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full ${color}`} />
          )}
          {label}
        </button>
      ))}
    </div>
  )
}
