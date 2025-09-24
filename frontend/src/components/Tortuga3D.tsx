import React, { useRef, useEffect, useMemo } from 'react'
import { useGLTF, useAnimations } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { Group, LoopRepeat } from 'three'

type AnimationState = 'standby' | 'loading' | 'talking'

interface Tortuga3DProps {
  animationState?: AnimationState
}

const animationActionPriority: Record<AnimationState, string[]> = {
  standby: ['Standby', 'idle', 'default'],
  loading: ['Mano', 'MANO', 'Loading', 'Cargando', 'loading', 'idle', 'default'],
  talking: ['Talking', 'talk', 'speak', 'idle', 'default'],
}

const Tortuga3D: React.FC<Tortuga3DProps> = ({ animationState = 'standby' }) => {
  const groupRef = useRef<Group>(null)

  const { scene: standbyScene, animations: standbyAnimations } = useGLTF('/Standby.glb')
  const { scene: loadingScene, animations: loadingAnimations } = useGLTF('/MANO.glb')
  const { scene: talkingScene, animations: talkingAnimations } = useGLTF('/Talking.glb')

  // Clonamos las escenas una sola vez para que no se pisen entre estados
  const sceneByState = useMemo(() => ({
    standby: standbyScene.clone(),
    loading: loadingScene.clone(),
    talking: talkingScene.clone(),
  }), [standbyScene, loadingScene, talkingScene])

  const animationsByState = useMemo(() => ({
    standby: standbyAnimations,
    loading: loadingAnimations,
    talking: talkingAnimations,
  }), [standbyAnimations, loadingAnimations, talkingAnimations])

  const currentScene = sceneByState[animationState]
  const currentAnimations = animationsByState[animationState]

  const { actions } = useAnimations(currentAnimations, groupRef)

  useEffect(() => {
    if (currentScene) {
      console.log(`[Tortuga3D] Modelo ${animationState} cargado`, currentScene)
      console.log('[Tortuga3D] Animaciones disponibles:', currentAnimations.map(anim => anim.name))
    } else {
      console.error(`[Tortuga3D] Error al cargar el modelo ${animationState}`)
    }
  }, [animationState, currentScene, currentAnimations])

  useEffect(() => {
    if (!actions || Object.keys(actions).length === 0) return

    Object.values(actions).forEach(action => action?.stop())

    const priorities = animationActionPriority[animationState]
    const targetAction =
      priorities.map(name => actions[name]).find(action => action) || Object.values(actions)[0]

    if (targetAction) {
      targetAction.reset()
      targetAction.setLoop(LoopRepeat, Infinity)
      targetAction.setEffectiveWeight(1)
      targetAction.setEffectiveTimeScale(1)
      targetAction.play()
      console.log(`[Tortuga3D] Reproduciendo animacion ${animationState}:`, targetAction.getClip().name)
    }
  }, [actions, animationState])

  useFrame(() => {
    if (!actions || Object.keys(actions).length === 0) return

    const priorities = animationActionPriority[animationState]
    const targetAction =
      priorities.map(name => actions[name]).find(action => action) || Object.values(actions)[0]

    if (targetAction && !targetAction.isRunning()) {
      targetAction.play()
    }
  })

  return (
    <group
      ref={groupRef}
      position={[0, -2, 0]}
      scale={[1.5, 1.5, 1.5]}
      rotation={[0, -Math.PI / 2, 0]}
    >
      <primitive object={currentScene} />
    </group>
  )
}

useGLTF.preload('/Standby.glb')
useGLTF.preload('/MANO.glb')
useGLTF.preload('/Talking.glb')

export default Tortuga3D
