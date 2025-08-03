from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.vec_env import VecNormalize
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from environment.custom_env import CustomCareerEnv

def train_dqn():
    env = DummyVecEnv([lambda: Monitor(CustomCareerEnv(render_mode="rgb_array"))])
    env = VecNormalize(env, norm_obs=True, norm_reward=False)
    eval_env = DummyVecEnv([lambda: Monitor(CustomCareerEnv(render_mode="rgb_array"))])
    eval_env = VecNormalize(eval_env, norm_obs=True, norm_reward=False)
    eval_env.training = False
    eval_env.norm_reward = False

    eval_callback = EvalCallback(
       eval_env,
        best_model_save_path='./models/dqn/best_model/',
        log_path='./logs/',
        eval_freq=5000,
        n_eval_episodes=5,
        deterministic=True,
        render=False,
        verbose=1, 
    )
    model = DQN(
        policy="MlpPolicy",
        env=env,
        learning_rate=5e-4,
        buffer_size=20000,
        learning_starts=5000,
        batch_size=64,
        gamma=0.99,
        exploration_initial_eps=1.0,
        exploration_fraction=0.2,
        exploration_final_eps=0.05,
        verbose=1,
        tensorboard_log="./dqn_tensorboard/"
    )

    model.learn(
        total_timesteps=200000,
        callback=eval_callback
    )

    model.save("models/dqn/custom_env_dqn")
    print("DQN training complete and model saved!")

if __name__ == "__main__":
    train_dqn()