import React, { useRef, useEffect } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { Group, LoopRepeat } from 'three'

interface Tortuga3DProps {
  isTalking?: boolean
}

const Tortuga3D: React.FC<Tortuga3DProps> = ({ isTalking = false }) => {
  const groupRef = useRef<Group>(null)
  
  // Cargar el modelo según el estado
  const { scene: standbyScene, animations: standbyAnimations } = useGLTF('/Standby.glb')
  const { scene: talkingScene, animations: talkingAnimations } = useGLTF('/Talking.glb')
  
  // Usar el modelo y animaciones según el estado
  const currentScene = isTalking ? talkingScene : standbyScene
  const currentAnimations = isTalking ? talkingAnimations : standbyAnimations
  const { actions } = useAnimations(currentAnimations, groupRef)

  // Validar que los modelos se cargaron correctamente
  useEffect(() => {
    if (currentScene) {
      console.log(`✅ Modelo ${isTalking ? 'Talking' : 'Standby'} cargado correctamente:`, currentScene)
      console.log('📊 Animaciones disponibles:', currentAnimations.map(anim => anim.name))
    } else {
      console.error(`❌ Error al cargar el modelo ${isTalking ? 'Talking' : 'Standby'}`)
    }
  }, [currentScene, currentAnimations, isTalking])

  // Aplicar animación según el estado
  useEffect(() => {
    if (!actions || Object.keys(actions).length === 0) return
    console.log('🎬 Animaciones disponibles:', Object.keys(actions))

    // Detener cualquier animación previa
    Object.values(actions).forEach(action => action?.stop())

    // Elegir animación según estado
    const targetAction = isTalking
      ? actions['Talking'] || actions['talk'] || actions['speak'] || actions['idle'] || Object.values(actions)[0]
      : actions['Standby'] || actions['idle'] || actions['default'] || Object.values(actions)[0]

    if (targetAction) {
      targetAction.reset()
      targetAction.setLoop(LoopRepeat, Infinity)
      targetAction.setEffectiveWeight(1.0)
      targetAction.setEffectiveTimeScale(1.0)
      targetAction.play()
      console.log(`🎭 Reproduciendo animación ${isTalking ? 'Talking' : 'Standby'} en bucle infinito:`, targetAction.getClip().name)
    }
  }, [actions, isTalking])

  // Asegurar continuidad del bucle si el mixer detiene la acción
  useFrame(() => {
    if (!actions || Object.keys(actions).length === 0) return
    const targetAction = isTalking
      ? actions['Talking'] || actions['talk'] || actions['speak'] || actions['idle'] || Object.values(actions)[0]
      : actions['Standby'] || actions['idle'] || actions['default'] || Object.values(actions)[0]
    if (targetAction && !targetAction.isRunning()) {
      targetAction.play()
    }
  })

  return (
    <group ref={groupRef} position={[0, -2, 0]} scale={[1.5, 1.5, 1.5]} rotation={[0, -Math.PI / 2, 0]}>
      <primitive object={currentScene} />
    </group>
  )
}

export default Tortuga3D
