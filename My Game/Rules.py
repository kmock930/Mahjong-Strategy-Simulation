from Card import Card;
from collections import Counter
from utils import break_into_melds_and_pair
import math;

class Rules:
    '''
    Mahjong Rules
    '''
    score = 0;
    upperScoreLimit = math.inf;
    incomingTile: Card = None;
    closedDeck: list[Card] = [];
    openTile: list[list[Card]] = [];
    incomingPlayerId: int = 0;
    currentPlayerId: int = 0;
    gameID: int = 0;
    flowerDeck:list[Card] = [];
    isWinning = False;

    '''
    Initialize the rules set
    @param incomingTile: Card
    @param closedDeck: list[Card]
    @param openDeck: list[Card]
    @param incomingPlayerId: int
    @param currentPlayerId: int
    '''
    def __init__(self, incomingTile: Card, closedDeck: list[Card], openDeck: list[list[Card]], incomingPlayerId: int, currentPlayerId: int, flowerDeck: list[Card] = None, upperScoreLimit: float = math.inf, gameID: int = 0):
        self.flowerDeck = flowerDeck if flowerDeck != None else [];
        self.incomingTile = incomingTile;
        self.incomingPlayerId = incomingPlayerId;
        self.closedDeck = closedDeck;
        self.openTile = openDeck;
        self.incomingPlayerId = incomingPlayerId;
        self.currentPlayerId = currentPlayerId;
        self.upperScoreLimit = upperScoreLimit;
        self.gameID = gameID;

    def evalScore(self, isFirstRound: bool = False, isLastPlayer: bool = False) -> int|float|None:
        '''
        Evaluates the score of a winning hand, None means not winning.
        @return int|float|None
        '''
        if (isFirstRound == True):
            # 天胡
            if (len(self.closedDeck) == 14 and self.incomingTile == None):
                self.isWinning = True;
                self.score += math.inf;
                return min(self.upperScoreLimit, math.inf);
            # 地胡
            if (len(self.closedDeck) == 13 and self.incomingTile != None and self.isStandardHand(
                closedDeck=self.closedDeck + [self.incomingTile],
                openDeck=[]
            )):
                self.isWinning = True;
                self.score += math.inf;
                return min(self.upperScoreLimit, math.inf);

        # check for flower tiles
        if (self.incomingTile != None and self.incomingTile.suit == '花'):
            self.flowerDeck.append(self.incomingTile);
        if (len(self.flowerDeck) == 7):
            self.score += 3;
            self.isWinning = True;
        if (len(self.flowerDeck) == 8):
            self.score += self.upperScoreLimit;
            self.isWinning = True;

        # check for a special hand
        totalTiles: list[Card] = self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld];
        if (len(totalTiles) < 14 or len(totalTiles) > 18):
            if (len(self.flowerDeck)< 7):
                self.isWinning = False;
        else:
            # Special Case
            # 十三幺
            # only count hand tiles and the incoming tile
            if (self.isThirteenOrphans(self.closedDeck + [self.incomingTile])):
                self.score += 13;
                self.isWinning = True;
            else:
                # normal hand
                if (self.isStandardHand(self.closedDeck + [self.incomingTile], self.openTile)):
                    self.isWinning = True;
                    # winning with no points
                
                # Special Patterns
                # 么九
                if (self.isMixedTerminals(totalTiles)):
                    self.isWinning = True;
                    if (self.isPureTerminals(totalTiles)):
                        self.score += 10;
                    else:
                        if (not self.isAllHonors(totalTiles)):
                            self.score += 6;

                # 清一色
                if (self.isAllOneSuit(totalTiles) and not self.isAllHonors(totalTiles)):
                    self.isWinning = True;
                    if (self.isNineGates(self.closedDeck, self.openTile)):
                        # 九指連環
                        self.isWinning = True;
                        self.score += 10;
                    else:
                        if (self.isEighteenArhats(totalTiles) == True):
                            # 十八羅漢 - handle later
                            pass
                        else:
                            # 清一色 - 萬 筒 索
                            self.score += 7;
                
                if (self.isAllHonors(totalTiles)):
                    # 字一色
                    self.score += 8;

                # 混一色
                if (self.isMixedSuit(totalTiles)):
                    self.isWinning = True;
                    self.score += 3;

                # 對對胡
                if (self.isAllPongs(totalTiles)):
                    self.isWinning = True;
                    if (self.isFourConcealed(self.closedDeck, self.openTile)):
                        # 四暗刻
                        self.score += math.inf;
                    else: 
                        self.score += 3;

                # 平胡
                if (self.isAllSequence(totalTiles)):
                    self.isWinning = True;
                    self.score += 1;

                # 三元
                if (self.isBigThreeDragons(totalTiles)):
                    self.isWinning = True;
                    self.score += 8;
                elif (self.isSmallThreeDragons(totalTiles)):
                    self.isWinning = True;
                    self.score += 5;

                # 四喜
                if (self.isBigFourWinds(totalTiles)):
                    self.isWinning = True;
                    self.score += 13;
                elif (self.isSmallFourWinds(totalTiles)):
                    self.isWinning = True;
                    self.score += 6;
                
                # 十八羅漢
                if (self.isEighteenArhats(totalTiles)):
                    self.isWinning = True;
                    self.score += 13;
        
        # Rules for additional points
        # flower tiles
        if (self.flowerDeck == None or len(self.flowerDeck) == 0):
            if (self.isWinning == True):
                self.score += 1
        elif (len(self.flowerDeck) < 7): # not 花胡
            if (self.isWinning == True):
                if (self.fullFlowerSet() == 0):
                    self.score += self.countRightFlower();
                self.score += self.fullFlowerSet();
        
        # 門前清
        if (self.noOpenTiles() == True 
                and not self.isFourConcealed(self.closedDeck, self.openTile) 
                and not self.isThirteenOrphans(self.closedDeck + [self.incomingTile])
                and not self.isNineGates(self.closedDeck, self.openTile)
                and not len(self.flowerDeck) >= 7
                and (self.incomingTile is not None and not self.incomingTile.suit == '花')
                and self.isWinning == True
        ):
            self.score += 1;
        
        # Wind
        self.score += self.countRightWind();

        # 自摸
        if (self.incomingPlayerId == self.currentPlayerId and not isLastPlayer):
            if ((len(self.flowerDeck) < 7)):
                self.score += 1;
        
        # 海底撈月
        if (isLastPlayer and self.isWinning):
            self.score += 1;

        # score is capped at upperScoreLimit if provided
        # only the winner has a score
        return min(self.score, self.upperScoreLimit) if self.isWinning == True else None;

    def isStandardHand(self, closedDeck: list[Card], openDeck: list[list[Card]]) -> bool:
        '''
        Check if the tiles form a standard hand.
        '''
        ret: bool = False;
        
        tiles = closedDeck + [tile for meld in openDeck for tile in meld]

        if (len(tiles) < 14 and ((len(closedDeck)-2) % 3 != 0)):
            print("Not enough tiles to win.");
            return ret;
    
        ret, melds = break_into_melds_and_pair(closedDeck);

        # not counting the last group (which is a pair)
        pair = melds[-1] if ret == True else [];
        melds = melds[:-1] + openDeck if ret == True else [];

        # Evaluate if hand matches the 5-block hypothesis
        return ret and len(melds) == 4 and len(pair) == 2;
        
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
        return all(tile.rank in [1, 9] for tile in tiles) and len(tiles) >= 14;

    # 混么九
    def isMixedTerminals(self, tiles: list[Card]) -> bool:
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

    # 九指連環
    def isNineGates(self, closedDeck: list[Card], openDeck: list[list[Card]]) -> bool:
        '''
        Check if the tiles form a nine gates hand.
        '''
        if (len(closedDeck) < 14 or len(openDeck) > 0):
            return False;
    
        counterSuits = Counter(tile.suit for tile in closedDeck if tile.suit in ('萬', '筒', '索'));
        if (len(counterSuits) != 1):
            return False;

        counterRank = Counter(tile.rank for tile in closedDeck if tile.suit in ('萬', '筒', '索'));
        if all(rank in counterRank for rank in range(1, 10)):
            return ((counterRank[1] == 4 and counterRank[9] == 3 and all(counterRank[rank] == 1 for rank in range(2, 9))) or # pair at 9
                    (counterRank[9] == 4 and counterRank[1] == 3 and all(counterRank[rank] == 1 for rank in range(2, 9))) or # pair at 1
                    (counterRank[1] == 3 and counterRank[9] == 3 and any(counterRank[rank] == 2 for rank in range(2, 9))) # pair at 2 to 8
                   );
        return False;

    # 對對胡
    def isAllPongs(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form an all-pongs hand.
        '''
        counterTiles = Counter(tiles)
        pairs = sum(1 for count in counterTiles.values() if count == 2);
        pongs = sum(1 for count in counterTiles.values() if count == 3);
        kongs = sum(1 for count in counterTiles.values() if count == 4);
        return pairs == 1 and pongs + kongs == 4 and kongs < 4;
    
    # 十八羅漢
    def isEighteenArhats(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form an eighteen arhats hand.
        '''
        return len(tiles) == 18 
    
    # 四暗刻
    def isFourConcealed(self, closedDeck: list[Card], openDeck: list[list[Card]]) -> bool:
        '''
        Check if the tiles form a four concealed pongs hand.
        '''
        counterClosedTiles = Counter(closedDeck)
        pairs = sum(1 for count in counterClosedTiles.values() if count == 2);
        pongs = sum(1 for count in counterClosedTiles.values() if count == 3);
        # count secret kongs
        counterOpenTiles = Counter(tile for meld in openDeck for tile in meld if tile.toDisplay == False);
        kongs = sum(1 for count in counterOpenTiles.values() if count == 4);
        return pongs + kongs == 4 and pairs == 1;

    # 平胡
    def isAllSequence(self, tiles: list[Card]) -> bool:
        '''
        Check if the tiles form an all-sequence hand.
        '''
        ret, melds = break_into_melds_and_pair(tiles)
        if (not ret):
            return False;

        pair = melds[-1] if ret else []
        if (len(pair) != 2 or pair[0].suit != pair[1].suit or pair[0].rank != pair[1].rank):
            return False;
        melds = melds[:-1] if ret else [];

        # check if all melds are in sequence
        for meld in melds[:-1]:
            # Error checking
            if (len(meld) != 3 or any(tile.suit not in ('萬', '筒', '索') for tile in meld)):
                return False;
            counterSuits = Counter(tile.suit for tile in meld);
            if (len(counterSuits) != 1):
                return False;
            # Sort
            meld.sort(key=lambda tile: tile.rank);
            if (meld[0].rank + 1 != meld[1].rank and meld[1].rank + 1 != meld[2].rank):
                return False;        
        
        # all sequences + 1 pair
        return ret and len(tiles) == 14 and len(pair) == 2 and len(melds) == 4;

    ####################################################################
    # Rules for additional points
    ####################################################################
    # Right Flower
    def countRightFlower(self) -> int:
        '''
        Check if the tiles form a right flower hand.
        '''
        counterFlowers = 0
        flower1 = ['春', '夏', '秋', '冬'];
        flower2 = ['梅', '蘭', '竹', '菊'];
        if (self.flowerDeck != None and len(self.flowerDeck) > 0):
            for flower in self.flowerDeck:
                if (flower.suit == '花' and flower1[self.currentPlayerId] == flower.rank):
                    counterFlowers += 1;
                if (flower.suit == '花' and flower2[self.currentPlayerId] == flower.rank):
                    counterFlowers += 1;
        return counterFlowers;

    def fullFlowerSet(self) -> int:
        '''
        Check if the tiles form a full flower set.
        Returns the number of full sets.
        '''
        flower1 = ['春', '夏', '秋', '冬'];
        flower2 = ['梅', '蘭', '竹', '菊'];
        counterFullSets = 0;
        if (self.flowerDeck != None and len(self.flowerDeck) > 0):
            flower1_count = sum(1 for flower in self.flowerDeck if flower.rank in flower1)
            flower2_count = sum(1 for flower in self.flowerDeck if flower.rank in flower2)
            counterFullSets = flower1_count // 4 + flower2_count // 4
        return counterFullSets;

    def noOpenTiles(self) -> bool:
        '''
        Check if the tiles form a no open tiles hand.
        '''
        return len(self.openTile) == 0 or (len(self.openTile) > 0 and all(tile.toDisplay == False for meld in self.openTile for tile in meld));

    def countRightWind(self) -> int:
        '''
        Count the melds of matching winds in a hand.
        '''
        total_tiles = self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld]
        if (self.isBigFourWinds(total_tiles)
            or self.isSmallFourWinds(total_tiles)
        ):
            # never count those points twice
            return 0;

        counterWinds: int = 0;

        ret, melds = break_into_melds_and_pair(self.closedDeck + [self.incomingTile]);
        if (not ret):
            return 0;
        melds = melds[:-1] if ret else [];

        winds = ['東', '南', '西', '北'];
        # closed tiles
        for meld in melds:
            if (len(meld) < 3):
                continue;
            # seat wind
            if (all(tile.suit == '風' for tile in meld)
                and len(set(tile.rank for tile in meld)) == 1 
                and all(tile.rank == winds[self.currentPlayerId] for tile in meld)
            ):
                counterWinds += 1;
            # prevailing wind
            if (all(tile.suit == '風' for tile in meld)
                and len(set(tile.rank for tile in meld)) == 1 
                and all(tile.rank == winds[self.gameID] for tile in meld)
            ):
                counterWinds += 1;
            # 中發白
            if (all(tile.suit == '箭' for tile in meld) 
                and len(set(tile.rank for tile in meld)) == 1
                and not self.isSmallThreeDragons(self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld])
                and not self.isBigThreeDragons(self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld])
            ):
                counterWinds += 1;
        
        # open tiles
        for meld in self.openTile:
            # seat wind
            if (all(tile.suit == '風' for tile in meld)
                and len(set(tile.rank for tile in meld)) == 1 
                and all(tile.rank == winds[self.currentPlayerId] for tile in meld)
            ):
                counterWinds += 1;
            # prevailing wind
            if (all(tile.suit == '風' for tile in meld)
                and len(set(tile.rank for tile in meld)) == 1
                and all(tile.rank == winds[self.gameID] for tile in meld)
            ):
                counterWinds += 1;
            # 中發白
            if (all(tile.suit == '箭' for tile in meld) 
                and len(set(tile.rank for tile in meld)) == 1
                and not self.isSmallThreeDragons(self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld])
                and not self.isBigThreeDragons(self.closedDeck + [self.incomingTile] + [tile for meld in self.openTile for tile in meld])
            ):
                counterWinds += 1;

        return counterWinds;