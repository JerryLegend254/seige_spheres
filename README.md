#  SEIGE SPHERES

A modern twist on the classic air hockey game, featuring glowing visual effects, power-ups, and dynamic gameplay mechanics. Built with Python and Pygame.

## ✨ Features

- **Neon Visual Effects**: Enjoy vibrant glowing paddles, balls, and boundaries
- **Dynamic Power-up System**: Collect various power-ups to gain advantages
- **Smooth Physics**: Realistic ball movement and collision mechanics
- **Particle Effects**: Beautiful particle explosions on collisions
- **Goal Animations**: Exciting visual feedback for scoring
- **Two-Player Mode**: Local multiplayer support
- **Play Against AI**: With Varying Difficulty Levels

### Power-ups

  - **🟦Speed Boost**: Increases player movement speed by 50% (5 seconds) 
  - **🟪Size Change**: Makes the paddle 50% larger (5 seconds) 
  - **🟧Ball Speed**: Increases ball speed by 20% (permanent until goal) 
  - **🟩Multi Ball**: Spawns an additional ball 
  - **🟥Freeze Opponent**: The opponent cannot move 
  - **🟨Double Points**: The next goal earns double points 

## 🎮 Controls

### Player 1 (Left Side)
- `W` - Move Up
- `S` - Move Down
- `A` - Move Left
- `D` - Move Right

### Player 2 (Right Side)
- `↑` - Move Up
- `↓` - Move Down
- `←` - Move Left
- `→` - Move Right

##  Getting Started

### Prerequisites

- Python 3.7+
- Pygame library

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JerryLegend254/seige_spheres.git
cd seige_spheres
```
2. Create a virtual environment (recommended):
```bash
python -m venv venv
```
 - On Windows
   ```bash
    venv\Scripts\activate
   ```
 - on Mac/Linux
   ```bash
    source venv/bin/activate
   ```
3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python __main__.py
```

##  Gameplay Mechanics

### Scoring
- Score points by getting the ball into your opponent's goal
- The game continues until players decide to quit
- Current scores are displayed at the top of the screen

### Power-up System
- Power-ups spawn randomly every 10 seconds (70% spawn chance)
- Active power-ups are displayed next to the player's score
- Multiple power-ups can be active simultaneously
- Some power-ups stack with others for increased advantage

### Physics
- Ball speed increases slightly after each paddle hit
- Collision angles are calculated based on impact point
- Anti-stick mechanism prevents ball from getting trapped
- Minimum bounce angles ensure dynamic gameplay

## Technical Details

### Core Components

1. **Game Class**
   - Main game loop and state management
   - Power-up spawning and management
   - Collision detection
   - Score tracking

2. **Player Class**
   - Paddle movement and control
   - Power-up effects management
   - Score display
   - Glow effects rendering

3. **Ball Class**
   - Physics calculations
   - Collision response
   - Visual effects
   - Movement patterns

4. **Power-up Class**
   - Effect implementation
   - Visual representation
   - Duration management
   - Collision detection

### Performance Optimizations

- Collision cooldown system
- Efficient particle management
- Smart boundary checking
- Optimized rendering with surface caching

##  Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- Inspired by classic air hockey arcade games
- Built using the Pygame library
- Special thanks to the open-source gaming community

##  Known Issues

- [Issue 1]: Performance may decrease with too many particles
- [Issue 2]: Rare edge cases in power-up spawning locations
- [Issue 3]: Minor visual glitches with particle rendering and collision physics

##  Contact

Project Link: [https://github.com/JerryLegend254/seige_spheres](https://github.com/JerryLegend254/seige_spheres)
