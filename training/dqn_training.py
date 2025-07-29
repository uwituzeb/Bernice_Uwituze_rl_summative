from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.custom_env import CustomEnv

def train_dqn():
    env = CustomEnv(render_mode="human")
    model = DQN("MlpPolicy", 
                env, 
                verbose=1,
                learning_rate=1e-4, 
                buffer_size=10000,
                exploration_fraction=0.1, 
                exploration_final_eps=0.02, 
                train_freq=4, 
                target_update_interval=100, 
                tensorboard_log="./dqn_tensorboard/")

    model.learn(total_timesteps=25000)

    model.save("models/dqn/custom_env_dqn")
    print("DQN training complete and model saved!")

if __name__ == "__main__":
    train_dqn()