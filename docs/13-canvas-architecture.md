# 13 — Canvas Architecture

> React Flow interactive architecture canvas — the visual heart of the platform.

---

## Canvas Overview

The canvas is the **primary workspace** where users visualize, build, and modify system architectures. It's built on **React Flow** and tightly integrated with the Zustand state store.

```
┌──────────────────────────────────────────────────────────────┐
│ ┌─ Toolbar ────────────────────────────────────────────────┐ │
│ │ 🔍 Zoom │ 📐 Layout │ ↩️ Undo │ ↪️ Redo │ 📸 Export │  │ │
│ └──────────────────────────────────────────────────────────┘ │
│ ┌── Palette ──┐ ┌── Canvas ─────────────────────────────┐   │
│ │             │ │                                       │   │
│ │ ⚖️ LB      │ │    ┌──────────┐                       │   │
│ │ 🚪 Gateway  │ │    │  Users   │                       │   │
│ │ 🖥️ Service  │ │    └────┬─────┘                       │   │
│ │ 🐘 Postgres │ │         │                             │   │
│ │ 🔴 Redis    │ │    ┌────▼─────┐                       │   │
│ │ 📨 Kafka    │ │    │   CDN    │                       │   │
│ │ 🪣 S3       │ │    └────┬─────┘                       │   │
│ │ 🌐 CDN      │ │         │                             │   │
│ │ 📊 Monitor  │ │    ┌────▼─────┐                       │   │
│ │             │ │    │    LB    │                       │   │
│ │ ─── Groups  │ │    └────┬─────┘                       │   │
│ │ □ Custom    │ │    ┌────┴────┬────────┐               │   │
│ │             │ │ ┌──▼───┐ ┌──▼───┐ ┌──▼───┐           │   │
│ │             │ │ │ API  │ │Video │ │ User │           │   │
│ │             │ │ │ Svc  │ │ Svc  │ │ Svc  │           │   │
│ │             │ │ └──┬───┘ └──┬───┘ └──┬───┘           │   │
│ │             │ │    │        │        │               │   │
│ │             │ │ ┌──▼───┐ ┌──▼──┐ ┌──▼───┐           │   │
│ │             │ │ │ PG   │ │ S3  │ │Redis │           │   │
│ │             │ │ └──────┘ └─────┘ └──────┘           │   │
│ │             │ │                                       │   │
│ │             │ │  ┌─ MiniMap ──┐                       │   │
│ │             │ │  │  [·····]   │                       │   │
│ │             │ │  └────────────┘                       │   │
│ └─────────────┘ └───────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Custom Node Design

Every node is a custom React Flow component with consistent styling:

```
┌─────────────────────────────┐
│  🐘                         │  ← Icon (per type)
│  PostgreSQL                 │  ← Technology label
│  ─────────────────────────  │
│  Primary Database           │  ← Role/purpose label
│  ×5 replicas    Sharded     │  ← Metadata badges
└─────────────────────────────┘
     ▲ (target handle)
     ▼ (source handle)
```

### Node States

```css
/* Default */
.arch-node {
  background: var(--bg-secondary);
  border: 1.5px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  min-width: 160px;
  transition: all 0.2s ease;
}

/* Hover */
.arch-node:hover {
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
}

/* Selected */
.arch-node.selected {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3);
}

/* AI-highlighted (bottleneck warning) */
.arch-node.warning {
  border-color: var(--accent-warning);
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
}

/* Level fade-in animation */
.arch-node.entering {
  animation: nodeEnter 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes nodeEnter {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

/* Level fade-out */
.arch-node.exiting {
  animation: nodeExit 0.3s ease-out forwards;
}

@keyframes nodeExit {
  to { opacity: 0; transform: scale(0.8); }
}
```

---

## Connection (Edge) Types

```typescript
const edgeStyles = {
  sync: {
    stroke: '#6366f1',        // Indigo — synchronous calls
    strokeWidth: 2,
    animated: false,
  },
  async: {
    stroke: '#f59e0b',        // Amber — async/event-driven
    strokeWidth: 2,
    animated: true,           // Animated dashes
    strokeDasharray: '5 5',
  },
  data: {
    stroke: '#22c55e',        // Green — data flow
    strokeWidth: 1.5,
    animated: false,
  },
  replication: {
    stroke: '#8b5cf6',        // Violet — replication
    strokeWidth: 1,
    animated: true,
    strokeDasharray: '3 3',
  },
};
```

Edge labels show the protocol or purpose:

```
  API Service ──── HTTPS ────→ Database
  API Service ═══ async ═══→ Kafka
  Primary ------repl------→ Replica
```

---

## Drag and Drop from Palette

```typescript
// components/canvas/ComponentPalette.tsx

function ComponentPalette() {
  const components = [
    { type: 'load_balancer', label: 'Load Balancer', icon: '⚖️' },
    { type: 'api_gateway', label: 'API Gateway', icon: '🚪' },
    { type: 'service', label: 'Service', icon: '🖥️' },
    { type: 'database', label: 'Database', icon: '🐘' },
    { type: 'cache', label: 'Cache', icon: '🔴' },
    { type: 'message_queue', label: 'Message Queue', icon: '📨' },
    { type: 'object_storage', label: 'Storage', icon: '🪣' },
    { type: 'cdn', label: 'CDN', icon: '🌐' },
    { type: 'monitoring', label: 'Monitoring', icon: '📊' },
    { type: 'worker', label: 'Worker', icon: '👷' },
  ];

  const onDragStart = (event: DragEvent, componentType: string) => {
    event.dataTransfer.setData('application/reactflow', componentType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className="palette">
      <h3>Components</h3>
      {components.map(comp => (
        <div
          key={comp.type}
          className="palette-item"
          draggable
          onDragStart={(e) => onDragStart(e, comp.type)}
        >
          <span className="palette-icon">{comp.icon}</span>
          <span className="palette-label">{comp.label}</span>
        </div>
      ))}
    </div>
  );
}
```

### Drop Handler

```typescript
// components/canvas/ArchitectureCanvas.tsx

const onDrop = useCallback((event: DragEvent) => {
  event.preventDefault();
  
  const type = event.dataTransfer.getData('application/reactflow');
  if (!type) return;
  
  const position = reactFlowInstance.screenToFlowPosition({
    x: event.clientX,
    y: event.clientY,
  });
  
  // Open technology selector modal
  openTechSelector(type, position);
}, []);

// After user selects technology (e.g., "PostgreSQL" for type "database")
const addComponent = (type: string, technology: string, position: XYPosition) => {
  const nodeId = `${type}_${nanoid(6)}`;
  
  const newNode: ArchNode = {
    id: nodeId,
    type,
    technology,
    label: technology,
    min_level: getDefaultLevel(type),
    position,
    metadata: {},
  };
  
  // Add to store → triggers React Flow re-render
  addNode(newNode);
  
  // Persist to backend
  api.addNode(systemId, newNode);
};
```

---

## Level Transition Animation

When the user switches levels, nodes animate in/out:

```typescript
// hooks/useLevelFilter.ts

function useLevelFilter(nodes: ArchNode[], level: DesignLevel) {
  const [displayNodes, setDisplayNodes] = useState<DisplayNode[]>([]);
  const prevLevel = useRef(level);
  
  useEffect(() => {
    const isLevelUp = level > prevLevel.current;
    
    const visible = nodes.filter(n => n.min_level <= level);
    const hidden = nodes.filter(n => n.min_level > level);
    
    setDisplayNodes(prev => {
      const next: DisplayNode[] = [];
      
      for (const node of visible) {
        const existed = prev.find(p => p.id === node.id);
        if (existed) {
          next.push({ ...node, state: 'stable' });
        } else {
          // New node — animate in
          next.push({ ...node, state: 'entering' });
        }
      }
      
      if (!isLevelUp) {
        // Nodes being removed — animate out
        for (const node of hidden) {
          const existed = prev.find(p => p.id === node.id);
          if (existed) {
            next.push({ ...node, state: 'exiting' });
            // Remove after animation
            setTimeout(() => removeDisplayNode(node.id), 300);
          }
        }
      }
      
      return next;
    });
    
    prevLevel.current = level;
  }, [level, nodes]);
  
  return displayNodes;
}
```

---

## Context Menu

Right-clicking a node shows a context menu:

```
┌──────────────────────┐
│ 🔍 Explore Component │
│ 🤖 Ask AI About This │
│ ✏️  Rename            │
│ 🔄 Change Technology  │
│ 📋 Duplicate          │
│ 🔗 Connect To...      │
│ 📝 Add Note           │
│ ──────────────────── │
│ 🗑️  Delete            │
└──────────────────────┘
```

---

## AI-Driven Canvas Modifications

When the AI modifies the canvas, changes are animated:

1. **New nodes**: Appear with scale-up + fade-in animation
2. **Removed nodes**: Scale-down + fade-out, then removed
3. **New connections**: Draw from source to target with path animation
4. **Removed connections**: Fade out
5. **Changed technology**: Node flashes briefly, label updates

```typescript
function applyAIDiff(diff: GraphDiff) {
  // Phase 1: Remove old connections (0ms)
  for (const conn of diff.remove_connections) {
    markConnectionExiting(conn.id);
  }
  
  // Phase 2: Remove old nodes (300ms delay)
  setTimeout(() => {
    for (const nodeId of diff.remove_nodes) {
      markNodeExiting(nodeId);
    }
  }, 300);
  
  // Phase 3: Add new nodes (600ms delay)
  setTimeout(() => {
    for (const node of diff.add_nodes) {
      addNodeWithAnimation(node); // Enters with scale-up
    }
  }, 600);
  
  // Phase 4: Add new connections (900ms delay)
  setTimeout(() => {
    for (const conn of diff.add_connections) {
      addConnectionWithAnimation(conn); // Path draws from source to target
    }
  }, 900);
  
  // Phase 5: Auto-relayout if needed (1200ms delay)
  setTimeout(() => {
    if (diff.add_nodes.length > 2) {
      autoLayout();
    }
  }, 1200);
}
```

---

## Export

```typescript
// hooks/useExport.ts

function useExport() {
  const exportPNG = async () => {
    const canvas = document.querySelector('.react-flow__viewport');
    const blob = await toBlob(canvas, { backgroundColor: '#0f0f14' });
    saveAs(blob, `${systemName}_architecture.png`);
  };
  
  const exportSVG = async () => {
    const svg = await toSvg(canvas);
    saveAs(new Blob([svg]), `${systemName}_architecture.svg`);
  };
  
  const exportJSON = () => {
    const graph = { nodes, connections, metadata: systemMeta };
    saveAs(new Blob([JSON.stringify(graph, null, 2)]), `${systemName}.json`);
  };
  
  const exportMermaid = () => {
    const mermaid = graphToMermaid(nodes, connections);
    saveAs(new Blob([mermaid]), `${systemName}.mmd`);
  };
  
  return { exportPNG, exportSVG, exportJSON, exportMermaid };
}
```

---

## Related Documents

- [05-frontend-architecture.md](./05-frontend-architecture.md) — Frontend component structure
- [03-design-levels.md](./03-design-levels.md) — Level transition rules
- [16-export-system.md](./16-export-system.md) — Full export capabilities
