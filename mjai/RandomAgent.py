import random
import mjai
import json
import sys

class RandomAgent:
    def __init__(self):
        self.actions = [
            "discard", "tsumo", "ron", "pon", "chi", "kan", "reach"
        ]

    def choose_action(self, state):
        return random.choice(self.actions)

if __name__ == "__main__":
    agent = RandomAgent()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        event = json.loads(line)
        agent.handle_event(event)
        action = agent.choose_action(event)
        if action:
            print(json.dumps(action))
            sys.stdout.flush()