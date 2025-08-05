import pandas as pd
import matplotlib.pyplot as plt
import os

def load_rewards(file_path, is_monitor=True):
    if not os.path.exists(file_path):
        return None
    if is_monitor:
        df = pd.read_csv(file_path, skiprows=1)
    else:
        df = pd.read_csv(file_path)
    return df['r'].cumsum()

def plot_rewards():
    methods = {
        "DQN":      ("./logs/monitor.csv", True),
        "PPO":      ("./logs/ppo_monitor.csv", True),
        "A2C":      ("./logs/a2c_monitor.csv", True),
        "REINFORCE":("./logs/reinforce_rewards.csv", False),
    }

    plt.figure(figsize=(12, 6))
    for name, (path, is_monitor) in methods.items():
        rewards = load_rewards(path, is_monitor)
        if rewards is not None:
            plt.plot(rewards, label=name)

    plt.title("Cumulative Reward Over Episodes")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative Reward")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cumulative_rewards_plot.png")
    plt.show()

if __name__ == "__main__":
    plot_rewards()