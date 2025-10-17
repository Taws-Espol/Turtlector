import { useEffect, useRef, useState } from 'react'
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import Scene3D from './components/Scene3D'
import './App.css'

type Msg = {
  id: string
  role: 'user' | 'assistant'
  text: string
  ts: number
}

function App() {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition()

  const [conversationId, setConversationId] = useState('')
  const [messages, setMessages] = useState<Msg[]>([])
  const [titlePulse, setTitlePulse] = useState(false)
  const listRef = useRef<HTMLDivElement>(null)

  const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

  // efecto: pulso al click del título
  const pulse = () => {
    setTitlePulse(true)
    setTimeout(() => setTitlePulse(false), 700)
  }

  // autoscroll al final cuando haya nuevos mensajes
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages.length])

  // si el navegador no soporta STT
  if (!browserSupportsSpeechRecognition) {
    return <span>Lo sentimos, tu navegador no soporta el reconocimiento de voz.</span>
  }

  const handleMicrophoneClick = async () => {
    if (listening) {
      // detener escucha y enviar lo capturado
      SpeechRecognition.stopListening()
      const text = transcript.trim()
      if (!text) return

      const userMsg: Msg = { id: crypto.randomUUID(), role: 'user', text, ts: Date.now() }
      setMessages(prev => [...prev, userMsg])

      try {
        const res = await fetch(`${API_URL}/chat/send`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, conversation_id: conversationId })
        })
        const data = await res.json()

        const botMsg: Msg = {
          id: crypto.randomUUID(),
          role: 'assistant',
          text: data.response ?? '…',
          ts: Date.now()
        }
        setMessages(prev => [...prev, botMsg])

        if (data.is_complete) setConversationId('')
        else setConversationId(data.conversation_id)

        if (data.audiob64) {
          const audio = new Audio(`data:audio/mp3;base64,${data.audiob64}`)
          audio.play().catch(() => {})
        }
      } catch (e) {
        const errMsg: Msg = {
          id: crypto.randomUUID(),
          role: 'assistant',
          text: '¡Ups! Hubo un error al comunicarse con la tortuga.',
          ts: Date.now()
        }
        setMessages(prev => [...prev, errMsg])
        console.error(e)
      } finally {
        resetTranscript()
      }
    } else {
      // empezar a escuchar
      resetTranscript()
      SpeechRecognition.startListening({ continuous: true, language: 'es-ES' })
    }
  }

  return (
    <div className="turtlector-app">
      <div className="header-edge" />

      <header className="header">
        <div className="brand">
          <div className="logo-ring"><div className="logo-dot" /></div>
          <h1 className={`app-title ${titlePulse ? 'active' : ''}`} onClick={pulse}>Turtlector</h1>
        </div>

        <a
          className="pill"
          href="https://taws.espol.edu.ec/"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Abrir sitio de TAWS en una nueva pestaña"
        >
          <div className="pill-logo">
            <img src="/taws.svg" width={30} height={30} alt="TAWS"
              onError={(e)=>{ (e.target as HTMLImageElement).src='/vite.svg' }} />
          </div>
          <div className="pill-line">BE DIFFERENT&nbsp;&nbsp;BE TAWS</div>
          <span className="pill-dot" />
        </a>
      </header>

      <main className="main-content">
        <div className="layout-chat">
          {/* izquierda: tortuga 3D */}
          <aside className="left-col">
            <div className="tortuga-3d-container">
              <Scene3D animationState={listening ? 'loading' : 'standby'} />
            </div>
          </aside>

          {/* derecha: chat */}
          <section className="chat-panel">
            <div className="chat-header">
              <span className="chat-title">Chat</span>
              <span className={`chat-dot ${listening ? 'on' : ''}`} />
            </div>

            <div className="chat-list" ref={listRef}>
              {messages.length === 0 ? (
                <div className="chat-empty">
                  Empieza a hablar con el micrófono para enviar tu mensaje.
                </div>
              ) : messages.map(m => (
                <div key={m.id} className={`bubble-row ${m.role}`}>
                  <div className={`bubble ${m.role}`}>
                    <p>{m.text}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <button
          className={`microphone-button ${listening ? 'recording' : ''}`}
          onClick={handleMicrophoneClick}
        >
          <svg className="microphone-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="white" />
            <path d="M19 10V12C19 15.87 15.87 19 12 19C8.13 19 5 15.87 5 12V10H7V12C7 14.76 9.24 17 12 17C14.76 17 17 14.76 17 12V10H19Z" fill="white" />
            <path d="M11 22H13V24H11V22Z" fill="white" />
          </svg>
        </button>
      </main>

      <div className="footer-edge" />
      <footer className="footer">
        <span>© 2025 TAWS — Todos los derechos reservados.</span>
      </footer>
    </div>
  )
}

export default App
