import datetime

class GameLog:
    def __init__(self, log_file='game_log.txt'):
        self.log_file = log_file
        with open(self.log_file, 'w') as file:
            file.write("Game Log Initialized\n")
            file.write(f"Start Time: {datetime.datetime.now()}\n\n")

    def log(self, message):
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(f"{datetime.datetime.now()}: {message}\n")

    def log_move(self, player, move):
        self.log(f"Player {player} made move: {move}")

    def log_winner(self, player):
        self.log(f"Player {player} won the game", encoding='utf-8')

# Example usage
if __name__ == "__main__":
    game_log = GameLog()
    game_log.log("Game started")
    game_log.log_move(1, "Draw tile")
    game_log.log_move(2, "Discard tile")
    game_log.log_winner(1)