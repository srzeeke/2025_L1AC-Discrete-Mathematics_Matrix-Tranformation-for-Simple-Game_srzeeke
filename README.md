# Matrix Transformation Game
<img width="836" height="893" alt="image" src="https://github.com/user-attachments/assets/8e2e6714-c94f-4fdc-add4-d8e67222a535" />


A React-based game that demonstrates real-time matrix transformations using homogeneous coordinates. Control a spaceship using transformation matrices and collect targets in space!

## 🎮 How to Play

### Basic Controls
- **Arrow Up**: Move forward (thrust)
- **Arrow Down**: Move backward
- **Arrow Left**: Rotate counterclockwise
- **Arrow Right**: Rotate clockwise
- **Start/Pause**: Toggle game state
- **Reset**: Reset game to initial state

### Game Objective
- Navigate your spaceship to collect the red target circles
- Each target collected gives you 10 points
- Targets respawn when all are collected
- The spaceship wraps around screen edges

## 🚀 Features

### Matrix Transformation System
The game implements **homogeneous transformation matrices** to combine all transformations into a single 3x3 matrix:

```javascript
// Homogeneous Transformation Matrix Structure:
[
  [sx*cos(θ), -sy*sin(θ), tx],  // Scale + Rotation + Translation X
  [sx*sin(θ),  sy*cos(θ), ty],  // Scale + Rotation + Translation Y
  [0,          0,          1 ]  // Homogeneous coordinate
]
```

### Real-time Visual Feedback
- **Live Matrix Display**: Watch the transformation matrix update in real-time
- **Visual Transformations**: See scale, rotation, and translation applied simultaneously
- **Coordinate System**: Homogeneous coordinates enable efficient 2D transformations

### Interactive Controls
- **Rotation Slider**: Manually adjust rotation angle (-π to π radians)
- **Scale Slider**: Adjust spaceship size (0.5x to 2x)
- **Real-time Translation**: Position updates displayed continuously

### Game Elements
- **Spaceship**: Transformed using matrix operations
- **Target System**: Collect red circles for points
- **Particle Effects**: Engine glow with radial gradients
- **Starfield Background**: Immersive space environment

## 🧮 Technical Implementation

### Homogeneous Coordinates
The game uses 3D homogeneous coordinates `[x, y, 1]` for 2D points, allowing:
- **Translation** as matrix multiplication (not just addition)
- **Combined transformations** in single matrix operations
- **Efficient computation** using matrix multiplication

### Transformation Pipeline
1. **Input Processing**: Keyboard controls update transformation parameters
2. **Matrix Construction**: Build 3x3 homogeneous transformation matrix
3. **Vertex Transformation**: Apply matrix to each spaceship vertex
4. **Rendering**: Draw transformed shape with visual effects

### Key Mathematical Operations
```javascript
// Matrix multiplication for point transformation
x' = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]
y' = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]
```

## 🎯 Learning Outcomes

This game demonstrates:
- **Linear Algebra in Practice**: Real-world use of transformation matrices
- **Computer Graphics Fundamentals**: How 2D transformations work
- **Homogeneous Coordinates**: Why they're essential for graphics programming
- **Matrix Composition**: Combining multiple transformations efficiently

## 🛠️ Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Run the Game**
   ```bash
   npm run dev
   ```

3. **Play!**
   - Click "Start" to begin
   - Use arrow keys to navigate
   - Watch the transformation matrix update

## 📊 Game Mechanics

- **Collision Detection**: Circle-based collision with targets
- **Screen Wrapping**: Seamless movement across screen edges
- **Continuous Game Loop**: ~60 FPS update rate
- **State Management**: React hooks for game state

Experience the power of matrix mathematics in this interactive space adventure!


