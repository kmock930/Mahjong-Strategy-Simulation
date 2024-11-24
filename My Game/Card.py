class Card:
    '''
    A Mahjong Tile
    '''
    suit: str;
    rank: int | str;

    def __init__(self, suit: str, rank: int | str):
        self.suit = suit;
        self.rank = rank;