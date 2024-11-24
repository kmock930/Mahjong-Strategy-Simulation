from Card import Card;

class Player:
    '''
    A Player in a Mahjong Game
    '''
    Id: int = 0;
    wind: str = '東';
    hand: list[Card] = [];
    openHand: list[Card] = [];

    points: int = 0;
    meld: list[Card] = [];
    
    flowers: list[Card] = [];
    hu: bool = False;

    def __init__(self, Id: int, wind: str, hand: list='東'):
        self.Id = Id;
        self.wind = wind;
        self.hand = hand;

    def discard(self, tilePosition: int):
        toRemove = self.hand[tilePosition];
        self.hand.pop(tilePosition);
        return toRemove;

    def draw(self, tile: Card):
        self.hand.append(tile);
        return tile;

    def pong(self, tile: Card):
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.meld.append([tile, tile, tile]);
        return tile;

    def chow(self, tile: Card):
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.meld.append([tile, tile, tile]);
        return tile;

    def kong(self, tile: Card):
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.hand.remove(tile);
        self.meld.append([tile, tile, tile, tile]);
        return tile;

    def showFlower(self, tilePosition: int):
        tile = self.hand[tilePosition]
        self.flowers.append(tile)
        self.hand.pop(tilePosition)
        return tile;

    def canChow(self, tile: Card) -> bool:
        if tile.suit in ['花', '風', '箭']:
            return False;
        else:
            return (self.hand.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0 and
                    self.hand.count(Card(suit=tile.suit, rank=tile.rank+2)) > 0) or \
                   (self.hand.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0 and
                    self.hand.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0) or \
                   (self.hand.count(Card(suit=tile.suit, rank=tile.rank-2)) > 0 and
                    self.hand.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0);

    def canPong(self, tile: Card) -> bool:
        return self.hand.count(tile) == 2;

    def canGong(self, tile: Card) -> bool:
        return self.hand.count(tile) == 3;

    # default strategy (To be overriden by another class)
    def discard(self):
        # by default it discards what is drawn (i.e., the new tile)
        newTile = self.hand[-1];
        tile = self.hand.pop(len(self.hand)-1);
        return tile;

    def hu(self):
        self.hu = True;
        # return self.points;