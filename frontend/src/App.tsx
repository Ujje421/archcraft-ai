import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import CanvasPage from './pages/CanvasPage'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/design/:id" element={<CanvasPage />} />
      </Route>
    </Routes>
  )
}
