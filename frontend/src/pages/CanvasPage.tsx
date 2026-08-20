import { useCallback, useMemo } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  BackgroundVariant,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { useParams } from 'react-router-dom'
import { useDesignStore } from '../store/designStore'
import LevelSelector from '../components/LevelSelector'

// ── Demo nodes for initial prototype ──
const initialNodes: Node[] = [
  {
    id: 'clients',
    type: 'default',
    position: { x: 400, y: 0 },
    data: { label: '👥 Clients (Web/Mobile)' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #313147', borderRadius: '12px', padding: '12px 20px', fontSize: '13px', fontWeight: 600 },
  },
  {
    id: 'cdn',
    type: 'default',
    position: { x: 400, y: 100 },
    data: { label: '🌐 CDN (CloudFront)' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #313147', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
  {
    id: 'lb',
    type: 'default',
    position: { x: 400, y: 200 },
    data: { label: '⚖️ Load Balancer (NGINX)' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #313147', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
  {
    id: 'api',
    type: 'default',
    position: { x: 400, y: 320 },
    data: { label: '🖥️ API Server' },
    style: { background: '#181825', color: '#fff', border: '1px solid #2a91ff', borderRadius: '12px', padding: '12px 20px', fontSize: '13px', fontWeight: 600 },
  },
  {
    id: 'redis',
    type: 'default',
    position: { x: 150, y: 320 },
    data: { label: '🔴 Redis Cache' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #ef4444', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
  {
    id: 'postgres',
    type: 'default',
    position: { x: 650, y: 320 },
    data: { label: '🐘 PostgreSQL' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #10b981', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
  {
    id: 'kafka',
    type: 'default',
    position: { x: 400, y: 460 },
    data: { label: '📨 Kafka (Event Bus)' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #f59e0b', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
  {
    id: 's3',
    type: 'default',
    position: { x: 650, y: 460 },
    data: { label: '🪣 S3 (Object Storage)' },
    style: { background: '#1e1e2e', color: '#fff', border: '1px solid #8b5cf6', borderRadius: '12px', padding: '12px 20px', fontSize: '13px' },
  },
]

const initialEdges: Edge[] = [
  { id: 'e1', source: 'clients', target: 'cdn', animated: true, style: { stroke: '#313147' } },
  { id: 'e2', source: 'cdn', target: 'lb', style: { stroke: '#313147' } },
  { id: 'e3', source: 'lb', target: 'api', style: { stroke: '#2a91ff' } },
  { id: 'e4', source: 'api', target: 'redis', label: 'Cache', style: { stroke: '#ef4444' }, labelStyle: { fill: '#999', fontSize: 10 } },
  { id: 'e5', source: 'api', target: 'postgres', label: 'Read/Write', style: { stroke: '#10b981' }, labelStyle: { fill: '#999', fontSize: 10 } },
  { id: 'e6', source: 'api', target: 'kafka', label: 'Events', animated: true, style: { stroke: '#f59e0b' }, labelStyle: { fill: '#999', fontSize: 10 } },
  { id: 'e7', source: 'api', target: 's3', label: 'Media', style: { stroke: '#8b5cf6' }, labelStyle: { fill: '#999', fontSize: 10 } },
]

export default function CanvasPage() {
  const { id } = useParams()
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const level = useDesignStore((s) => s.activeLevel)

  return (
    <div className="h-screen w-full relative">
      {/* Level Selector (top-right) */}
      <div className="absolute top-4 right-4 z-10">
        <LevelSelector />
      </div>

      {/* System title (top-left) */}
      <div className="absolute top-4 left-4 z-10">
        <div className="bg-surface-800/90 backdrop-blur-sm border border-surface-500 rounded-lg px-4 py-2">
          <h2 className="text-sm font-semibold text-white">Demo Architecture</h2>
          <p className="text-[11px] text-gray-500">Level {level} • 8 components</p>
        </div>
      </div>

      {/* React Flow Canvas */}
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="#1e1e2e" />
        <Controls position="bottom-left" />
        <MiniMap
          nodeColor="#313147"
          maskColor="rgba(10, 10, 15, 0.7)"
          position="bottom-right"
        />
      </ReactFlow>
    </div>
  )
}
