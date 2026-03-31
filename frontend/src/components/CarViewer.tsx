// CarViewer.tsx - 3D GT3 R showroom viewport

import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

interface CarViewerProps {
  highlightComponent?: "front_wing" | "rear_wing" | "brakes" | null;
}

export const CarViewer: React.FC<CarViewerProps> = ({ highlightComponent }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let w = container.clientWidth;
    let h = container.clientHeight;

    /* ═══════════════════════════════════
       Scene
       ═══════════════════════════════════ */
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x050508);
    scene.fog = new THREE.FogExp2(0x050508, 0.04);

    /* ═══════════════════════════════════
       Camera
       ═══════════════════════════════════ */
    const camera = new THREE.PerspectiveCamera(42, w / h, 0.1, 500);
    camera.position.set(5.5, 3, 7.5);

    /* ═══════════════════════════════════
       Renderer
       ═══════════════════════════════════ */
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    container.appendChild(renderer.domElement);

    /* ═══════════════════════════════════
       Studio Lighting Rig
       ═══════════════════════════════════ */

    // Low ambient — keeps shadows dramatic
    const ambient = new THREE.AmbientLight(0x16162a, 1.0);
    scene.add(ambient);

    // Hemisphere — subtle sky-to-ground color shift
    const hemi = new THREE.HemisphereLight(0x1c1c3a, 0x060608, 0.5);
    scene.add(hemi);

    // Key light — warm spot from upper-right-front
    const keyLight = new THREE.SpotLight(0xfff0dd, 40);
    keyLight.position.set(7, 10, 7);
    keyLight.angle = Math.PI / 5;
    keyLight.penumbra = 0.85;
    keyLight.decay = 1.6;
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(1024, 1024);
    keyLight.shadow.camera.near = 3;
    keyLight.shadow.camera.far = 30;
    keyLight.shadow.bias = -0.0004;
    scene.add(keyLight);
    keyLight.target.position.set(0, 0, 0);
    scene.add(keyLight.target);

    // Fill light — cool blue from upper-left
    const fillLight = new THREE.SpotLight(0xa8bfff, 10);
    fillLight.position.set(-7, 7, -1);
    fillLight.angle = Math.PI / 4;
    fillLight.penumbra = 0.9;
    fillLight.decay = 1.6;
    scene.add(fillLight);

    // Rim / back light — separates car from background
    const rimLight = new THREE.SpotLight(0xffffff, 15);
    rimLight.position.set(0, 5, -9);
    rimLight.angle = Math.PI / 4.5;
    rimLight.penumbra = 0.7;
    rimLight.decay = 1.5;
    scene.add(rimLight);

    // Brand accent — orange, low front-left
    const accentOrange = new THREE.PointLight(0xff6b00, 4, 12, 2);
    accentOrange.position.set(3, 0.4, 4);
    scene.add(accentOrange);

    // Cool accent — cyan, low rear-right
    const accentCyan = new THREE.PointLight(0x00d4ff, 2.5, 12, 2);
    accentCyan.position.set(-3, 0.4, -4);
    scene.add(accentCyan);

    /* ═══════════════════════════════════
       Ground & Platform
       ═══════════════════════════════════ */

    // Large ground disc
    const groundGeo = new THREE.CircleGeometry(25, 64);
    const groundMat = new THREE.MeshStandardMaterial({
      color: 0x07070d,
      roughness: 0.55,
      metalness: 0.45,
    });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.03;
    ground.receiveShadow = true;
    scene.add(ground);

    // Grid overlay — subtle engineering aesthetic
    const grid = new THREE.GridHelper(40, 80, 0x161628, 0x0d0d18);
    grid.position.y = -0.02;
    const gridMats = Array.isArray(grid.material)
      ? grid.material
      : [grid.material];
    gridMats.forEach((m) => {
      m.transparent = true;
      m.opacity = 0.45;
    });
    scene.add(grid);

    // Circular turntable platform
    const platformGeo = new THREE.CylinderGeometry(3.4, 3.6, 0.06, 96);
    const platformMat = new THREE.MeshStandardMaterial({
      color: 0x0a0a15,
      roughness: 0.25,
      metalness: 0.7,
    });
    const platform = new THREE.Mesh(platformGeo, platformMat);
    platform.receiveShadow = true;
    scene.add(platform);

    // Outer edge ring — glowing orange
    const edgeRingGeo = new THREE.TorusGeometry(3.5, 0.012, 8, 128);
    const edgeRingMat = new THREE.MeshBasicMaterial({
      color: 0xff6b00,
      transparent: true,
      opacity: 0.35,
    });
    const edgeRing = new THREE.Mesh(edgeRingGeo, edgeRingMat);
    edgeRing.rotation.x = -Math.PI / 2;
    edgeRing.position.y = 0.035;
    scene.add(edgeRing);

    // Inner ring — subtle cyan
    const innerRingGeo = new THREE.TorusGeometry(2.2, 0.006, 8, 96);
    const innerRingMat = new THREE.MeshBasicMaterial({
      color: 0x00d4ff,
      transparent: true,
      opacity: 0.12,
    });
    const innerRing = new THREE.Mesh(innerRingGeo, innerRingMat);
    innerRing.rotation.x = -Math.PI / 2;
    innerRing.position.y = 0.035;
    scene.add(innerRing);

    // Ground glow disc under platform
    const glowGeo = new THREE.CircleGeometry(5, 64);
    const glowMat = new THREE.MeshBasicMaterial({
      color: 0xff6b00,
      transparent: true,
      opacity: 0.015,
    });
    const glowDisc = new THREE.Mesh(glowGeo, glowMat);
    glowDisc.rotation.x = -Math.PI / 2;
    glowDisc.position.y = -0.025;
    scene.add(glowDisc);

    /* ═══════════════════════════════════
       Floating Dust Particles
       ═══════════════════════════════════ */
    const PARTICLE_COUNT = 60;
    const pPositions = new Float32Array(PARTICLE_COUNT * 3);
    const pSpeeds = new Float32Array(PARTICLE_COUNT);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      pPositions[i * 3] = (Math.random() - 0.5) * 24;
      pPositions[i * 3 + 1] = Math.random() * 10;
      pPositions[i * 3 + 2] = (Math.random() - 0.5) * 24;
      pSpeeds[i] = 0.001 + Math.random() * 0.004;
    }

    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute("position", new THREE.BufferAttribute(pPositions, 3));

    const pMat = new THREE.PointsMaterial({
      color: 0xff6b00,
      size: 0.035,
      transparent: true,
      opacity: 0.35,
      sizeAttenuation: true,
      depthWrite: false,
    });
    const particles = new THREE.Points(pGeo, pMat);
    scene.add(particles);

    /* ═══════════════════════════════════
       Controls
       ═══════════════════════════════════ */
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.enablePan = false;
    controls.minDistance = 4.5;
    controls.maxDistance = 14;
    controls.maxPolarAngle = Math.PI / 2.05;
    controls.minPolarAngle = Math.PI / 10;
    controls.target.set(0, 0.45, 0);

    /* ═══════════════════════════════════
       Load GLB Model
       ═══════════════════════════════════ */
    const loader = new GLTFLoader();
    let carModel: THREE.Object3D | null = null;

    loader.load(
      "/models/2017_porsche_911_rsr.glb",
      (gltf) => {
        carModel = gltf.scene;

        carModel.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            const mesh = child as THREE.Mesh;
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            // Boost reflections on every material
            const mat = mesh.material;
            if (mat && !Array.isArray(mat) && "envMapIntensity" in mat) {
              mat.envMapIntensity = 0.9;
            }
          }
        });

        // Highlight a specific component
        if (highlightComponent) {
          const target = carModel.getObjectByName(highlightComponent);
          if (target && (target as THREE.Mesh).isMesh) {
            (target as THREE.Mesh).material = new THREE.MeshStandardMaterial({
              color: 0xff6b00,
              emissive: 0xff6b00,
              emissiveIntensity: 1.2,
              roughness: 0.15,
              metalness: 0.85,
            });
          }
        }

        carModel.position.y = 0.03;
        scene.add(carModel);
      },
      (xhr) => {
        if (xhr.total > 0) {
          console.log(`Model: ${((xhr.loaded / xhr.total) * 100).toFixed(0)}%`);
        }
      },
      (error) => {
        console.warn("GLB not found — showing placeholder:", error);

        // Fallback placeholder so viewport isn't just black
        const bodyGeo = new THREE.BoxGeometry(2.2, 0.7, 4.8);
        const bodyMat = new THREE.MeshStandardMaterial({
          color: 0x1a1a2e,
          roughness: 0.3,
          metalness: 0.6,
        });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.position.y = 0.45;
        body.castShadow = true;
        body.receiveShadow = true;
        scene.add(body);

        const cabinGeo = new THREE.BoxGeometry(1.6, 0.55, 2.0);
        const cabinMat = new THREE.MeshStandardMaterial({
          color: 0x0e0e1c,
          roughness: 0.1,
          metalness: 0.9,
        });
        const cabin = new THREE.Mesh(cabinGeo, cabinMat);
        cabin.position.set(0, 0.95, -0.3);
        cabin.castShadow = true;
        scene.add(cabin);

        carModel = new THREE.Group();
        carModel.add(body, cabin);
        scene.add(carModel);
      }
    );

    /* ═══════════════════════════════════
       Animation Loop
       ═══════════════════════════════════ */
    let animId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      // Turntable rotation
      if (carModel) {
        carModel.rotation.y += 0.003;
      }

      // Edge ring pulse
      edgeRingMat.opacity = 0.28 + Math.sin(t * 2) * 0.12;

      // Inner ring slow counter-rotation
      innerRing.rotation.z = t * 0.08;

      // Ground glow breathe
      glowMat.opacity = 0.012 + Math.sin(t * 1.2) * 0.008;

      // Particle drift
      const pos = pGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        pos[i * 3 + 1] += pSpeeds[i];
        if (pos[i * 3 + 1] > 10) {
          pos[i * 3 + 1] = -0.5;
          pos[i * 3] = (Math.random() - 0.5) * 24;
          pos[i * 3 + 2] = (Math.random() - 0.5) * 24;
        }
      }
      pGeo.attributes.position.needsUpdate = true;

      // Slowly orbit the accent lights
      accentOrange.position.x = 3 + Math.sin(t * 0.4) * 1.5;
      accentOrange.position.z = 4 + Math.cos(t * 0.4) * 1.5;
      accentCyan.position.x = -3 + Math.sin(t * 0.25 + 2) * 1.5;
      accentCyan.position.z = -4 + Math.cos(t * 0.25 + 2) * 1.5;

      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    /* ═══════════════════════════════════
       Resize
       ═══════════════════════════════════ */
    const onResize = () => {
      if (!container) return;
      w = container.clientWidth;
      h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", onResize);

    /* ═══════════════════════════════════
       Cleanup
       ═══════════════════════════════════ */
    return () => {
      window.removeEventListener("resize", onResize);
      cancelAnimationFrame(animId);
      controls.dispose();
      renderer.dispose();

      scene.traverse((obj) => {
        const mesh = obj as THREE.Mesh;
        if (mesh.geometry) mesh.geometry.dispose();
        if (mesh.material) {
          const mats = Array.isArray(mesh.material)
            ? mesh.material
            : [mesh.material];
          mats.forEach((m) => m.dispose());
        }
      });

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [highlightComponent]);

  return (
    <div className="card p-0 overflow-hidden">
      <div className="relative">
        {/* Top-left: viewport badge */}
        <div className="absolute top-4 left-5 z-10 flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#FF6B00] animate-pulse" />
          <span className="font-mono text-[10px] tracking-[3px] text-white/20 uppercase">
            3D Viewport
          </span>
        </div>

        {/* Top-right: highlight indicator */}
        {highlightComponent && (
          <div className="absolute top-4 right-5 z-10 px-2.5 py-1 rounded-md bg-[#FF6B00]/10 border border-[#FF6B00]/20 backdrop-blur-sm">
            <span className="text-[10px] font-mono tracking-wider text-[#FF6B00]">
              {highlightComponent.replace(/_/g, " ").toUpperCase()}
            </span>
          </div>
        )}

        {/* Bottom-left: car name */}
        <div className="absolute bottom-4 left-5 z-10">
          <p className="font-mono text-[11px] tracking-widest text-[#FF6B00]/40">
            PORSCHE 911 GT3 RSR
          </p>
        </div>

        {/* Bottom-right: interaction hint */}
        <div className="absolute bottom-4 right-5 z-10 text-[10px] text-white/15 font-mono">
          DRAG TO ROTATE
        </div>

        {/* 3D canvas — fills the viewport */}
        <div
          ref={containerRef}
          className="car-viewer"
          style={{ height: "min(90vh, 960px)" }}
        />
      </div>
    </div>
  );
};