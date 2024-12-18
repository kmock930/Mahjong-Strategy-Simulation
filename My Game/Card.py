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
    
    def encode(self):
        """Encode the card into a unique integer."""
        suit_map = {"萬": 0, "筒": 36, "索": 72, "風": 108, "箭": 136, "花": 144}
        if self.suit in ["萬", "筒", "索"]:
            return suit_map[self.suit] + (self.rank - 1)
        elif self.suit in ["風", "箭"]:
            encodedRank: int = 0
            match self.rank:
                case '東':
                    encodedRank = 1
                case '南':
                    encodedRank = 2
                case '西':
                    encodedRank = 3
                case '北':
                    encodedRank = 4
                case '中':
                    encodedRank = 5
                case '發':
                    encodedRank = 6
                case '白':
                    encodedRank = 7
                case _:
                    raise ValueError(f"Unknown rank: {self.rank}")
            return suit_map[self.suit] + (encodedRank - 1)
        elif self.suit == "花":
            encodedRank: int = 0
            match self.rank:
                case '春':
                    encodedRank = 1
                case '夏':
                    encodedRank = 2
                case '秋':
                    encodedRank = 3
                case '冬':
                    encodedRank = 4
                case '梅':
                    encodedRank = 5
                case '蘭':
                    encodedRank = 6
                case '菊':
                    encodedRank = 7
                case '竹':
                    encodedRank = 8
            return suit_map[self.suit] + (encodedRank - 1)
        else:
            raise ValueError(f"Unknown suit: {self.suit}")