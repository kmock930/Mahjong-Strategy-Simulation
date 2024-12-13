class Card:
    '''
    A Mahjong Tile
    '''
    suit: str;
    rank: int | str;
    toDisplay: bool = False;

    def __init__(self, suit: str, rank: int | str):
        self.suit = suit;
        self.rank = rank;
        self.toDisplay = False;

    def __eq__(self, other):
        """Check if two cards are equal based on suit and rank."""
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __hash__(self):
        """Generate a unique hash for a card."""
        return hash((self.suit, self.rank))

    def __repr__(self):
        """Readable string representation for debugging."""
        return f"Card(suit='{self.suit}', rank={self.rank})"