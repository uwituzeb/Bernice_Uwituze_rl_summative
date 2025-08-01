# 🚀 Enhanced Career Environment

A visually stunning reinforcement learning environment with advanced graphics, particle effects, and smooth animations for career development simulation.

## ✨ Features

### 🎨 Visual Enhancements
- **Particle Effects**: Colorful particle bursts when collecting opportunities
- **Screen Shake**: Dynamic feedback for interactions
- **Flash Effects**: Bright flashes for significant events
- **Smooth Animations**: Floating and rotating elements
- **Gradient Effects**: Beautiful color gradients on all elements
- **Animated UI**: Progress bars and legends with life-like animations

### 🎯 Gameplay Improvements
- **8x8 Grid**: Larger, more strategic playing field
- **Strategic Placement**: Opportunities placed in different quadrants
- **Enhanced Scoring**: More nuanced reward system
- **Visual Feedback**: Clear indicators for all actions
- **Consecutive Bonuses**: Rewards for consistent positive behavior

## 🎮 Controls

### Basic Controls
- **Arrow Keys** or **WASD**: Move the agent
- **SPACE**: Engage with opportunities
- **ESC**: Quit the game

### Demo Controls
- **A**: Toggle auto-play mode
- **E**: Toggle visual effects
- **R**: Reset the environment

## 🏆 Scoring System

| Action | Points | Description |
|--------|--------|-------------|
| 🟢 Course | +10 | Academic knowledge gain |
| 🔵 Extracurricular | +7 | Skill development |
| 🟣 Internship | +15 | Professional experience |
| 🔴 Distraction | -8 | Time wasted |
| 💫 Consecutive Bonus | +2 | Consistency reward |
| 🎯 Completion Bonus | +25 | All opportunities collected |

## 🚀 Quick Start

### 1. Run the Basic Demo
```bash
python demo_enhanced_env.py
```

### 2. Run the Advanced Demo
```bash
python demo_advanced_env.py
```

### 3. Use in Your RL Training
```python
from environment.advanced_env import AdvancedCareerEnv

env = AdvancedCareerEnv(render_mode="human", window_size=800)
obs, info = env.reset()

# Your RL training loop here
action = agent.act(obs)
obs, reward, done, truncated, info = env.step(action)
```

## 📁 File Structure

```
environment/
├── advanced_env.py          # Main advanced environment
├── advanced_rendering.py    # Advanced rendering system
├── enhanced_env.py          # Enhanced environment
├── enhanced_rendering.py    # Enhanced rendering system
├── custom_env.py           # Original basic environment
├── rendering.py            # Original basic rendering
└── assets/                 # Image assets (future use)

demo_enhanced_env.py        # Enhanced environment demo
demo_advanced_env.py        # Advanced environment demo
```

## 🎨 Visual Features Explained

### Particle System
- **Course Particles**: Green particles burst when collecting courses
- **Extracurricular Particles**: Blue particles for extracurricular activities
- **Internship Particles**: Purple particles for internships
- **Distraction Particles**: Red particles for negative interactions

### Animation Effects
- **Floating Animation**: Opportunities gently float up and down
- **Rotation Animation**: Elements rotate subtly for dynamic feel
- **Pulse Animation**: UI elements pulse with life
- **Blinking Eyes**: Agent blinks occasionally for realism

### Screen Effects
- **Screen Shake**: Intensity varies based on action importance
- **Flash Effects**: White flash for significant events
- **Gradient Backgrounds**: Smooth color transitions
- **Alpha Blending**: Transparent overlays for depth

## 🔧 Customization

### Adjusting Visual Effects
```python
# In advanced_rendering.py
class AdvancedRenderer:
    def __init__(self, window_size=800):
        # Modify animation speeds
        self.animation_speed = 0.1
        self.pulse_animation = 0
        self.float_animation = 0
        self.rotation_animation = 0
```

### Changing Colors
```python
# Customize the color scheme
self.colors = {
    'background': (240, 248, 255),  # AliceBlue
    'agent': (65, 105, 225),        # RoyalBlue
    'course': (34, 139, 34),        # ForestGreen
    # ... add your colors
}
```

### Adjusting Gameplay
```python
# In advanced_env.py
class AdvancedCareerEnv:
    def __init__(self, render_mode=None, window_size=800):
        self.grid_size = 8           # Change grid size
        self.max_steps = 200         # Adjust time limit
        # Modify rewards in step() method
```

## 🎯 Training Tips

### For RL Agents
1. **Start Simple**: Use the basic environment first
2. **Gradual Complexity**: Move to enhanced, then advanced
3. **Visual Feedback**: Use render mode during training
4. **Reward Shaping**: The environment provides rich reward signals

### For Human Players
1. **Plan Your Route**: Opportunities are strategically placed
2. **Avoid Distractions**: They're often near opportunities
3. **Prioritize Internships**: Highest reward, but harder to reach
4. **Watch for Bonuses**: Consecutive positive actions pay off

## 🐛 Troubleshooting

### Common Issues
1. **Pygame Not Found**: Install with `pip install pygame`
2. **Performance Issues**: Reduce window size or disable effects
3. **Visual Glitches**: Update your graphics drivers

### Performance Optimization
```python
# For better performance
env = AdvancedCareerEnv(render_mode=None)  # No rendering
env = AdvancedCareerEnv(window_size=400)   # Smaller window
```

## 🎨 Future Enhancements

- [ ] Real image assets for opportunities
- [ ] Sound effects and music
- [ ] Multiple difficulty levels
- [ ] Save/load game states
- [ ] Multiplayer support
- [ ] Custom themes and skins

## 📊 Performance Metrics

The enhanced environment maintains the same RL interface while providing:
- **60 FPS** smooth animations
- **Particle effects** with physics simulation
- **Real-time visual feedback**
- **Strategic gameplay elements**

## 🤝 Contributing

Feel free to enhance the environment with:
- New visual effects
- Additional game mechanics
- Improved AI behaviors
- Better UI elements

## 📝 License

This project is open source. Feel free to use and modify for your RL research and educational purposes.

---

**Enjoy exploring the enhanced career environment! 🚀** 