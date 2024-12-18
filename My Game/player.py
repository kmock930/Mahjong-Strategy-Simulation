from Card import Card
from Rules import Rules
from gameLog import GameLog
import math
import random
from utils import find_possible_melds

class Player:
    '''
    A Player in a Mahjong Game
    '''
    Id: int = 0
    wind: str = '東'
    hand: list[Card] = []
    openHand: list[list[Card]] = []

    points: int = 0
    meld: list[Card] = []
    
    flowers: list[Card] = []
    hu: bool = False

    def __init__(self, Id: int, wind: str,  hand: list, logger: GameLog = None):
        self.Id = Id
        self.wind = wind
        self.hand = hand
        self.logger = logger

    def draw(self, tile: Card):
        self.hand.append(tile)
        return tile

    def pong(self, tile: Card):
        # obtain the tile from the discarded tile
        self.draw(tile)
        if (self.hand.count(tile) == 3):
            # remove the hand to the open tile as a meld
            self.hand.remove(tile)
            self.hand.remove(tile)
            self.hand.remove(tile)
            tile.toDisplay = True
            self.openHand.append([tile] * 3)
        else:
            raise ValueError("Cannot pong")
        self.logger.log_move(self.Id, f"pong {tile.suit}-{tile.rank}")
        return tile

    def chow(self, tile: Card, meld: list[Card]):
        # obtain the tile from the discarded tile
        self.draw(tile)
        if (tile.suit, tile.rank) not in [(t.suit, t.rank) for t in meld]:
            return None
        # remove the hand to the open tile as a meld
        self.hand = [
            tile
            for tile in self.hand
            if (tile.suit, tile.rank) not in [(t.suit, t.rank) for t in meld]
        ]
        for tile in meld:
            tile.toDisplay = True
        self.openHand.append(meld)
        self.logger.log_move(self.Id, f"chow {tile.suit}-{tile.rank}")
        return tile

    def kong(self, tile: Card):
        # obtain the tile from the discarded tile
        self.draw(tile)
        if (self.hand.count(tile) == 4):
            # remove the hand to the open tile as a meld
            self.hand.remove(tile)
            self.hand.remove(tile)
            self.hand.remove(tile)
            self.hand.remove(tile)
            tile.toDisplay = True
            self.openHand.append([tile] * 4)
        else:
            raise ValueError("Cannot kong")
        self.logger.log_move(self.Id, f"kong {tile.suit}-{tile.rank}")
        return tile

    def showFlower(self, tilePosition: int):
        tile = self.hand[tilePosition]
        self.flowers.append(tile)
        self.hand.pop(tilePosition)
        self.logger.log_move(self.Id, f"show flower {tile.suit}-{tile.rank}")
        return tile

    def canChow(self, deck: list[Card], tile: Card, oppID: int) -> bool:
        if tile.suit in ['花', '風', '箭']:
            return False
        if (oppID != (self.Id - 1) % 4): # not the previous player
            return False
        return (deck.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0 and
                deck.count(Card(suit=tile.suit, rank=tile.rank+2)) > 0) or \
                (deck.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0 and
                deck.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0) or \
                (deck.count(Card(suit=tile.suit, rank=tile.rank-2)) > 0 and
                deck.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0)

    def canPong(self, deck: list[Card], tile: Card) -> bool:
        return deck.count(tile) == 2

    def canGong(self, deck: list[Card], tile: Card) -> bool:
        return deck.count(tile) == 3

    def handleSpecialActions(self, tile: Card, oppID: int):
        if tile is None:
            return None
        if self.canChow(self.hand, tile, oppID):
            possible_melds = [
                [Card(tile.suit, tile.rank - 2), Card(tile.suit, tile.rank - 1), tile],
                [Card(tile.suit, tile.rank - 1), tile, Card(tile.suit, tile.rank + 1)],
                [tile, Card(tile.suit, tile.rank + 1), Card(tile.suit, tile.rank + 2)]
            ]
            hypotheticalHand = self.hand.copy()
            hypotheticalHand += [tile]
            possible_melds = [
                meld 
                for meld in possible_melds 
                if meld in find_possible_melds(hypotheticalHand)
            ]
            return self.chow(tile, random.choice(possible_melds))
        if self.canPong(self.hand, tile):
            return self.pong(tile)
        if self.canGong(self.hand, tile):
            return self.kong(tile)
        return None

    # default strategy (To be overriden by another class)
    def discard(self):
        self.logger.log_move(self.Id, f"discards a tile: {self.hand[len(self.hand)-1].suit}-{self.hand[len(self.hand)-1].rank}")
        self.logger.log(f"Original {len(self.hand)} Tiles:")
        for tile in self.hand:
            self.logger.log(f"{tile.suit} {tile.rank}")

        # by default it discards what is drawn (i.e., the new tile)
        tile = self.hand.pop(len(self.hand)-1)

        self.logger.log(f"Remaining {len(self.hand)} Tiles")
        for tile in self.hand:
            self.logger.log(f"{tile.suit} {tile.rank}")
        return tile

    def hu(self, incomingTile: Card, closedDeck: list[Card], incomingPlayerId: int, gameID: int, upperScoreLimit: int):
        rules = Rules(
            incomingTile=incomingTile,
            closedDeck=closedDeck,
            openDeck=self.openHand,
            incomingPlayerId=incomingPlayerId,
            flowerDeck=self.flowers,
            currentPlayerId=self.Id,
            gameID=gameID,
            upperScoreLimit=upperScoreLimit
        )
        self.points = rules.evalScore()
        self.hu = self.points is not None
        if self.hu:
            self.logger.log_winner(self.Id)
        else:
            self.points = - upperScoreLimit if upperScoreLimit is not None else - math.inf
        
        # clean up
        del rules

        return self.points