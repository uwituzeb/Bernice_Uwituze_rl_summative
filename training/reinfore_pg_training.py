import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.distributions import Categorical
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.custom_env import CustomCareerEnv

class PolicyNetwork(nn.Module):
    def __init__(self, obs_size, n_actions):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(obs_size, 128),
            nn.ReLU(),
            nn.Linear(128, n_actions),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.fc(x)

def train_reinforce(episodes=500):
    env = CustomCareerEnv()
    
    # Handle environments with tuple observation space
    sample_obs = env.reset()
    sample_obs = sample_obs[0] if isinstance(sample_obs, tuple) else sample_obs
    obs_size = np.array(sample_obs).shape[0]
    n_actions = env.action_space.n

    policy = PolicyNetwork(obs_size, n_actions)
    optimizer = optim.Adam(policy.parameters(), lr=1e-2)
    gamma = 0.99

    for episode in range(episodes):
        reset_output = env.reset()
        state = reset_output[0] if isinstance(reset_output, tuple) else reset_output

        log_probs = []
        rewards = []
        done = False

        while not done:
            # Ensure state is a NumPy array
            state = np.array(state, dtype=np.float32)
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

            probs = policy(state_tensor)
            dist = Categorical(probs)
            action = dist.sample()

            step_output = env.step(action.item())

            # Handle both Gym API formats
            if len(step_output) == 5:
                next_state, reward, terminated, truncated, _ = step_output
                done = terminated or truncated
            else:
                next_state, reward, done, _ = step_output

            log_probs.append(dist.log_prob(action))
            rewards.append(reward)
            state = next_state

        # Compute returns
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)

        loss = -torch.sum(torch.stack(log_probs) * returns)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Episode {episode + 1}, Total reward: {sum(rewards)}")

    torch.save(policy.state_dict(), "models/reinforce_policy.pth")
    print("REINFORCE training complete and model saved!")

if __name__ == "__main__":
    train_reinforce()
