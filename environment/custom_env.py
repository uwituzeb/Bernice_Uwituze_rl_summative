import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random
import time
from .rendering import Rendering
import imageio

pygame.init()

class CustomCareerEnv(gym.Env):
    metadata = {
        "render_modes": ["human"],
        "render_fps": 15
    }

    def __init__(self, render_mode=None, window_size=800, record_gif=False, gif_path="career_env_demo.gif"):
        super().__init__()
        self.grid_size = 8
        self.max_steps = 200
        self.steps_taken = 0
        self.readiness_score = 0
        self.window_size = window_size
        self.agent_location = [0, 0]
        self.opportunity_cells = [] 
        self.distraction_cells = []
        self.render_mode = render_mode
        self.renderer = Rendering(window_size)
        self.last_time = time.time()
        self.last_reward = 0
        self.consecutive_positive_rewards = 0
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([self.grid_size-1, self.grid_size-1, 100]),
            dtype=np.float32
        )
        self.window = None
        self.clock = None
        self.record_gif = record_gif
        self.gif_path = gif_path
        self.frames = []

    def _get_observation(self):
        return np.array([self.agent_location[0], self.agent_location[1], self.readiness_score], dtype=np.float32)

    def _generate_opportunities(self):
        possible = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                    if (i, j) != tuple(self.agent_location)]
        random.shuffle(possible)
        # Single job goal in bottom-right quadrant
        candidates = [(i, j) for i in range(self.grid_size//2, self.grid_size) 
                     for j in range(self.grid_size//2, self.grid_size)]
        candidates = [pos for pos in candidates if pos in possible]
        if candidates:
            pos = random.choice(candidates)
            return [{"pos": pos, "type": "job"}]
        return []

    def _generate_distractions(self):
        possible = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                    if (i, j) != tuple(self.agent_location) and
                    all((i, j) != opp["pos"] for opp in self.opportunity_cells)]
        random.shuffle(possible)
        distraction_types = ["phone", "drugs_alcohol", "social_media"]
        distractions = []
        num_distractions = 3
        for i, dist_type in enumerate(distraction_types):
            if possible:
                pos = possible.pop(0)
                distractions.append({"pos": pos, "type": dist_type})
        return distractions

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_location = [0, 0]
        self.steps_taken = 0
        self.readiness_score = 0
        self.opportunity_cells = self._generate_opportunities()
        self.distraction_cells = self._generate_distractions()
        self.last_time = time.time()
        self.last_reward = 0
        self.consecutive_positive_rewards = 0
        self.frames = []
        if self.render_mode == "human":
            self.render()
        return self._get_observation(), {}

    def step(self, action):
        self.steps_taken += 1
        reward = 0.0  # Removed -0.1 step penalty
        done = False
        truncated = False
        prev_pos = self.agent_location.copy()
        if action == 0 and self.agent_location[0] > 0:
            self.agent_location[0] -= 1
        elif action == 1 and self.agent_location[0] < self.grid_size - 1:
            self.agent_location[0] += 1
        elif action == 2 and self.agent_location[1] > 0:
            self.agent_location[1] -= 1
        elif action == 3 and self.agent_location[1] < self.grid_size - 1:
            self.agent_location[1] += 1
        elif action == 4:
            for opp in self.opportunity_cells[:]:
                if tuple(self.agent_location) == opp["pos"]:
                    reward = 25.0
                    self.readiness_score += 25
                    x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
                    y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
                    self.renderer.add_particles(x, y, self.renderer.colors['particle_job'], 20)
                    self.renderer.trigger_screen_shake(10)
                    self.renderer.trigger_flash(0.5)
                    self.opportunity_cells.remove(opp)
                    break
        for dist in self.distraction_cells:
            if tuple(self.agent_location) == dist["pos"]:
                reward = -8.0
                self.readiness_score = max(0, self.readiness_score - 8)
                self.agent_location = prev_pos
                x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
                y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
                particle_color = self.renderer.colors[f'particle_{dist["type"]}']
                self.renderer.add_particles(x, y, particle_color, 8)
                self.renderer.trigger_screen_shake(8)
                self.renderer.trigger_flash(0.5)
                break
        if reward > 0:
            self.consecutive_positive_rewards += 1
            if self.consecutive_positive_rewards >= 3:
                reward += 2.0
                self.consecutive_positive_rewards = 0
        else:
            self.consecutive_positive_rewards = 0
        if self.steps_taken >= self.max_steps:
            truncated = True
        if len(self.opportunity_cells) == 0:
            done = True
            reward += 25.0
            self.renderer.trigger_screen_shake(15)
            self.renderer.trigger_flash(1.0)
        self.last_reward = reward
        if self.render_mode == "human":
            self.render()
        return self._get_observation(), reward, done, truncated, {}

    def render(self):
        if self.window is None and self.render_mode == "human":
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            pygame.display.set_caption("Career Path Environment - Random Demo")
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        current_time = time.time()
        dt = current_time - self.last_time
        self.renderer.update_animations(dt)
        self.last_time = current_time
        canvas = self.renderer.draw_environment(
            self.window,
            self.agent_location,
            self.opportunity_cells,
            self.distraction_cells,
            self.readiness_score,
            self.steps_taken,
            self.max_steps
        )
        self.window.blit(canvas, canvas.get_rect())
        if self.record_gif and self.steps_taken % 2 == 0:  # Capture every other frame
            frame = pygame.surfarray.array3d(canvas)
            frame = np.transpose(frame, (1, 0, 2))
            self.frames.append(frame)
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            if self.record_gif and self.frames:
                imageio.mimsave(self.gif_path, self.frames, fps=15)
                print(f"GIF saved to {self.gif_path}")
            pygame.display.quit()
            self.window = None
        pygame.quit()

# DEMO with random actions
if __name__ == "__main__":
    env = CustomCareerEnv(render_mode="human", window_size=800, record_gif=True, gif_path="career_env_demo.gif")
    obs, info = env.reset()
    done = False
    truncated = False

    print("🚀 Career Path Environment Random Demo")

    while not (done or truncated):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
        if done or truncated:
            break
        action = env.action_space.sample()  # Random action
        obs, reward, done, truncated, info = env.step(action)
        if reward != 0.0:
            print(f"Action: {action}, Reward: {reward:.1f}, Score: {env.readiness_score}")
        time.sleep(0.3)  # Increased delay for slower movement visibility
    print(f"\n🎉 Final Score: {env.readiness_score}")
    print(f"Steps Taken: {env.steps_taken}")
    print(f"Job Goal Reached: {len(env.opportunity_cells) == 0}")
    print("Press the window's close button to exit...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                exit()
        env.render()
        pygame.event.pump()
        pygame.display.update()
        env.clock.tick(15)