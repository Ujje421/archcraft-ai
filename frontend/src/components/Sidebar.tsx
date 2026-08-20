import { NavLink } from 'react-router-dom'
import { Cpu, LayoutDashboard, BookOpen, Settings, Zap } from 'lucide-react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/library', icon: BookOpen, label: 'Library' },
  { to: '/settings', icon: Settings, label: 'Settings' },
]

export default function Sidebar() {
  return (
    <aside className="w-16 md:w-56 bg-surface-800 border-r border-surface-500 flex flex-col shrink-0">
      {/* Logo */}
      <div className="h-14 flex items-center gap-2.5 px-4 border-b border-surface-500">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
          <Zap className="w-4 h-4 text-white" />
        </div>
        <span className="hidden md:block font-bold text-sm tracking-tight text-white">
          ArchCraft
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-2 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-brand-600/20 text-brand-400'
                  : 'text-gray-400 hover:text-white hover:bg-surface-700'
              }`
            }
          >
            <Icon className="w-4 h-4 shrink-0" />
            <span className="hidden md:block">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-surface-500">
        <div className="hidden md:flex items-center gap-2 px-2">
          <Cpu className="w-3.5 h-3.5 text-gray-500" />
          <span className="text-[11px] text-gray-500 font-mono">v0.1.0</span>
        </div>
      </div>
    </aside>
  )
}
