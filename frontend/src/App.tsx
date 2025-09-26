import { useState, useEffect } from 'react'
// --- Importaciones de la librería de reconocimiento de voz ---
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import Scene3D from './components/Scene3D'
import './App.css'

// El tipo AnimationState ya no es necesario, lo manejaremos de otra forma
// pnpm add react-speech-recognition -> libreria , pnpm add -D @types/react-speech-recognition --> instalar los tipos de TypeScript
function App() {
    // --- LÓGICA DE RECONOCIMIENTO DE VOZ ---
    const {
        transcript, // El texto que el navegador reconoce en tiempo real
        listening, // Un booleano que nos dice si el micrófono está activo (true) or not (false)
        resetTranscript, // Una función para borrar el texto reconocido
        browserSupportsSpeechRecognition // Comprueba si el navegador es compatible
    } = useSpeechRecognition()

    // --- ESTADOS DEL COMPONENTE ---
    // El estado 'animationState' ahora se puede derivar directamente de 'listening'
    const [userText, setUserText] = useState('Aquí aparecerá el texto que hables para que la tortuga lo lea...')
    const [turtleText, setTurtleText] = useState('Aquí aparecerá la respuesta de la tortuga...')
    const [conversationId, setConversationId] = useState('')

    // --- useEffect para actualizar el cuadro de texto ---
    // Este "escucha" los cambios en `transcript` y actualiza nuestro estado `userText`.
    useEffect(() => {
        if (transcript) {
            setUserText(transcript)
        }
    }, [transcript])

    // --- Lógica del botón del micrófono totalmente renovada ---
    const handleMicrophoneClick = async () => {
        if (listening) {
            SpeechRecognition.stopListening() // Si ya está escuchando, lo detenemos

            if (transcript.trim()) {
                console.log(conversationId)
                try {
                    fetch("http://localhost:8000/chat/send", {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: transcript, conversation_id: conversationId })
                    })
                    .then( res => res.json() )
                    .then( data => {
                        setTurtleText(data.response);
                        if (data.is_complete) {
                            setConversationId('')
                        } else {
                            setConversationId(data.conversation_id)
                        }
                        const audio = new Audio(`data:audio/mp3;base64,${data.audiob64}`);
                        audio.play();
                    })
                } catch (e) {
                    console.error('Error sending message to backend:', e)
                    setTurtleText('¡Ups! Hubo un error al comunicarse con la tortuga.')
                }
            }
        } else {
            resetTranscript() // Borramos el texto anterior
            setUserText('') // Limpiamos el cuadro de texto visualmente

            SpeechRecognition.startListening({ continuous: true, language: 'es-ES' })
        }
    }

    // --- Comprobación de compatibilidad del navegador ---
    if (!browserSupportsSpeechRecognition) {
        return <span>Lo sentimos, tu navegador no soporta el reconocimiento de voz.</span>
    }

    return (
        <div className="turtlector-app">
            <header className="header">
                <h1 className="app-title">Turtlector</h1>
                <div className="logo">taws</div>
            </header>

            <main className="main-content">
                <div className="layout-container">
                    <div className="left-column">
                        <div className="tortuga-3d-container">
                            {/* La animación ahora depende directamente de si estamos escuchando o no */}
                            <Scene3D animationState={listening ? 'loading' : 'standby'} />
                        </div>
                        <div className="dialogue-box user-text-box">
                            {/* Si no hay texto y no está escuchando, muestra el mensaje inicial */}
                            <p>{userText || listening ? userText : "Haz clic en el micrófono y empieza a hablar..."}</p>
                        </div>
                    </div>
                    <div className="right-column">
                        <div className="dialogue-box turtle-response-box">
                            <p>{turtleText}</p>
                        </div>
                    </div>
                </div>

                <button
                    // La clase 'recording' ahora depende directamente de 'listening'
                    className={`microphone-button ${listening ? 'recording' : ''}`}
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
