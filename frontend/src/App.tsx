import { useState, useEffect, useRef } from 'react'
// --- Reconocimiento de voz ---
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import Scene3D from './components/Scene3D'
import './App.css'

// Tipo para los mensajes del chat
interface Message {
  type: 'user' | 'turtle'
  text: string
  timestamp: number
}

function App() {
  // --- LÓGICA DE RECONOCIMIENTO DE VOZ ---
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition()

  // --- ESTADOS DEL COMPONENTE ---
  const [conversationId, setConversationId] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [currentUserText, setCurrentUserText] = useState('')
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Pulso neón del título
  const [titlePulse, setTitlePulse] = useState(false)
  const pulse = () => {
    setTitlePulse(true)
    setTimeout(() => setTitlePulse(false), 700)
  }

  // URL del backend (permite Vite env)
  const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

  // --- Actualiza el texto del usuario a medida que habla ---
  useEffect(() => {
    if (transcript) setCurrentUserText(transcript)
  }, [transcript])

  // Auto-scroll al último mensaje
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // --- Botón de micrófono ---
  const handleMicrophoneClick = async () => {
    if (listening) {
      // Si ya está escuchando, detenemos
      SpeechRecognition.stopListening()

      if (transcript.trim()) {
        // Agregar mensaje del usuario al historial
        const userMessage: Message = {
          type: 'user',
          text: transcript,
          timestamp: Date.now()
        }
        setMessages(prev => [...prev, userMessage])

        try {
          const res = await fetch(`${API_URL}/chat/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: transcript, conversation_id: conversationId })
          })
          const data = await res.json()
          
          // Agregar respuesta de la tortuga al historial
          const turtleMessage: Message = {
            type: 'turtle',
            text: data.response,
            timestamp: Date.now()
          }
          setMessages(prev => [...prev, turtleMessage])

          if (data.is_complete) setConversationId('')
          else setConversationId(data.conversation_id)

          if (data.audiob64) {
            const audio = new Audio(`data:audio/mp3;base64,${data.audiob64}`)
            audio.play().catch(() => {})
          }
        } catch (e) {
          console.error('Error sending message to backend:', e)
          const errorMessage: Message = {
            type: 'turtle',
            text: '¡Ups! Hubo un error al comunicarse con la tortuga.',
            timestamp: Date.now()
          }
          setMessages(prev => [...prev, errorMessage])
        }

        // Limpiar el texto actual
        setCurrentUserText('')
      }
    } else {
      // Preparar para escuchar
      resetTranscript()
      setCurrentUserText('')
      SpeechRecognition.startListening({ continuous: true, language: 'es-ES' })
    }
  }

  // --- Compatibilidad del navegador ---
  if (!browserSupportsSpeechRecognition) {
    return <span>Lo sentimos, tu navegador no soporta el reconocimiento de voz.</span>
  }

  return (
    <div className="turtlector-app">
      {/* borde dorado superior */}
      <div className="header-edge" />

      {/* ENCABEZADO */}
      <header className="header">
        <div className="brand">
          <div className="logo-ring"><div className="logo-dot" /></div>
          <h1
            className={`app-title ${titlePulse ? 'active' : ''}`}
            onClick={pulse}
            title="✨"
          >
            Turtlector
          </h1>
        </div>

        {/* Píldora TAWS animada y clicable */}
        <a
            className="pill"
            href="https://taws.espol.edu.ec/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Abrir sitio de TAWS en una nueva pestaña"
            >
            <div className="pill-logo">
                <img
                src="/taws.svg"
                width={30}
                height={30}
                alt="TAWS"
                onError={(e) => { (e.target as HTMLImageElement).src = '/vite.svg' }}
                />
            </div>

            {/* NUEVO: línea con el eslogan */}
            <div className="pill-line">BE DIFFERENT&nbsp;&nbsp;BE TAWS</div>

            <span className="pill-dot" />
        </a>

      </header>

      {/* CONTENIDO PRINCIPAL */}
      <main className="main-content">
        <div className="layout-container new-layout">
          {/* COLUMNA IZQUIERDA */}
          <div className="left-column">
            {/* Tortuga */}
            <div className="tortuga-3d-container">
              <Scene3D animationState={listening ? 'loading' : 'standby'} />
            </div>

            {/* Micrófono debajo de la tortuga */}
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
          </div>

          {/* COLUMNA DERECHA - CHAT */}
          <div className="right-column">
            <div className="chat-container">
              {/* Historial de mensajes */}
              <div className="chat-history">
                {messages.length === 0 ? (
                  <div className="chat-empty">
                    <p>Haz clic en el micrófono y empieza a hablar con la tortuga...</p>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div 
                      key={idx} 
                      className={`chat-message ${msg.type === 'user' ? 'user-message' : 'turtle-message'}`}
                    >
                      <div className="message-label">
                        {msg.type === 'user' ? '👤 Tú' : '🐢 Tortuga'}
                      </div>
                      <div className="message-content">
                        <p>{msg.text}</p>
                      </div>
                    </div>
                  ))
                )}
                
                {/* Mensaje actual mientras hablas */}
                {listening && currentUserText && (
                  <div className="chat-message user-message typing">
                    <div className="message-label">👤 Tú (escribiendo...)</div>
                    <div className="message-content">
                      <p>{currentUserText}</p>
                    </div>
                  </div>
                )}
                
                <div ref={chatEndRef} />
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* FOOTER */}
      <div className="footer-edge" />
      <footer className="footer">
        <span>© 2025 TAWS — Todos los derechos reservados.</span>
      </footer>
    </div>
  )
}

export default App