# 05 — Frontend Architecture

> React + TypeScript + React Flow + Tailwind CSS

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Framework | React | 18+ |
| Language | TypeScript | 5+ |
| Build Tool | Vite | 5+ |
| Canvas | React Flow | 11+ |
| Styling | Tailwind CSS | 4 |
| State | Zustand | 4+ |
| Routing | React Router | 6+ |
| HTTP | Axios | 1+ |
| Icons | Lucide React | Latest |
| Fonts | Google Fonts (Inter) | — |
| Animations | Framer Motion | 10+ |

---

## Project Structure

```
frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── main.tsx                    # Entry point
│   ├── App.tsx                     # Root component + routing
│   │
│   ├── api/                        # API client layer
│   │   ├── client.ts               # Axios instance, interceptors
│   │   ├── systems.ts              # System CRUD endpoints
│   │   ├── ai.ts                   # AI assistant endpoints
│   │   ├── components.ts           # Component knowledge base
│   │   └── types.ts                # API response types
│   │
│   ├── store/                      # Zustand state management
│   │   ├── useSystemStore.ts       # Current system design state
│   │   ├── useCanvasStore.ts       # Canvas (React Flow) state
│   │   ├── useChatStore.ts         # AI chat messages
│   │   ├── useUIStore.ts           # UI state (panels, modals, level)
│   │   └── useLevelStore.ts        # Active design level (0-4)
│   │
│   ├── components/                 # Shared components
│   │   ├── ui/                     # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Panel.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Slider.tsx
│   │   │   ├── Tabs.tsx
│   │   │   └── Tooltip.tsx
│   │   │
│   │   ├── canvas/                 # Architecture canvas components
│   │   │   ├── ArchitectureCanvas.tsx     # Main React Flow canvas
│   │   │   ├── CanvasToolbar.tsx          # Top toolbar (zoom, layout, export)
│   │   │   ├── ComponentPalette.tsx       # Left sidebar: draggable components
│   │   │   ├── MiniMap.tsx                # Canvas minimap
│   │   │   ├── ConnectionLine.tsx         # Custom edge rendering
│   │   │   └── nodes/                     # Custom React Flow nodes
│   │   │       ├── BaseNode.tsx           # Base node wrapper
│   │   │       ├── ServiceNode.tsx        # Application service node
│   │   │       ├── DatabaseNode.tsx       # Database node
│   │   │       ├── CacheNode.tsx          # Cache (Redis) node
│   │   │       ├── QueueNode.tsx          # Message queue node
│   │   │       ├── StorageNode.tsx        # Object storage node
│   │   │       ├── LoadBalancerNode.tsx   # Load balancer node
│   │   │       ├── CDNNode.tsx            # CDN node
│   │   │       ├── APIGatewayNode.tsx     # API gateway node
│   │   │       ├── ClientNode.tsx         # User/client node
│   │   │       ├── MonitoringNode.tsx     # Observability node
│   │   │       └── GroupNode.tsx          # Logical grouping node
│   │   │
│   │   ├── explorer/               # Component explorer panel
│   │   │   ├── ComponentExplorer.tsx      # Main explorer panel
│   │   │   ├── ComponentOverview.tsx      # Why, what, alternatives
│   │   │   ├── ComponentScaling.tsx       # Scaling info
│   │   │   ├── ComponentFailure.tsx       # Failure scenarios
│   │   │   ├── ComponentCost.tsx          # Cost info
│   │   │   └── ComponentInterview.tsx     # Interview questions
│   │   │
│   │   ├── chat/                   # AI assistant panel
│   │   │   ├── ChatPanel.tsx              # Main chat container
│   │   │   ├── ChatMessage.tsx            # Single message
│   │   │   ├── ChatInput.tsx              # Input with send button
│   │   │   ├── SuggestionChips.tsx        # Quick action suggestions
│   │   │   └── StreamingResponse.tsx      # Streaming AI response
│   │   │
│   │   ├── designer/               # System design generator
│   │   │   ├── DesignGenerator.tsx        # Generation form
│   │   │   ├── ParameterForm.tsx          # Users, DAU, budget, etc.
│   │   │   ├── LevelSelector.tsx          # Level 0-4 selector
│   │   │   └── GenerationProgress.tsx     # Progress during generation
│   │   │
│   │   ├── schema/                 # Schema section renderers
│   │   │   ├── SchemaPanel.tsx            # Container with tabs
│   │   │   ├── RequirementsView.tsx
│   │   │   ├── CapacityView.tsx
│   │   │   ├── APIDesignView.tsx
│   │   │   ├── DataModelView.tsx
│   │   │   ├── DataFlowView.tsx
│   │   │   ├── ScalingView.tsx
│   │   │   ├── CostView.tsx
│   │   │   ├── TradeoffsView.tsx
│   │   │   └── InterviewView.tsx
│   │   │
│   │   └── layout/                 # Page layout
│   │       ├── AppLayout.tsx              # Main app shell
│   │       ├── Sidebar.tsx                # Left navigation
│   │       ├── Header.tsx                 # Top bar
│   │       └── SplitPane.tsx              # Resizable split layout
│   │
│   ├── pages/                      # Route pages
│   │   ├── DashboardPage.tsx       # Home / system list
│   │   ├── DesignPage.tsx          # Main design workspace
│   │   ├── GeneratePage.tsx        # New system generator
│   │   ├── LibraryPage.tsx         # Pre-built system designs
│   │   ├── KnowledgePage.tsx       # Component knowledge base
│   │   └── InterviewPage.tsx       # Interview mode (V2)
│   │
│   ├── hooks/                      # Custom React hooks
│   │   ├── useArchitectureGraph.ts # Graph manipulation
│   │   ├── useAIAssistant.ts       # AI chat interaction
│   │   ├── useWebSocket.ts         # WebSocket connection
│   │   ├── useLevelFilter.ts       # Filter nodes by level
│   │   ├── useAutoLayout.ts        # Auto-layout with dagre
│   │   └── useExport.ts            # Export functionality
│   │
│   ├── utils/                      # Utility functions
│   │   ├── graphUtils.ts           # Graph manipulation helpers
│   │   ├── layoutUtils.ts          # Dagre auto-layout
│   │   ├── exportUtils.ts          # PNG/SVG/JSON export
│   │   ├── levelUtils.ts           # Level filtering
│   │   └── formatUtils.ts          # Number/text formatting
│   │
│   ├── types/                      # TypeScript type definitions
│   │   ├── system.ts               # System design types
│   │   ├── graph.ts                # Architecture graph types
│   │   ├── component.ts            # Component knowledge types
│   │   ├── chat.ts                 # Chat message types
│   │   └── schema.ts               # 26-section schema types
│   │
│   └── styles/
│       └── index.css               # Global styles + Tailwind
│
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── vite.config.ts
```

---

## Core Architecture Pattern

### State Management (Zustand)

```typescript
// store/useSystemStore.ts
interface SystemState {
  // Current system
  currentSystem: SystemDesign | null;
  
  // Architecture graph (source of truth)
  nodes: ArchNode[];
  connections: ArchConnection[];
  
  // Schema sections
  sections: Record<SectionName, SectionData>;
  
  // Active level
  activeLevel: DesignLevel; // 0 | 1 | 2 | 3 | 4
  
  // Version history
  versions: SystemVersion[];
  currentVersion: number;
  
  // Actions
  setSystem: (system: SystemDesign) => void;
  addNode: (node: ArchNode) => void;
  removeNode: (nodeId: string) => void;
  addConnection: (conn: ArchConnection) => void;
  updateNodeTechnology: (nodeId: string, tech: string) => void;
  setLevel: (level: DesignLevel) => void;
  applyAIDiff: (diff: GraphDiff) => void;
}
```

### Architecture Graph ↔ React Flow Mapping

```typescript
// hooks/useArchitectureGraph.ts

// Convert our domain model to React Flow nodes
function toReactFlowNodes(
  nodes: ArchNode[], 
  activeLevel: DesignLevel
): ReactFlowNode[] {
  return nodes
    .filter(n => n.min_level <= activeLevel)  // Level filtering
    .map(node => ({
      id: node.id,
      type: getNodeType(node.type),  // Maps to custom node component
      position: node.position,
      data: {
        label: node.label,
        technology: node.technology,
        type: node.type,
        metadata: node.metadata,
      },
    }));
}

// Convert our connections to React Flow edges
function toReactFlowEdges(
  connections: ArchConnection[],
  visibleNodeIds: Set<string>
): ReactFlowEdge[] {
  return connections
    .filter(c => visibleNodeIds.has(c.source) && visibleNodeIds.has(c.target))
    .map(conn => ({
      id: `${conn.source}-${conn.target}`,
      source: conn.source,
      target: conn.target,
      label: conn.label,
      animated: conn.protocol === 'async',
      style: getEdgeStyle(conn),
    }));
}
```

---

## Custom Node Components

Each infrastructure component renders as a custom React Flow node:

```typescript
// components/canvas/nodes/DatabaseNode.tsx

interface DatabaseNodeProps {
  data: {
    label: string;          // "PostgreSQL"
    technology: string;     // "PostgreSQL"
    type: string;          // "database"
    metadata: {
      replicas?: number;
      sharded?: boolean;
      purpose?: string;
    };
  };
}

function DatabaseNode({ data }: DatabaseNodeProps) {
  return (
    <div className="node-database">
      <div className="node-icon">🗄️</div>
      <div className="node-label">{data.label}</div>
      <div className="node-tech">{data.technology}</div>
      {data.metadata.replicas && (
        <div className="node-badge">×{data.metadata.replicas}</div>
      )}
      {data.metadata.sharded && (
        <div className="node-badge">Sharded</div>
      )}
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
```

### Node Type Registry

```typescript
const nodeTypes: Record<string, ComponentType> = {
  service: ServiceNode,
  database: DatabaseNode,
  cache: CacheNode,
  message_queue: QueueNode,
  object_storage: StorageNode,
  load_balancer: LoadBalancerNode,
  cdn: CDNNode,
  api_gateway: APIGatewayNode,
  client: ClientNode,
  monitoring: MonitoringNode,
  group: GroupNode,
};
```

---

## Page Layout: Design Workspace

```
┌──────────────────────────────────────────────────────────────┐
│ Header: System Name    │ Level [0-4]    │ AI ▼  │ Export ▼  │
├────────────┬─────────────────────────────────┬───────────────┤
│            │                                 │               │
│ Component  │                                 │  Component    │
│ Palette    │     Architecture Canvas         │  Explorer     │
│            │     (React Flow)                │  Panel        │
│ □ Service  │                                 │               │
│ □ Database │     [Nodes + Edges]             │  Selected:    │
│ □ Cache    │                                 │  PostgreSQL   │
│ □ Queue    │                                 │               │
│ □ Storage  │                                 │  - Why?       │
│ □ CDN      │                                 │  - Scaling    │
│ □ LB       │                                 │  - Failures   │
│ □ Gateway  │                                 │  - Cost       │
│            │                                 │  - Interview  │
│            │                                 │               │
├────────────┴─────────────────────────────────┴───────────────┤
│ Schema Tabs: Requirements │ Capacity │ Data Model │ APIs │..│
├──────────────────────────────────────────────────────────────┤
│ AI Assistant Chat Panel                                      │
│ > "Why did you choose PostgreSQL?"                           │
│ AI: "PostgreSQL was chosen because..."                       │
│ [input: Ask about architecture...]                           │
└──────────────────────────────────────────────────────────────┘
```

The layout uses resizable split panes:
- **Left**: Component palette (collapsible)
- **Center**: Architecture canvas (main workspace)
- **Right**: Component explorer (collapsible)
- **Bottom-top**: Schema section tabs
- **Bottom**: AI chat panel (collapsible)

---

## Interaction Flows

### 1. Drag Component from Palette to Canvas

```
User drags "Redis" from palette
  → onDrop event on canvas
  → Create new ArchNode { id: uuid(), type: "cache", technology: "Redis", min_level: 2 }
  → Add to Zustand store
  → React Flow re-renders with new node
  → POST /api/v1/systems/{id}/nodes (persist)
```

### 2. Click Component → Explorer Panel Opens

```
User clicks "PostgreSQL" node
  → onNodeClick event
  → Set selectedNodeId in UI store
  → Explorer panel fetches component knowledge
  → GET /api/v1/components/postgresql
  → Render detail tabs
```

### 3. AI Modifies Canvas

```
User types: "Add Kafka between API and Database"
  → POST /api/v1/systems/{id}/ai/command
  → Backend returns GraphDiff: { add_nodes: [...], add_connections: [...], remove_connections: [...] }
  → applyAIDiff(diff) in Zustand store
  → Canvas animates: new nodes fade in, old connections fade out, new connections draw
```

### 4. Switch Design Level

```
User moves slider from Level 1 → Level 3
  → setLevel(3) in Zustand store
  → useLevelFilter hook recalculates visible nodes
  → Nodes with min_level > 3 fade out
  → Nodes with min_level <= 3 fade in
  → Schema tabs update to show Level 3 sections
  → Auto-relayout if needed
```

---

## Auto-Layout Engine

Uses **dagre** for hierarchical graph layout:

```typescript
// utils/layoutUtils.ts
import dagre from 'dagre';

function autoLayout(nodes: ArchNode[], connections: ArchConnection[]): PositionMap {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ 
    rankdir: 'TB',      // Top to bottom
    nodesep: 80,        // Horizontal spacing
    ranksep: 100,       // Vertical spacing
    marginx: 40,
    marginy: 40,
  });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach(n => g.setNode(n.id, { width: 180, height: 80 }));
  connections.forEach(c => g.setEdge(c.source, c.target));

  dagre.layout(g);

  const positions: PositionMap = {};
  g.nodes().forEach(id => {
    const node = g.node(id);
    positions[id] = { x: node.x - 90, y: node.y - 40 };
  });
  return positions;
}
```

---

## Theming

### Design System Tokens

```css
/* Dark mode primary palette */
:root {
  --bg-primary: #0f0f14;
  --bg-secondary: #1a1a24;
  --bg-tertiary: #24243a;
  --bg-glass: rgba(255, 255, 255, 0.04);
  
  --text-primary: #e8e8f0;
  --text-secondary: #9898b4;
  --text-muted: #5a5a7a;
  
  --accent-primary: #6366f1;     /* Indigo */
  --accent-secondary: #8b5cf6;   /* Violet */
  --accent-success: #22c55e;
  --accent-warning: #f59e0b;
  --accent-danger: #ef4444;
  
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-active: rgba(99, 102, 241, 0.5);
  
  --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
}
```

### Node Styling by Type

```css
.node-service    { border-color: var(--accent-primary); }
.node-database   { border-color: #3b82f6; }   /* Blue */
.node-cache      { border-color: #ef4444; }   /* Red — Redis */
.node-queue      { border-color: #f59e0b; }   /* Amber — Kafka */
.node-storage    { border-color: #22c55e; }   /* Green — S3 */
.node-cdn        { border-color: #8b5cf6; }   /* Violet */
.node-lb         { border-color: #06b6d4; }   /* Cyan */
.node-gateway    { border-color: #ec4899; }   /* Pink */
```

---

## Responsive Strategy

| Breakpoint | Layout |
|---|---|
| Desktop (1280px+) | Full layout: palette + canvas + explorer + chat |
| Laptop (1024px) | Palette collapsed to icons, explorer as overlay |
| Tablet (768px) | Canvas only, panels as modals |
| Mobile (< 768px) | View-only mode, no editing |

---

## Related Documents

- [04-architecture-overview.md](./04-architecture-overview.md) — System context
- [13-canvas-architecture.md](./13-canvas-architecture.md) — Canvas deep dive
- [06-backend-architecture.md](./06-backend-architecture.md) — API endpoints the frontend calls
