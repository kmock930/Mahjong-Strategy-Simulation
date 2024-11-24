from Card import Card;
from player import Player;
import random;
# RLCard
import rlcard;
from rlcard.games.mahjong.game import MahjongGame as Game;
from rlcard.games.mahjong.utils import init_deck;

class CustomGame(Game):
    '''
    Mahjong Game Environment
    '''
    discardedTiles: list = [];
    players: list[Player] = [];
    unseenTiles: list[Card] = [];

    def __init__(self, experiment: bool = False, players: list[Player] = []):
        self.game = rlcard.make('mahjong').game;
        # init players
        self.players = players if len(players) > 0 else [
            Player(1, '東', []),
            Player(2, '南', []),
            Player(3, '西', []),
            Player(4, '北', [])
        ]
        self.init_tiles();
        
        if experiment:
            self.saveUnseenTiles(shuffled=False)
        
        self.shuffle()
        
        if experiment:
            self.saveUnseenTiles(shuffled=True)
        
        self.deal()

    def init_tiles(self):
        '''
        Initialize the tiles
        '''
        # for loop to create normal tiles
        for suit in ['萬', '筒', '索']:
            for rank in range(1, 10):
                for _ in range(4):
                    self.unseenTiles.append(Card(
                        suit=suit,
                        rank=rank
                    ));
        # honor tiles
        for rank in ['東', '南', '西', '北', '中', '發', '白']:
            for _ in range(4):
                self.unseenTiles.append(Card(
                    suit='風' if suit in ['東', '南', '西', '北'] else '箭',
                    rank=rank
                ));
        # flower tiles
        for rank in ['春', '夏', '秋', '冬', '梅', '蘭', '竹', '菊']:
            self.unseenTiles.append(Card(
                suit='花',
                rank=rank
            ));

    def saveUnseenTiles(self, shuffled: bool = True):
        filename = "totalCards.txt" if shuffled is False else "shuffledCards.txt"
        with open(filename, 'w', encoding="utf-8") as f:
            for tile in self.unseenTiles:
                suit = tile.suit;
                rank = tile.rank;
                f.write(f"{rank} {suit}\n")

    def shuffle(self):
        random.shuffle(self.unseenTiles)

    def handleFlowers(self):
        hasFlower: list[bool] = [True, True, True, True]
        while (all(hasFlower)==True):
            for playerID in range(len(self.players)):
                player = self.players[playerID]
                hand_copy = player.hand[:]
                for handPosition, tile in enumerate(hand_copy):
                    if tile.suit == '花':
                        print(f"Player {player.Id} has a flower tile: {tile.rank} {tile.suit}, at position {handPosition}")
                        player.showFlower(player.hand.index(tile))
                        self.discardedTiles.append(tile)
                        # draw a tile from the back
                        player.draw(self.unseenTiles.pop())
                # check if a player's hand still has flower tiles
                hasFlower[playerID] = any(tile.suit == '花' for tile in player.hand)

    def deal(self):
        '''
        Deal 13 tiles to each player (init)
        '''
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
                    suit = tile.suit;
                    rank = tile.rank;
                    f.write(f"{rank} {suit}\n")
        
        return [tile for tile in [player.hand for player in self.players]]

    def play(self, playerID: int):
        print(f"Player {playerID} is playing.")
        print(f"Original Tiles:")
        for tile in self.players[playerID-1].hand:
            print(f"{tile.rank} {tile.suit}")
        # player draws a tile
        if (len(self.unseenTiles) > 0):
            newTile: Card = self.unseenTiles.pop()
            self.players[playerID-1].draw(newTile)
        else: 
            print("Game Ended.")

        # handle flower tiles
        self.handleFlowers()

        # player discards a tile according to his own strategy
        self.discardedTiles.append(
            self.players[playerID-1].discard()
        )

        print(f"Player {playerID} has discarded a tile: {self.discardedTiles[-1].rank} {self.discardedTiles[-1].suit}")
        print(f"Resulting Tiles:")
        for tile in self.players[playerID-1].hand:
            print(f"{tile.rank} {tile.suit}")

    def run(self):
        '''
        Run the game
        '''
        # play the game
        # 1 round simulation
        for player in self.players:
            self.play(player.Id)

def main():
    game = CustomGame(experiment=True);
    game.run();

if __name__ == "__main__":
    main()