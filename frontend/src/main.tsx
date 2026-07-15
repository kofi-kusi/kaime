import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'

import './index.css'
import App from './App.tsx'
import Events from './components/Events.tsx'
import Subscribers from './components/Subscribers.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/">
          <Route index element={<App />} />
          <Route path="events" element={<Events />} />
          <Route path="subscribers" element={<Subscribers />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
