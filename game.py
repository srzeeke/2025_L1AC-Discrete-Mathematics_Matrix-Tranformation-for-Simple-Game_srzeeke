import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';

const MatrixGame = () => {
  const canvasRef = useRef(null);
  const [rotation, setRotation] = useState(0);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 400, y: 300 });
  const [isPlaying, setIsPlaying] = useState(false);
  const [score, setScore] = useState(0);
  const [targets, setTargets] = useState([]);
  const [keysPressed, setKeysPressed] = useState({});

  // ═══════════════════════════════════════════════════════════════
  // ✨ HOMOGENEOUS COORDINATES - 3x3 TRANSFORMATION MATRIX ✨
  // ═══════════════════════════════════════════════════════════════
  // Create homogeneous transformation matrix
  // This combines Scale, Rotation, and Translation into ONE matrix!
  const createTransformMatrix = (tx, ty, angle, sx, sy) => {
    const cos = Math.cos(angle);
    const sin = Math.sin(angle);
    
    // 3x3 Homogeneous Transformation Matrix:
    // | sx*cos  -sy*sin   tx |  ← Translation (tx, ty) in 3rd column
    // | sx*sin   sy*cos   ty |  ← Scale (sx, sy) combined with Rotation
    // |   0        0       1 |  ← Homogeneous coordinate (makes translation possible)
    return [
      [sx * cos, -sy * sin, tx],  // Row 1: X transformation + translation
      [sx * sin, sy * cos, ty],   // Row 2: Y transformation + translation
      [0, 0, 1]                   // Row 3: Homogeneous row (always [0,0,1])
    ];
  };

  // ═══════════════════════════════════════════════════════════════
  // ✨ APPLYING HOMOGENEOUS TRANSFORMATION ✨
  // ═══════════════════════════════════════════════════════════════
  // Apply transformation matrix to a point (x, y, 1)
  // Point in homogeneous coords: [x, y, 1]ᵀ
  // Result: [x', y', 1]ᵀ = Matrix × [x, y, 1]ᵀ
  const transformPoint = (matrix, x, y) => {
    // Matrix multiplication: [x', y', w] = Matrix × [x, y, 1]
    // x' = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]*1
    // y' = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]*1
    // w  = matrix[2][0]*x + matrix[2][1]*y + matrix[2][2]*1 = 1 (always)
    return {
      x: matrix[0][0] * x + matrix[0][1] * y + matrix[0][2], // x' = rotation/scale + translation
      y: matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]  // y' = rotation/scale + translation
      // Note: We implicitly use homogeneous coordinate w=1 (third component)
    };
  };

  // Spaceship shape (centered at origin)
  const shipShape = [
    { x: 0, y: -20 },    // nose
    { x: -10, y: 10 },   // left wing
    { x: -5, y: 5 },     // left inner
    { x: 5, y: 5 },      // right inner
    { x: 10, y: 10 }     // right wing
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const draw = () => {
      // Clear canvas
      ctx.fillStyle = '#0a0a1a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw stars
      ctx.fillStyle = '#ffffff';
      for (let i = 0; i < 50; i++) {
        const x = (i * 137.5) % canvas.width;
        const y = (i * 217.3) % canvas.height;
        ctx.fillRect(x, y, 2, 2);
      }
      
      // ═══════════════════════════════════════════════════════════════
      // ✨ HOMOGENEOUS TRANSFORMATION IN ACTION ✨
      // ═══════════════════════════════════════════════════════════════
      // Create transformation matrix combining all transformations
      const matrix = createTransformMatrix(
        position.x,  // Translation X
        position.y,  // Translation Y
        rotation,    // Rotation angle
        scale,       // Scale X
        scale        // Scale Y
      );
      
      // Transform each vertex of the spaceship using the matrix
      // Each point [x, y] is treated as [x, y, 1] in homogeneous coordinates
      // Result: [x', y', 1] = TransformMatrix × [x, y, 1]
      const transformedPoints = shipShape.map(p => transformPoint(matrix, p.x, p.y));
      
      ctx.beginPath();
      ctx.moveTo(transformedPoints[0].x, transformedPoints[0].y);
      for (let i = 1; i < transformedPoints.length; i++) {
        ctx.lineTo(transformedPoints[i].x, transformedPoints[i].y);
      }
      ctx.closePath();
      ctx.fillStyle = '#00ff88';
      ctx.fill();
      ctx.strokeStyle = '#00ffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw engine glow
      const enginePos = transformPoint(matrix, 0, 10);
      const gradient = ctx.createRadialGradient(enginePos.x, enginePos.y, 0, enginePos.x, enginePos.y, 15);
      gradient.addColorStop(0, 'rgba(255, 100, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(255, 100, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(enginePos.x, enginePos.y, 15, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw targets
      targets.forEach(target => {
        ctx.beginPath();
        ctx.arc(target.x, target.y, 15, 0, Math.PI * 2);
        ctx.strokeStyle = '#ff0066';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(target.x, target.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#ff0066';
        ctx.fill();
      });
      
      // Draw transformation matrix
      ctx.fillStyle = '#ffffff';
      ctx.font = '14px monospace';
      ctx.fillText('Transformation Matrix:', 10, 30);
      matrix.forEach((row, i) => {
        const rowText = [${row.map(v => v.toFixed(2).padStart(7)).join(' ')}];
        ctx.fillText(rowText, 10, 50 + i * 20);
      });
      
      // Draw score
      ctx.font = '20px monospace';
      ctx.fillText(Score: ${score}, canvas.width - 150, 30);
    };
    
    draw();
  }, [position, rotation, scale, targets, score]);

  useEffect(() => {
    if (isPlaying && targets.length === 0) {
      // Spawn new targets
      const newTargets = [];
      for (let i = 0; i < 3; i++) {
        newTargets.push({
          x: Math.random() * 700 + 50,
          y: Math.random() * 500 + 50,
          id: Date.now() + i
        });
      }
      setTargets(newTargets);
    }
  }, [isPlaying, targets.length]);

  useEffect(() => {
    // Check collisions
    if (isPlaying) {
      const newTargets = targets.filter(target => {
        const dx = target.x - position.x;
        const dy = target.y - position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < 30) {
          setScore(s => s + 10);
          return false;
        }
        return true;
      });
      if (newTargets.length !== targets.length) {
        setTargets(newTargets);
      }
    }
  }, [position, targets, isPlaying]);

  const handleKeyDown = (e) => {
    if (!isPlaying) return;
    setKeysPressed(prev => ({ ...prev, [e.key]: true }));
  };

  const handleKeyUp = (e) => {
    setKeysPressed(prev => ({ ...prev, [e.key]: false }));
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [isPlaying]);

  // Game loop for continuous movement
  useEffect(() => {
    if (!isPlaying) return;

    const gameLoop = setInterval(() => {
      if (keysPressed['ArrowLeft']) {
        setRotation(r => r - 0.1);
      }
      if (keysPressed['ArrowRight']) {
        setRotation(r => r + 0.1);
      }
      if (keysPressed['ArrowUp']) {
        setPosition(p => {
          let newX = p.x + Math.sin(rotation) * 5;
          let newY = p.y - Math.cos(rotation) * 5;
          
          // Wrap around screen edges
          if (newX < 0) newX = 800;
          if (newX > 800) newX = 0;
          if (newY < 0) newY = 600;
          if (newY > 600) newY = 0;
          
          return { x: newX, y: newY };
        });
      }
      if (keysPressed['ArrowDown']) {
        setPosition(p => {
          let newX = p.x - Math.sin(rotation) * 5;
          let newY = p.y + Math.cos(rotation) * 5;
          
          // Wrap around screen edges
          if (newX < 0) newX = 800;
          if (newX > 800) newX = 0;
          if (newY < 0) newY = 600;
          if (newY > 600) newY = 0;
          
          return { x: newX, y: newY };
        });
      }
    }, 16); // ~60 FPS

    return () => clearInterval(gameLoop);
  }, [isPlaying, keysPressed, rotation]);

  const reset = () => {
    setPosition({ x: 400, y: 300 });
    setRotation(0);
    setScale(1);
    setScore(0);
    setTargets([]);
    setIsPlaying(false);
  };

  return (
    <div className="w-full h-screen bg-gray-900 flex flex-col items-center justify-center p-4">
      <div className="bg-gray-800 rounded-lg p-6 shadow-2xl">
        <h1 className="text-3xl font-bold text-cyan-400 mb-4 text-center">
          Matrix Transformation Game
        </h1>
        
        <canvas
          ref={canvasRef}
          width={800}
          height={600}
          className="border-4 border-cyan-500 rounded-lg mb-4"
        />
        
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="bg-gray-700 p-4 rounded-lg">
            <label className="text-cyan-300 block mb-2">Rotation</label>
            <input
              type="range"
              min="-3.14"
              max="3.14"
              step="0.1"
              value={rotation}
              onChange={(e) => setRotation(parseFloat(e.target.value))}
              className="w-full"
            />
            <span className="text-white">{rotation.toFixed(2)} rad</span>
          </div>
          
          <div className="bg-gray-700 p-4 rounded-lg">
            <label className="text-cyan-300 block mb-2">Scale</label>
            <input
              type="range"
              min="0.5"
              max="2"
              step="0.1"
              value={scale}
              onChange={(e) => setScale(parseFloat(e.target.value))}
              className="w-full"
            />
            <span className="text-white">{scale.toFixed(1)}x</span>
          </div>
          
          <div className="bg-gray-700 p-4 rounded-lg">
            <label className="text-cyan-300 block mb-2">Translation</label>
            <div className="text-white text-sm">
              X: {position.x.toFixed(0)}<br/>
              Y: {position.y.toFixed(0)}
            </div>
          </div>
        </div>
        
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="bg-cyan-500 hover:bg-cyan-600 text-white px-6 py-3 rounded-lg flex items-center gap-2"
          >
            {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            {isPlaying ? 'Pause' : 'Start'}
          </button>
          
          <button
            onClick={reset}
            className="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-lg flex items-center gap-2"
          >
            <RotateCcw size={20} />
            Reset
          </button>
        </div>
        
        <div className="mt-4 text-gray-300 text-sm text-center">
          <p>Use arrow keys to control the spaceship!</p>
          <p>↑↓ to move forward/backward • ←→ to rotate</p>
        </div>
      </div>
    </div>
  );
};

export default MatrixGame;