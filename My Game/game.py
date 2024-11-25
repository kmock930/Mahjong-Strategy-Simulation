from Card import Card
from player import Player
from gameLog import GameLog
import random
# RLCard
import rlcard
from rlcard.games.mahjong.game import MahjongGame as Game

# for debugging
import importlib
import gameLog
import player
importlib.reload(gameLog)
importlib.reload(player)

class CustomGame(Game):
    '''
    Mahjong Game Environment
    '''
    discardedTiles: list = []
    players: list[Player] = []
    unseenTiles: list[Card] = []
    game: Game = None
    logger: GameLog = None

    def __init__(self, experiment: bool = False, players: list[Player] = None, gameID: int = 1):
        self.game = rlcard.make('mahjong').game
        self.logger = GameLog(gameID=gameID)
        # init players
        self.logger.log("Initializing players...")
        self.players = players if players is not None and len(players) > 0 else [
            Player(1, '東', [], logger=self.logger),
            Player(2, '南', [], logger=self.logger),
            Player(3, '西', [], logger=self.logger),
            Player(4, '北', [], logger=self.logger)
        ]
        self.init_tiles()
        
        if experiment:
            self.logger.log("Saving Unseen Tiles before shuffling...")
            self.saveUnseenTiles(shuffled=False)
        
        self.shuffle()
        
        if experiment:
            self.logger.log("Saving Unseen Tiles after shuffling...")
            self.saveUnseenTiles(shuffled=True)
        
        self.deal()

    def init_tiles(self):
        '''
        Initialize the tiles
        '''
        self.logger.log("Initializing tiles...")
        # for loop to create normal tiles
        for suit in ['萬', '筒', '索']:
            for rank in range(1, 10):
                for _ in range(4):
                    self.unseenTiles.append(Card(
                        suit=suit,
                        rank=rank
                    ))
        # honor tiles
        for rank in ['東', '南', '西', '北', '中', '發', '白']:
            for _ in range(4):
                self.unseenTiles.append(Card(
                    suit='風' if rank in ['東', '南', '西', '北'] else '箭',
                    rank=rank
                ))
        # flower tiles
        for rank in ['春', '夏', '秋', '冬', '梅', '蘭', '竹', '菊']:
            self.unseenTiles.append(Card(
                suit='花',
                rank=rank
            ))

    def saveUnseenTiles(self, shuffled: bool = True):
        filename = "totalCards.txt" if shuffled is False else "shuffledCards.txt"
        with open(filename, 'w', encoding="utf-8") as f:
            for tile in self.unseenTiles:
                suit = tile.suit
                rank = tile.rank
                f.write(f"{rank} {suit}\n")

    def shuffle(self):
        random.shuffle(self.unseenTiles)

    def handleFlowers(self):
        self.logger.log("Handling Flower Tiles...")
        hasFlower: list[bool] = [True, True, True, True]
        while (all(hasFlower)==True):
            for playerID in range(len(self.players)):
                player = self.players[playerID]
                hand_copy = player.hand[:]
                for handPosition, tile in enumerate(hand_copy):
                    if tile.suit == '花':
                        self.logger.log(f"Player {player.Id} has a flower tile: {tile.rank} {tile.suit}, at position {handPosition}")
                        player.showFlower(player.hand.index(tile))
                        self.discardedTiles.append(tile)
                        # draw a tile from the back if available
                        if self.unseenTiles:
                            player.draw(self.unseenTiles.pop())
                        else:
                            self.logger.log("No more tiles to draw.")
                # check if a player's hand still has flower tiles
                hasFlower[playerID] = any(tile.suit == '花' for tile in player.hand)

    def deal(self):
        '''
        Deal 13 tiles to each player (init)
        '''
        self.logger.log("Dealing tiles to Each Player...")
        # Each player draws 13 tiles
        for player in self.players:
            player.hand = [self.unseenTiles.pop() for _ in range(13)]
        
        # deal with flower tiles from each player
        self.handleFlowers()
        
        # write player's hand to file
        for player in self.players:
            filename = f"player{player.Id}-hand.txt"
            with open(filename, 'w', encoding="utf-8") as f:
                for tile in player.hand:
                    suit = tile.suit
                    rank = tile.rank
                    f.write(f"{rank} {suit}\n")
        
        return [tile for tile in [player.hand for player in self.players]]

    def play(self, playerID: int, oppDiscardTile: Card = None):
        # player draws a tile
        if len(self.unseenTiles) > 0:
            newTile: Card = self.unseenTiles.pop(0) #牌頭
            self.players[playerID-1].draw(newTile)
        else: 
            self.logger.log("Game Ended.")

        # handle flower tiles
        self.handleFlowers()

        # player discards a tile according to his own strategy
        discardedTile = self.players[playerID-1].discard()
        self.discardedTiles.append(discardedTile)

        # handle special actions for each player
        for i in range(len(self.players)):
            if i != playerID - 1: # not current player
                specialAction: str | None = self.players[i].handleSpecialActions(
                    tile=discardedTile,
                    oppID=playerID
                )
                if specialAction is not None:
                    self.logger.log(f"Player {self.players[i].Id} {specialAction}!")
                    # change the order to the player who took the special action
                    return self.play(self.players[i].Id, discardedTile)

    def run(self):
        '''
        Run the game
        '''
        self.logger.log("Starting game run...")
        currentPlayerIndex = 0
        while len(self.unseenTiles) > 0:
            self.logger.log(f"Player {self.players[currentPlayerIndex].Id}'s turn")
            self.play(self.players[currentPlayerIndex].Id)
            currentPlayerIndex = (currentPlayerIndex + 1) % len(self.players)
        self.logger.log("Game run ended.")

    def reset(self):
        '''
        Reset the game state
        '''
        self.unseenTiles = []
        self.discardedTiles = []
        self.init_tiles()
        self.shuffle()
        self.deal()

    def shift_winds(self):
        '''
        Shift the winds of the players
        '''
        winds = ['東', '南', '西', '北']
        for player in self.players:
            current_wind_index = winds.index(player.wind)
            player.wind = winds[(current_wind_index + 1) % len(winds)]

def main():
    num_games = 4  # Number of games to run

    for iteration in range(num_games):
        game = CustomGame(
            experiment=True,
            gameID=iteration+1
        )

        game.logger.log(f"Starting Game {iteration+1}")

        # player logs
        logString:str = ""
        for playerID, player in enumerate(game.players):
            logString:str = logString + f"Wind Player {playerID+1}: {player.wind} "
        game.logger.log(logString)
        
        game.run()
        game.reset()
        game.shift_winds()
        game.logger.log_end()

if __name__ == "__main__":
    main()