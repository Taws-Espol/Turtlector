import React, { useRef, useEffect } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { Group } from 'three'

interface Tortuga3DProps {
  isTalking?: boolean
}

const Tortuga3D: React.FC<Tortuga3DProps> = ({ isTalking = false }) => {
  const groupRef = useRef<Group>(null)
  
  // Cargar el modelo con manejo de errores
  const { scene, animations } = useGLTF('/Standby.glb')
  const { actions } = useAnimations(animations, groupRef)

  // Validar que el modelo se cargó correctamente
  useEffect(() => {
    if (scene) {
      console.log('✅ Modelo Standby cargado correctamente:', scene)
      console.log('📊 Animaciones disponibles:', animations.map(anim => anim.name))
    } else {
      console.error('❌ Error al cargar el modelo Standby')
    }
  }, [scene, animations])

  // Aplicar animación de Standby automáticamente
  useEffect(() => {
    if (actions && Object.keys(actions).length > 0) {
      console.log('🎬 Animaciones disponibles:', Object.keys(actions))
      
      // Buscar animación de standby
      const standbyAction = actions['Standby'] || actions['idle'] || actions['default'] || Object.values(actions)[0]
      
      if (standbyAction) {
        // Configurar loop infinito
        standbyAction.setLoop(1, Infinity) // Loop infinito
        standbyAction.setEffectiveWeight(1.0) // Peso completo
        standbyAction.setEffectiveTimeScale(1.0) // Velocidad normal
        standbyAction.play()
        console.log('😴 Reproduciendo animación de Standby en bucle infinito:', standbyAction.getClip().name)
      }
    }
  }, [actions])

  // Asegurar que la animación se mantenga en bucle
  useFrame(() => {
    if (actions && Object.keys(actions).length > 0) {
      const standbyAction = actions['Standby'] || actions['idle'] || actions['default'] || Object.values(actions)[0]
      if (standbyAction && !standbyAction.isRunning()) {
        standbyAction.play()
      }
    }
  })

  return (
    <group ref={groupRef} position={[0, -2, 0]} scale={[1.5, 1.5, 1.5]} rotation={[0, -Math.PI / 2, 0]}>
      <primitive object={scene} />
    </group>
  )
}

export default Tortuga3D
