from training.dqn_training import train_dqn
from training.ppo_pg_training import train_pg
from training.reinfore_pg_training import train_reinforce
from training.a2c_pg_training import train_a2c

def main():
    print("=== RL Training Experiment Runner ===")
    print("Choose training method:")
    print("1: DQN")
    print("2: PPO (Policy Gradient)")
    print("3: REINFORCE (Policy Gradient)")
    print("4: A2C (Advantage Actor-Critic)")

    choice = input("Enter your choice (1-4): ").strip()
    if choice == "1":
        train_dqn()
    elif choice == "2":
        train_pg()
    elif choice == "3":
        train_reinforce()
    elif choice == "4":
        train_a2c()
    else:
        print("Invalid choice. Please select a valid training method.")

if __name__ == "__main__":
    main()