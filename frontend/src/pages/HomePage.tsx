import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Zap, ArrowRight, Layers, Bot, Search, BarChart3 } from 'lucide-react'

const features = [
  {
    icon: Zap,
    title: 'AI System Generator',
    description: 'Input a prompt like "Design YouTube" and get a complete architecture.',
    color: 'text-amber-400',
    bg: 'bg-amber-400/10',
  },
  {
    icon: Layers,
    title: 'Interactive Canvas',
    description: 'Visual architecture canvas with drag-and-drop components.',
    color: 'text-brand-400',
    bg: 'bg-brand-400/10',
  },
  {
    icon: Bot,
    title: 'AI Assistant',
    description: '"Add Kafka for async processing" — AI modifies your architecture.',
    color: 'text-accent-green',
    bg: 'bg-accent-green/10',
  },
  {
    icon: Search,
    title: 'Component Explorer',
    description: 'Click any component to deep-dive: scaling, failures, cost, alternatives.',
    color: 'text-accent-purple',
    bg: 'bg-accent-purple/10',
  },
  {
    icon: BarChart3,
    title: 'Capacity Engine',
    description: 'Deterministic capacity calculations — traffic, storage, bandwidth.',
    color: 'text-accent-cyan',
    bg: 'bg-accent-cyan/10',
  },
]

export default function HomePage() {
  const [prompt, setPrompt] = useState('')
  const navigate = useNavigate()

  const handleGenerate = () => {
    if (!prompt.trim()) return
    // In MVP, this will call the API and navigate to the canvas
    console.log('Generating:', prompt)
    navigate('/design/demo')
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center px-6 py-20">
        <div className="max-w-3xl w-full text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-600/10 border border-brand-600/20 text-brand-400 text-xs font-semibold mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-green animate-pulse" />
            AI-Powered System Design
          </div>

          {/* Title */}
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white mb-4 leading-tight">
            Design systems.{' '}
            <span className="bg-gradient-to-r from-brand-400 to-accent-cyan bg-clip-text text-transparent">
              Understand trade-offs.
            </span>
          </h1>
          <p className="text-gray-400 text-lg mb-10 max-w-xl mx-auto leading-relaxed">
            AI-native architecture platform. Go from problem statement to interactive
            visual canvas with capacity calculations and component deep-dives.
          </p>

          {/* Prompt Input */}
          <div className="relative max-w-xl mx-auto">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
              placeholder='Try "Design YouTube for 100M users"'
              className="w-full px-5 py-4 pr-36 bg-surface-700 border border-surface-500 rounded-xl text-white placeholder:text-gray-500 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500/30 transition-all"
            />
            <button
              onClick={handleGenerate}
              disabled={!prompt.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 px-5 py-2 bg-brand-600 hover:bg-brand-700 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg text-sm font-semibold text-white flex items-center gap-2 transition-colors"
            >
              Generate
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Quick suggestions */}
          <div className="flex flex-wrap justify-center gap-2 mt-4">
            {['URL Shortener', 'Instagram', 'Uber', 'Chat App', 'E-commerce'].map((s) => (
              <button
                key={s}
                onClick={() => setPrompt(`Design ${s}`)}
                className="px-3 py-1 text-xs text-gray-500 hover:text-gray-300 bg-surface-700/50 hover:bg-surface-700 border border-surface-500/50 rounded-full transition-colors"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="px-6 py-16 border-t border-surface-700">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-xl font-bold text-white mb-8 text-center">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {features.map(({ icon: Icon, title, description, color, bg }) => (
              <div
                key={title}
                className="p-5 bg-surface-800 border border-surface-500/50 rounded-xl hover:border-surface-400 transition-colors group"
              >
                <div className={`w-9 h-9 rounded-lg ${bg} flex items-center justify-center mb-3`}>
                  <Icon className={`w-4.5 h-4.5 ${color}`} />
                </div>
                <h3 className="font-semibold text-sm text-white mb-1.5">{title}</h3>
                <p className="text-xs text-gray-400 leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
