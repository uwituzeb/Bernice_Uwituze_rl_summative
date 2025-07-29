import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random
from rendering import draw_environment

class CustomEnv(gym.Env):
    """A custom environment simulating a student navigating career opportunities."""
    metadata = {
        "render_modes": ["human"],
        "render_fps": 4
    }
    
    def __init__(self, render_mode=None):
        super().__init__()
        self.grid_size = 5
        self.max_steps = 100
        self.steps_taken = 0
        self.career_score = 0

        self.agent_location = [0, 0]  # Starting position
        self.target_location = [self.grid_size - 1, self.grid_size - 1]  # Target position
        self.obstacles = []
        
        # Discrete actions: 0=Up, 1=Down, 2=Left, 3=Right, 4=Take Opportunity
        self.action_space = spaces.Discrete(5)
        
        # Observation space: agent position (x,y), target position (x,y), career score
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0]),
            high=np.array([self.grid_size-1, self.grid_size-1, self.grid_size-1, self.grid_size-1, 100]),
            dtype=np.float32
        )
        
        # Pygame visualization
        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.cell_size = 100
        self.window_size = self.grid_size * self.cell_size

    def _get_observation(self):
        """Return current state: agent position, target position, career score."""
        return np.array([self.agent_location[0], self.agent_location[1], 
                        self.target_location[0], self.target_location[1], 
                        self.career_score], dtype=np.float32)
        
    
    def _generate_obstacles(self):
        """Generate random obstacles (distractions) excluding start and target positions."""
        possible_positions = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                              if (i, j) != tuple(self.agent_location) and (i, j) != tuple(self.target_location)]
        return random.sample(possible_positions, k=random.randint(3, 6))
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_location = [0, 0]
        self.target_location = [self.grid_size - 1, self.grid_size - 1]
        self.obstacles = self._generate_obstacles()
        self.steps_taken = 0
        self.career_score = 0
        
        
        if self.render_mode == "human":
            self.render()

        return self._get_observation(), {}
    
    
    def step(self, action):
        """Execute one step in the environment."""
        self.steps_taken += 1
        reward = -0.1
        done = False
        truncated = False
        prev_pos = self.agent_location.copy()

        # Movement actions
        if action == 0 and self.agent_location[0] > 0:  # Up
            self.agent_location[0] -= 1
        elif action == 1 and self.agent_location[0] < self.grid_size - 1:  # Down
            self.agent_location[0] += 1
        elif action == 2 and self.agent_location[1] > 0:  # Left
            self.agent_location[1] -= 1
        elif action == 3 and self.agent_location[1] < self.grid_size - 1:  # Right
            self.agent_location[1] += 1
        elif action == 4:  # Take Opportunity
            if self.agent_location == self.target_location:
                reward = 10.0
                self.career_score += 10
                done = True
        
        # Check for obstacles
        if tuple(self.agent_location) in self.obstacles:
            reward = -1.0
            self.career_score -= 2
            self.agent_location = prev_pos

        # Check if max steps reached
        if self.steps_taken >= self.max_steps:
            truncated = True

        if self.render_mode == "human":
            self.render()

        return self._get_observation(), reward, done, truncated, {}

    def render(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = draw_environment(
        self.window,
        self.grid_size,
        self.cell_size,
        self.agent_location,
        self.target_location,
        self.obstacles
    )

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))

    def close(self):
        """Close the Pygame window."""
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

# Demonstration of random actions
if __name__ == "__main__":
    env = CustomEnv(render_mode="human")
    obs, info = env.reset()
    done = False
    truncated = False
    
    for _ in range(100):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                break
        
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}")

        if done or truncated:
            print("Episode finished.")
            obs, info = env.reset()
    
    env.close()
