import unittest
import sys
sys.path.append('My Game')
from Rules import Rules
from Card import Card

class TestEvalScore(unittest.TestCase):
    def test_flower_tiles(self):
        # Case 1: Exactly 7 flower tiles
        rules = Rules(
            incomingTile=Card('花', '竹'), 
            closedDeck=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 8), Card('索', 9),
                Card('風', '東'), Card('風', '南'), Card('風', '西'),
                Card('箭', '中'), Card('箭', '發')
            ], 
            openDeck=[], 
            incomingPlayerId=0, currentPlayerId=0, 
            flowerDeck=[Card('花', i) for i in ['春', '夏', '秋', '冬', '梅', '蘭']]
        )
        totalTiles = rules.flowerDeck + [rules.incomingTile]
        self.assertEqual(len(totalTiles), 7)
        self.assertEqual(rules.evalScore(), 3)

        # Case 2: Exactly 8 flower tiles
        upperScoreLimit = 10
        openDeck = [
                [Card('索', 7), Card('索', 8), Card('索', 9)],
                [Card('萬', 1), Card('萬', 2), Card('萬', 3)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('花', '竹'),
            closedDeck=[
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('風', '東'), Card('風', '南'), Card('風', '西'),
                Card('箭', '中'), Card('箭', '發')
            ], 
            openDeck=openDeck, 
            incomingPlayerId=0, currentPlayerId=0, 
            flowerDeck=[Card('花', i) for i in ['春', '夏', '秋', '冬', '梅', '蘭', '菊']], 
            upperScoreLimit=upperScoreLimit
        )
        totalFlowers = rules.flowerDeck + [rules.incomingTile]
        self.assertEqual(len(totalFlowers), 8)
        self.assertEqual(rules.evalScore(), upperScoreLimit)
    
    def test_invalid_hand_length(self):
        # Case 3: Less than 14 tiles
        rules = Rules(
            incomingTile=Card('萬', 1),
            closedDeck=[Card('萬', i) for i in range(1,6)], 
            openDeck=[], 
            incomingPlayerId=0, currentPlayerId=0
        )
        self.assertIsNone(rules.evalScore())

        # Case 4: More than 18 tiles
        rules = Rules(
            incomingTile=Card(suit='風', rank='東'), 
            closedDeck=[Card('萬', i) for i in range(1,10)], 
            openDeck=[[Card('筒', i) for i in range(1,10)]], 
            incomingPlayerId=0, currentPlayerId=0
        )
        self.assertIsNone(rules.evalScore())

        del rules
    
    def test_thirdteenorphans(self):
        # Case 5: Thirteen Orphans
        thirteen_orphans = [Card('萬', 1), Card('萬', 9), Card('筒', 1), Card('筒', 9), Card('索', 1), Card('索', 9),
                            Card('風', '東'), Card('風', '南'), Card('風', '西'), Card('風', '北'),
                            Card('箭', '中'), Card('箭', '發'), Card('箭', '白')]
        rules = Rules(incomingTile=Card('萬', 1), closedDeck=thirteen_orphans, openDeck=[], flowerDeck=[Card('花', '夏')], incomingPlayerId=3, currentPlayerId=0)
        self.assertEqual(rules.evalScore(), 13)

    def test_winningwith0score(self):
        # Case 8: Winning with 0 score
        zero_score = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), 
            Card('索', 3), Card('索', 4), Card('索', 5), 
            Card('筒', 9), Card('筒', 9), Card('筒', 9),
            Card('萬', 2)
        ]
        openDeck=[
                [Card('萬', 6), Card('萬', 7), Card('萬', 8)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True;
        rules = Rules(
            incomingTile=Card('萬', 2), 
            closedDeck=zero_score, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=1, currentPlayerId=0
        )
        self.assertEqual(rules.evalScore(),0)

    def test_mixedterminals(self):
        # Case 6: Mixed Terminals
        mixed_terminals = [
            Card('萬', 1), Card('萬', 1),  
            Card('索', 1), Card('索', 1), Card('索', 1),
            Card('風', '東'), Card('風', '東'), Card('風', '東'), Card('風', '東'), 
            Card('箭', '中'), Card('箭', '中')
        ]
        openDeck = [
            [Card('筒', 9), Card('筒', 9), Card('筒', 9)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('萬', 1), 
            closedDeck=mixed_terminals, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=2
        )
        self.assertEqual(rules.evalScore(), 6+3) # also a all pongs

    def test_pureterminals(self):
        # Case 9: Pure Terminals
        pure_terminals = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), 
            Card('筒', 9), Card('筒', 9), Card('筒', 9), 
            Card('索', 1), Card('索', 1), Card('索', 1),
            Card('萬', 9)
        ]
        openDeck = [
                [Card('索', 9), Card('索', 9), Card('索', 9), Card('索', 9)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('萬', 9), 
            closedDeck=pure_terminals, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=2, currentPlayerId=3,
            gameID=0
        )
        self.assertEqual(rules.evalScore(), 10+3) # also a all pongs

    def test_allinonesuit(self):
        # Case 10: All in One Suit
        all_in_one_suit = [
            Card('萬', 1), Card('萬', 2), Card('萬', 3), 
            Card('萬', 4), Card('萬', 5), Card('萬', 6), 
            Card('萬', 7), Card('萬', 9), # missing tile in chow
            Card('萬', 9),  Card('萬', 9)
        ]
        openDeck = [
            [Card('萬', 1), Card('萬', 2), Card('萬', 3)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('萬', 8), 
            closedDeck=all_in_one_suit, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=2)
        self.assertEqual(rules.evalScore(), 7+1) # it is also a sequence

    def test_allhonors(self):
        # Case 11: All Honors
        all_honors = [
            Card('風', '西'), Card('風', '西'), Card('風', '西'),
            Card('箭', '中'), Card('箭', '中'), Card('箭', '中'),
            Card('箭', '白')
        ]
        rules = Rules(
            incomingTile=Card('箭', '白'), 
            closedDeck=all_honors, 
            openDeck=[
                [Card('風', '東'), Card('風', '東'), Card('風', '東'), Card('風', '東')],
                [Card('風', '南'), Card('風', '南'), Card('風', '南')],
            ], 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=3
        )
        self.assertEqual(rules.evalScore(), 8+3+1+2) # also a all pongs + 門前清 + winds x2

    def test_mixedsuit(self):
        # Case 12: Mixed Suit
        mixed_suit = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), 
            Card('萬', 1), Card('萬', 2), Card('萬', 3), 
            Card('萬', 5), Card('萬', 5), Card('萬', 5),
            Card('萬', 6), Card('萬', 7), Card('萬', 8),
            Card('風', '東')
        ]
        rules = Rules(
            incomingTile=Card('風', '東'), 
            closedDeck=mixed_suit, 
            openDeck=[], 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=2
        )
        self.assertEqual(rules.evalScore(), 3+1) # also 門前清

    def test_allpongs(self):
        # Case 13: All Pongs
        all_pongs = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), 
            Card('筒', 2), Card('筒', 2), Card('筒', 2), 
            Card('索', 3), Card('索', 3),
            Card('筒', 5), Card('筒', 5)
        ]
        openDeck = [
            [Card('萬', 4), Card('萬', 4), Card('萬', 4)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('索', 3), 
            closedDeck=all_pongs, 
            openDeck=openDeck, 
            incomingPlayerId=0, currentPlayerId=1
        )
        self.assertEqual(rules.evalScore(), 3+1) # no flowers

    def test_bigdragon(self):
        # Case 14: Big Dragon
        big_dragon = [
            Card('箭', '中'), Card('箭', '中'), Card('箭', '中'), 
            Card('箭', '發'), Card('箭', '發'), Card('箭', '發'),
            Card('萬', 1), Card('萬', 2), Card('萬', 3),
            Card('索', 1)
        ]
        openDeck = [
            [Card('箭', '白'), Card('箭', '白'), Card('箭', '白'), Card('箭', '白')]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True;
        rules = Rules(
            incomingTile=Card('索', 1), 
            closedDeck=big_dragon, 
            openDeck=openDeck, 
            incomingPlayerId=0, currentPlayerId=1
        )
        self.assertEqual(rules.evalScore(), 8+1) # no flowers

    def test_smalldragon(self):
        # Case 15: Small Dragon
        small_dragon = [
            Card('箭', '中'), Card('箭', '中'), Card('箭', '中'), 
            Card('箭', '發'), Card('箭', '發'), Card('箭', '發'), 
            Card('萬', 1), Card('萬', 3), # missing tile in chow
            Card('箭', '白'), Card('箭', '白')
        ]
        openDeck = [
                [Card('索', 1), Card('索', 1), Card('索', 1)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True;
        rules = Rules(
            incomingTile=Card('萬', 2), 
            closedDeck=small_dragon, 
            openDeck=openDeck, 
            incomingPlayerId=0, currentPlayerId=1
        )
        self.assertEqual(rules.evalScore(), 5+1) # no flowers

    def test_bigwinds(self):
        # Case 16: Big Winds
        big_winds = [
            Card('風', '東'), Card('風', '東'), Card('風', '東'), 
            Card('風', '南'), Card('風', '南'), Card('風', '南'), 
            Card('風', '西'), Card('風', '西'), Card('風', '西'), 
            Card('筒', 8)
        ]
        openDeck = [
            [Card('風', '北'), Card('風', '北'), Card('風', '北'), Card('風', '北')]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True;
        rules = Rules(
            incomingTile=Card('筒', 8), 
            closedDeck=big_winds, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=1, currentPlayerId=0,
            gameID=1
        )
        self.assertEqual(rules.evalScore(), 13+3+3) # also a mixed suit and all pongs

    def test_smallwinds(self):
        # Case 19: Small Winds
        small_winds = [
            Card('風', '東'), Card('風', '東'), Card('風', '東'), 
            Card('風', '南'), Card('風', '南'), Card('風', '南'), 
            Card('風', '西'), Card('風', '西'), Card('風', '西'), 
            Card('風', '北')
        ]
        openDeck=[
                [Card('筒', 8), Card('筒', 8), Card('筒', 8)]
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True;
        rules = Rules(
            incomingTile=Card('風', '北'), 
            closedDeck=small_winds, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=3
        )
        self.assertEqual(rules.evalScore(), 6+3+3) # also a mixed suit and all pongs

    def test_all_sequences(self):
        # Case 7: All sequences
        all_sequence = [
            Card('萬', 1), Card('萬', 2),  # Chow (missing one)
            Card('筒', 2), Card('筒', 3), Card('筒', 4),  # Chow
            Card('索', 4), Card('索', 5), Card('索', 6),  # Chow
            Card('筒', 5), Card('筒', 5)  # Pair
        ]
        openDeck = [
            [Card('萬', 7), Card('萬', 8), Card('萬', 9)]  # Chow
        ]
        for meld in openDeck:
            for tile in meld:
                tile.toDisplay = True
        rules = Rules(
            incomingTile=Card('萬', 3), 
            closedDeck=all_sequence, 
            openDeck=openDeck, 
            flowerDeck=[Card('花', '春')],
            incomingPlayerId=0, currentPlayerId=1)
        self.assertEqual(rules.evalScore(), 1)

    def test_ninegates(self):
        # Case 17: Nine Gates
        nine_gates = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), Card('萬', 2), Card('萬', 3), Card('萬', 4), Card('萬', 5),
            Card('萬', 6), Card('萬', 7), Card('萬', 8), Card('萬', 9), Card('萬', 9), Card('萬', 9), Card('萬', 5)
        ]
        rules = Rules(
            incomingTile=Card('萬', 2), 
            closedDeck=nine_gates, 
            openDeck=[], 
            flowerDeck=[Card('花', '夏')],
            incomingPlayerId=0, currentPlayerId=2)
        self.assertEqual(rules.evalScore(), 10)

    def test_eighteen_arhats(self):
        # Case 18: Eighteen Arhats
        eighteen_arhats = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1), Card('萬', 1), 
            Card('萬', 2), Card('萬', 2), Card('萬', 2), Card('萬', 2), 
            Card('萬', 3), Card('萬', 3), Card('萬', 3), Card('萬', 3), 
            Card('萬', 4), Card('萬', 4), Card('萬', 4), Card('萬', 4),
            Card('萬', 5)
        ]
        rules = Rules(incomingTile=Card('萬', 5), 
            closedDeck=eighteen_arhats[0:4] + [eighteen_arhats[-1]], 
            openDeck=[
                eighteen_arhats[4:8], 
                eighteen_arhats[8:12],
                eighteen_arhats[12:16]
            ], 
            incomingPlayerId=2, currentPlayerId=0
        )
        self.assertEqual(rules.evalScore(), 13+1+1) # no flowers + 門前清

    def test_upperscorelimit(self):
        # Case 20: Upper Score Limit
        upperScoreLimit = 11
        thirteen_orphans = [Card('萬', 1), Card('萬', 9), Card('筒', 1), Card('筒', 9), Card('索', 1), Card('索', 9),
                            Card('風', '東'), Card('風', '南'), Card('風', '西'), Card('風', '北'),
                            Card('箭', '中'), Card('箭', '發'), Card('箭', '白')]
        rules = Rules(
            incomingTile=Card('萬', 1), 
            closedDeck=thirteen_orphans, 
            openDeck=[], 
            incomingPlayerId=0, currentPlayerId=0, 
            upperScoreLimit=upperScoreLimit
        )
        self.assertEqual(rules.evalScore(), upperScoreLimit)

    

if __name__ == '__main__':
    unittest.main()
