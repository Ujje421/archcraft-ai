import { create } from 'zustand'

interface DesignState {
  // Current active system
  activeSystemId: string | null
  setActiveSystemId: (id: string | null) => void

  // Complexity level (0-4)
  activeLevel: number
  setActiveLevel: (level: number) => void

  // Panel visibility
  showAiPanel: boolean
  toggleAiPanel: () => void
  showExplorerPanel: boolean
  toggleExplorerPanel: () => void
}

export const useDesignStore = create<DesignState>((set) => ({
  // System
  activeSystemId: null,
  setActiveSystemId: (id) => set({ activeSystemId: id }),

  // Level
  activeLevel: 2,
  setActiveLevel: (level) => set({ activeLevel: Math.max(0, Math.min(4, level)) }),

  // Panels
  showAiPanel: false,
  toggleAiPanel: () => set((s) => ({ showAiPanel: !s.showAiPanel })),
  showExplorerPanel: false,
  toggleExplorerPanel: () => set((s) => ({ showExplorerPanel: !s.showExplorerPanel })),
}))
