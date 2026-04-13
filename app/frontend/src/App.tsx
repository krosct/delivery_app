import { useState } from 'react'

function App() {
  const [message] = useState('Delivery App frontend loaded')

  return (
    <main className="app-shell">
      <h1>Delivery App</h1>
      <p>{message}</p>
    </main>
  )
}

export default App
