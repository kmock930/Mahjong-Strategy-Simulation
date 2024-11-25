from Card import Card
from gameLog import GameLog

class Player:
    '''
    A Player in a Mahjong Game
    '''
    Id: int = 0
    wind: str = '東'
    hand: list[Card] = []
    openHand: list[Card] = []

    points: int = 0
    meld: list[Card] = []
    
    flowers: list[Card] = []
    hu: bool = False

    def __init__(self, Id: int, wind: str, hand: list='東', logger: GameLog = None):
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
        # remove the hand to the open tile as a meld
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.meld.append([tile, tile, tile])
        self.openHand.append(self.meld)
        self.logger.log_move(self.Id, f"pong {tile.suit}-{tile.rank}")
        return tile

    def chow(self, tile: Card):
        # obtain the tile from the discarded tile
        self.draw(tile)
        # remove the hand to the open tile as a meld
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.meld.append([tile, tile, tile])
        self.openHand.append(self.meld)
        self.logger.log_move(self.Id, f"chow {tile.suit}-{tile.rank}")
        return tile

    def kong(self, tile: Card):
        # obtain the tile from the discarded tile
        self.draw(tile)
        # remove the hand to the open tile as a meld
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.hand.remove(tile)
        self.meld.append([tile, tile, tile, tile])
        self.openHand.append(self.meld)
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
        else:
            target_oppID = 4 if self.Id == 1 else self.Id - 1
            if (oppID != target_oppID):
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
        hypotheticalHand = self.hand + [tile]
        if self.canChow(hypotheticalHand, tile, oppID):
            self.chow(tile)
            return 'chow'
        elif self.canGong(hypotheticalHand, tile):
            self.kong(tile)
            return 'kong'
        elif self.canPong(hypotheticalHand, tile):
            self.pong(tile)
            return 'pong'
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

    def hu(self):
        self.hu = True
        self.logger.log_winner(self.Id)
        # return self.points