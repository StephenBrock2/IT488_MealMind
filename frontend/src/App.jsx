import { useState } from 'react'
import logo from '/mealmind-logo.png'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
          <img src={logo} className="logo" alt="logo" />

      </div>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
  
    </>
  )
}

export default App
