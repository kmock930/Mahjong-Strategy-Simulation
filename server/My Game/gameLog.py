import datetime

class GameLog:
    def __init__(self, gameID: int):
        self.log_file = f"game{gameID}_log.txt"
        self.file = open(self.log_file, 'w', encoding="utf-8")
        self.start_time = datetime.datetime.now()
        self.file.write(f"Game Log Initialized for Game {gameID}\n")
        self.file.write(f"Start Time: {self.start_time.strftime('%d-%b-%Y (%H:%M:%S.%f)')}\n\n")

    def log(self, message: str):
        self.file.write(f"{datetime.datetime.now().strftime('%d-%b-%Y (%H:%M:%S.%f)')}: {message}\n")

    def log_move(self, player, move):
        self.log(f"Player {player} made move: {move}")

    def log_winner(self, player):
        self.log(f"Player {player} won the game")

    def log_end(self):
        end_time = datetime.datetime.now()
        game_time_elapsed = end_time - self.start_time
        self.file.write("\n")
        self.file.write("Game Ended\n")
        self.file.write(f"End Time: {end_time.strftime('%d-%b-%Y (%H:%M:%S.%f)')}\n\n")
        self.file.write(f"Game Time Elapsed: {game_time_elapsed}\n")
        self.file.write("End of Game\n")
        self.file.close()

def main():
    game_log = GameLog(1)
    game_log.log("Game started")
    game_log.log_move(1, "Draw tile")
    game_log.log_move(2, "Discard tile")
    game_log.log_winner(1)
    game_log.log_end()

if __name__ == "__main__":
    main()