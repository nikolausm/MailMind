import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DocViewer from './pages/DocViewer'
import DocEditor from './pages/DocEditor'
import Home from './pages/Home'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="docs/*" element={<DocViewer />} />
          <Route path="edit/*" element={<DocEditor />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App