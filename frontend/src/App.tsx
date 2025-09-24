import { useState } from 'react'
import Scene3D from './components/Scene3D'
import './App.css'

type AnimationState = 'standby' | 'loading' | 'talking'

function App() {
  const [animationState, setAnimationState] = useState<AnimationState>('standby')

  const handleMicrophoneClick = () => {
    setAnimationState(prev => {
      if (prev === 'standby') return 'loading'   // primer click -> escuchando (MANO.glb)
      if (prev === 'loading') return 'talking'   // segundo click -> hablando (Talking.glb)
      if (prev === 'talking') return 'loading'   // tercer click -> escuchando otra vez (MANO.glb)
      return 'standby'                           // esto no debería pasar, pero por seguridad
    })
  }

  return (
    <div className="turtlector-app">
      <header className="header">
        <h1 className="app-title">Turtlector</h1>
        <div className="logo">taws</div>
      </header>

      <main className="main-content">
        <div className="tortuga-3d-container">
          <Scene3D animationState={animationState} />
        </div>

        <button
          className={`microphone-button ${animationState === 'loading' ? 'recording' : ''}`}
          onClick={handleMicrophoneClick}
        >
          <svg className="microphone-icon" viewBox="0 0 24 24" fill="none">
            <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="white" />
            <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10H7V12C7 14.76 9.24 17 12 17C14.76 17 17 14.76 17 12V10H19Z" fill="white" />
            <path d="M11 22H13V24H11V22Z" fill="white" />
          </svg>
        </button>
      </main>
    </div>
  )
}

export default App