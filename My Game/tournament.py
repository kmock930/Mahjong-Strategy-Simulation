from rlcard.envs import Env
from rlcard.agents.random_agent import RandomAgent
from game import CustomGame

class tournament(Env):
    env = Env(game=CustomGame(
        experiment=True
    ))
    env.set_agents([RandomAgent(env.action_num) for _ in range(env.player_num)]) 
    env.run(is_training=False)

    def __init__(self):
        pass

    def run(self, is_training=False):
        return super().run(is_training)

def main():
    env = tournament()
if __name__ == "__main__":
    main()
