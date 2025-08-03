from stable_baselines3 import PPO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.custom_env import CustomCareerEnv
from stable_baselines3.common.callbacks import EvalCallback

def train_pg():
    env = CustomCareerEnv(render_mode="human")

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=4096,
        batch_size=128,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        tensorboard_log="./ppo_tensorboard/"
    )

    model.learn(
       total_timesteps=100000
    )

    model.save("models/ppo/custom_env_ppo")
    print("PPO training complete and model saved!")


if __name__ == "__main__":
    train_pg()