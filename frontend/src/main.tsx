import React from 'react'
import ReactDOM from 'react-dom/client'

// Direct render check - No App, No CSS
ReactDOM.createRoot(document.getElementById('root')!).render(
  <div style={{ color: 'red', fontSize: '30px', padding: '20px' }}>
    <h1>🚨 EMERGENCY MAIN.TSX CHECK 🚨</h1>
    <p>If you see this, main.tsx is working!</p>
  </div>
)
