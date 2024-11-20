import mjai
import json
import sys

class SimpleAgent:
    def __init__(self):
        self.hand = []

    def handle_event(self, event):
        if event['type'] == 'start_game':
            self.hand = []
        elif event['type'] == 'tsumo':
            self.hand.append(event['pai'])
        elif event['type'] == 'dahai':
            if event['actor'] == 0:
                self.hand.remove(event['pai'])

    def choose_action(self, event):
        if event['type'] == 'tsumo':
            return {
                'type': 'dahai',
                'pai': self.hand[-1],
                'actor': 0
            }
        return None

if __name__ == "__main__":
    agent = SimpleAgent()
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