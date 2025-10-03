import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [index, setIndex] = useState<number>(0)
  const [text, setText] = useState("")

  async function getList(index: number){
    const response = await fetch(`http://127.0.0.1:8000/items/${index}`)
    if (!response.ok){
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data)
  }

  async function getText(){
    const response = await fetch("http://127.0.0.1:8000/print")
    if (!response.ok){
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json()
    const message = data.message
    setText(message)
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <input 
        type="number" 
        value={index} 
        onChange={(e) => setIndex(Number(e.target.value))}
        placeholder="Enter index"
      />
      <div className="card">
        <button onClick={() => getList(index)}>
          Click Me
        </button>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
        <button onClick={() => getText()}>
          Get Message
        </button>
        <p>
          {text}
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
