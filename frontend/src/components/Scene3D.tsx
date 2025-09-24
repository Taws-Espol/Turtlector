import React, { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment, Loader } from '@react-three/drei'
import Tortuga3D from './Tortuga3D'

type AnimationState = 'standby' | 'loading' | 'talking'

interface Scene3DProps {
  animationState?: AnimationState
}

const Scene3D: React.FC<Scene3DProps> = ({ animationState = 'standby' }) => (
  <div className="scene-3d-container">
    <Canvas
      camera={{ position: [0, 0, 8], fov: 40 }}
      style={{ width: '100%', height: '100%' }}
      shadows
    >
      {/* Iluminacion */}
      <ambientLight intensity={0.6} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <pointLight position={[-10, -10, -5]} intensity={0.5} />

      {/* Ambiente */}
      <Environment preset="sunset" />

      {/* Modelo 3D con Suspense para carga */}
      <Suspense fallback={null}>
        <Tortuga3D animationState={animationState} />
      </Suspense>

      {/* Controles de orbita */}
      <OrbitControls
        enableZoom
        enablePan={false}
        autoRotate={false}
        target={[0, -1, 0]}
        maxPolarAngle={Math.PI / 2}
        minPolarAngle={Math.PI / 3}
        minDistance={5}
        maxDistance={15}
      />
    </Canvas>
    <Loader />
  </div>
)

export default Scene3D
