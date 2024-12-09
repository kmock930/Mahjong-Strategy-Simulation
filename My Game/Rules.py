from player import Player;
from Card import Card;
from collections import Counter
import math;

class Rules:
    '''
    Mahjong Rules
    '''
    score = 0;
    incomingTile: Card = None;
    closedDeck: list[Card] = [];
    openTile: list[Card] = [];
    incomingPlayerId: int = 0;
    currentPlayerId: int = 0;
    flowerDeck:list[Card] = [];
    resDeck:list[Card] = [];
    isWinning = False;

    '''
    Initialize the rules set
    @param incomingTile: Card
    @param closedDeck: list[Card]
    @param openDeck: list[Card]
    @param incomingPlayerId: int
    @param currentPlayerId: int
    '''
    def __init__(self, incomingTile: Card, closedDeck: list[Card], openDeck: list[Card], incomingPlayerId: int, currentPlayerId: int, flowerDeck: list[Card] = None):
        self.flowerDeck = flowerDeck if flowerDeck != None else [];
        self.incomingTile = incomingTile;
        self.incomingPlayerId = incomingPlayerId;
        self.openTile = openDeck;
        self.incomingPlayerId = incomingPlayerId;
        self.currentPlayerId = currentPlayerId;
        self.resDeck = closedDeck + openDeck + [incomingTile];

    def evalScore(self) -> int|float|None:
        '''
        Evaluates the score of a winning hand, None means not winning.
        @return int|float|None
        '''
        # check for flower tiles
        if (len(self.flowerDeck) == 7):
            self.score += 3;
            self.isWinning = True;
        if (len(self.flowerDeck) == 8):
            self.score += math.inf;
            self.isWinning = True;

        # check for a special hand
        specialHand: list[Card] = self.closedDeck + [self.incomingTile];
        if (len(specialHand) != 14):
            self.isWinning = False;
        else:
            # 十三幺
            if (self.isThirteenOrphans(specialHand)):
                self.score += 13;
                self.isWinning = True;

            # special rules that add 1 point
            if (self.isWinning == True and self.incomingPlayerId == self.currentPlayerId):
                self.score += 1;
            if (len(self.openDeck)==0):
                self.score += 1;
    
        return self.score if self.isWinning == True else None;

    ####################################################################
    # Special Hand Rules
    ####################################################################

    # 十三幺 
    def isThirteenOrphans(self, tiles: list[Card]) -> bool:
        """
        Check if the tiles form a Thirteen Orphans hand.
        """
        required_suits = ['萬', '筒', '索', '風', '箭'];
        required_ranks = [1, 9, '東', '南', '西', '北', '中', '發', '白'];

        # Ensure there are exactly 14 tiles
        if (len(tiles) == 14 and 
            all(tile.suit in required_suits for tile in tiles) and 
            all(tile.rank in required_ranks for tile in tiles)
        ):
            return True
        return False

    # 清么九
    def isPureTerminals(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form a pure terminal hand.
        '''
        return all(tile.rank in [1, 9, '東', '南', '西', '北', '中', '發', '白'] for tile in tiles) and len(tiles) >= 14;

    # 字一色
    def isAllHonors(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form an all-honors hand.
        '''
        return all(tile.suit in ['風', '箭'] for tile in tiles) and len(tiles) >= 14;

    # 大三元
    def isBigThreeDragons(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form a big three dragons hand.
        '''
        dragons = ['中', '發', '白']
        counter = Counter(tile.rank for tile in tiles if tile.suit == '箭')
        pongs = sum(1 for dragon in dragons if counter[dragon] >= 3)
        return pongs == 3 and len(tiles) >= 14;

    # 小三元
    def isSmallThreeDragons(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form a small three dragons hand.
        '''
        dragons = ['中', '發', '白']
        counter = Counter(tile.rank for tile in tiles if tile.suit == '箭')
        pongs = sum(1 for dragon in dragons if counter[dragon] >= 3)
        pairs = sum(1 for dragon in dragons if counter[dragon] == 2)
        return pongs == 2 and pairs == 1 and len(tiles) >= 14;

    # 大四喜
    def isBigFourWinds(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form a big four winds hand.
        '''
        winds = ['東', '南', '西', '北']
        counter = Counter(tile.rank for tile in tiles if tile.suit == '風')
        pongs = sum(1 for wind in winds if counter[wind] >= 3)
        return pongs == 4 and len(tiles) >= 14;

    # 小四喜
    def isSmallFourWinds(self, tiles:list[Card]) -> bool:
        '''
        Check if the tiles form a small four winds hand.
        '''
        winds = ['東', '南', '西', '北']
        counter = Counter(tile.rank for tile in tiles if tile.suit == '風')
        pongs = sum(1 for wind in winds if counter[wind] >= 3)
        pairs = sum(1 for wind in winds if counter[wind] == 2)
        return pongs == 3 and pairs == 1 and len(tiles) >= 14;

    # 清一色
    def isAllOneSuit(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form an all-one-suit hand.
        '''
        return len(set(tile.suit for tile in tiles)) == 1 and len(tiles) >= 14;

    # 混一色
    def isMixedSuit(self, tiles: list[Card]) -> bool:
        suits = {tile.suit for tile in tiles if tile.suit not in ['風', '箭', '花']}
        has_honors = any(tile.suit in ['風', '箭'] for tile in tiles)
        return len(suits) == 1 and has_honors and len(tiles) >= 14;