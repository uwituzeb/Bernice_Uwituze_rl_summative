# Custom RL environment: Career Planning Simulator

## Project Overview

This project simulates an agent navigating career choices to maximize long-term rewards. The environment emulates realistic decision-making steps in a professional path, including choices on education, training, and job roles.

## Key Features:

- Custom career simulation environment with realistic long-term consequences

- Multiple RL algorithms: DQN, PPO, A2C, REINFORCE

- Monitoring and visualization via TensorBoard and custom reward tracking

- Dense reward shaping to improve training signal

- Replayable and testable environment to benchmark generalization and stability

## Project Structure

```
career-rl/
├── environment/
│   └── custom_env.py                # Custom Career RL 
│    └── custom_env.py              # Visualization GUI components
├── training/
│   ├── dqn_training.py                 # Deep Q-Network training
│   ├── ppo_pg_training.py                 # Proximal Policy 
│   ├── train_a2c.py                 # Advantage Actor-Critic
│   └── train_reinforce.py          # REINFORCE policy gradient
├── models/                          # Trained model weights
├── logs/                            # Monitor logs (reward, length)
├── dqn_tensorboard/                 # TensorBoard logs for DQN
├── a2c_tensorboard/                 # TensorBoard logs for A2C
└── requirements.txt                 # Dependencies

```


## Project Setup

1. Clone the repository:

```
git clone https://github.com/uwituzeb/Bernice_Uwituze_rl_summative.git
cd Bernice_Uwituze_rl_summative
```


2. Activate the virtual environment:

```
py -m venv venv
source venv/Scripts/Activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Running the Demo

```
python main.py
```

5. Cumulative Reward Interpretations

To generate plots showing cumulative rewards over episodes for all methods, run:

```
python plot_rewards.py
```

## Cumulative Reward Plot Interpretation

![Cumulative Rewards](https://raw.githubusercontent.com/uwituzeb/Bernice_Uwituze_rl_summative/main/cumulative_rewards_plot.png)

- **DQN**: Our DQN training showed steady growth with the agent consistenly learning and collecting positive rewards
- **PPO**: Our PPO algorithm seemed to outperform all other methods with a quick reward collection as shown by the sharp upward slope.
- **A2C**: Our A2C algorithm started off well but quickly stagnated showing that there may have been early convergence
- **REINFORCE**: This method only returned negative rewards, which goes to show that the model was not improving and may require more tuning to improve.

