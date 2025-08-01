import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random
import time
from rendering import Rendering
import imageio

pygame.init()

class CustomCareerEnv(gym.Env):
    metadata = {
        "render_modes": ["human"],
        "render_fps": 30  # Lower FPS for clearer visualization
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
        types = ["course", "extracurricular", "internship"]
        possible = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                    if (i, j) != tuple(self.agent_location)]
        random.shuffle(possible)
        opportunities = []
        for i, opp_type in enumerate(types):
            if i == 0:
                candidates = [(i, j) for i in range(0, self.grid_size//2) 
                            for j in range(0, self.grid_size//2)]
            elif i == 1:
                candidates = [(i, j) for i in range(0, self.grid_size//2) 
                            for j in range(self.grid_size//2, self.grid_size)]
            else:
                candidates = [(i, j) for i in range(self.grid_size//2, self.grid_size) 
                            for j in range(self.grid_size)]
            candidates = [pos for pos in candidates if pos in possible]
            if candidates:
                pos = random.choice(candidates)
                opportunities.append({"pos": pos, "type": opp_type})
                possible.remove(pos)
        return opportunities

    def _generate_distractions(self):
        possible = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)
                    if (i, j) != tuple(self.agent_location) and
                    all((i, j) != opp["pos"] for opp in self.opportunity_cells)]
        distractions = []
        num_distractions = 6  # Reduced for better navigation
        for opp in self.opportunity_cells:
            i, j = opp["pos"]
            nearby = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
            nearby = [pos for pos in nearby if pos in possible and pos not in distractions]
            if nearby and len(distractions) < num_distractions // 2:
                distractions.append(random.choice(nearby))
        remaining = [pos for pos in possible if pos not in distractions]
        if remaining:
            additional = random.sample(remaining, min(num_distractions - len(distractions), len(remaining)))
            distractions.extend(additional)
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
        reward = -0.1
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
                    if opp["type"] == "internship":
                        reward = 15.0
                        self.readiness_score += 15
                        x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
                        y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
                        self.renderer.add_particles(x, y, self.renderer.colors['particle_internship'], 20)
                        self.renderer.trigger_screen_shake(5)
                        self.renderer.trigger_flash(0.3)
                    elif opp["type"] == "course":
                        reward = 10.0
                        self.readiness_score += 10
                        x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
                        y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
                        self.renderer.add_particles(x, y, self.renderer.colors['particle_course'], 15)
                        self.renderer.trigger_screen_shake(3)
                    elif opp["type"] == "extracurricular":
                        reward = 7.0
                        self.readiness_score += 7
                        x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
                        y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
                        self.renderer.add_particles(x, y, self.renderer.colors['particle_extracurricular'], 12)
                        self.renderer.trigger_screen_shake(2)
                    self.opportunity_cells.remove(opp)
                    break
        if tuple(self.agent_location) in self.distraction_cells:
            reward = -8.0
            self.readiness_score = max(0, self.readiness_score - 8)
            self.agent_location = prev_pos
            x = self.agent_location[1] * self.renderer.cell_size + self.renderer.cell_size // 2
            y = self.agent_location[0] * self.renderer.cell_size + self.renderer.cell_size // 2
            self.renderer.add_particles(x, y, self.renderer.colors['particle_distraction'], 8)
            self.renderer.trigger_screen_shake(8)
            self.renderer.trigger_flash(0.5)
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
            pygame.display.set_caption("Advanced Career Environment - Random Demo")
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
                imageio.mimsave(self.gif_path, self.frames, fps=15)  # Lower FPS for smaller GIF
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

    print("🚀 Advanced Career Environment Random Demo")
    print("=" * 60)
    print("Features:")
    print("  ✨ Particle effects on interactions")
    print("  🌊 Screen shake and flash effects")
    print("  🎨 Smooth animations and gradients")
    print("  🎯 Strategic placement of opportunities")
    print("  ⚡ Enhanced visual feedback")
    print("=" * 60)

    while not (done or truncated):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
        if done or truncated:
            break
        action = env.action_space.sample()  # Random action
        obs, reward, done, truncated, info = env.step(action)
        if reward != -0.1:
            print(f"Action: {action}, Reward: {reward:.1f}, Score: {env.readiness_score}")
        time.sleep(0.2)  # Slow down for visibility

    print(f"\n🎉 Final Score: {env.readiness_score}")
    print(f"Steps Taken: {env.steps_taken}")
    print(f"Opportunities Collected: {3 - len(env.opportunity_cells)}/3")
    print("Press the window's close button to exit...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                exit()
        env.render()
        pygame.event.pump()
        pygame.display.update()
        env.clock.tick(30)