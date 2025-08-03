from stable_baselines3 import A2C
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.custom_env import CustomCareerEnv

def train_a2c():
    env = CustomCareerEnv(render_mode="human")

    model = A2C(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=7e-4,
        gamma=0.99,
        n_steps=5,
        ent_coef=0.01,
        vf_coef=0.5,
        tensorboard_log="./a2c_tensorboard/"
    )

    model.learn(total_timesteps=25000)
    model.save("models/a2c/custom_env_a2c")
    print("A2C training complete and model saved!")

if __name__ == "__main__":
    train_a2c()