import unittest
import sys
sys.path.append('My Game')
from Card import Card
from player import Player
from ShangtingPlayer import ShangTingPlayer
from utils import find_jokers
from gameLog import GameLog

class TestStrategies(unittest.TestCase):
    def test_find_joker_present(self):
        closedDeck = [
            Card('萬', 1), Card('萬', 1), Card('萬', 2), 
            Card('索', 3), Card('索', 5), 
            Card('筒', 9), Card('筒', 9),
            Card('萬', 2), Card('萬', 3),
            Card('風', '東'), Card('風', '南'), 
            Card('箭', '中'), Card('箭', '中'),
        ]
        self.assertEqual(find_jokers(closedDeck), 6)
    
    def test_find_joker_not_present(self):
        closedDeck = [
            Card('萬', 1), Card('萬', 9), 
            Card('筒', 1), Card('筒', 9), 
            Card('索', 1), Card('索', 9),
            Card('風', '東'), Card('風', '南'), Card('風', '西'), Card('風', '北'),
            Card('箭', '中'), Card('箭', '發'), Card('箭', '白')
        ]
        self.assertEqual(find_jokers(closedDeck), 0)
    
    def test_eval_ShangTing_Distance(self):
        closedDeck = [
            Card('萬', 1), Card('萬', 1), Card('萬', 2), 
            Card('索', 3), Card('索', 5), 
            Card('筒', 9), Card('筒', 9),
            Card('萬', 2)
        ]
        self.assertEqual(ShangTingPlayer.evalShangTing(
            closedDeck
        ), 8 - 2 * 0 - 4)

    def test_discard_minimizes_shangting(self):
        player = ShangTingPlayer(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 8), Card('索', 9),
                Card('風', '東'), Card('風', '南'), Card('風', '南'), Card('風', '南')
            ],
            logger=GameLog(gameID=0)
        )
        discarded_tile = player.discard()
        self.assertIsInstance(discarded_tile, Card)
        print(f"Discarded Tile: {discarded_tile.suit}-{discarded_tile.rank}")

    def test_handleSpecialActions(self):
        # chow
        player = Player(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 8), # missing chow
                Card('風', '南'), Card('風', '南'), Card('風', '南'),
                Card('箭', '中'), Card('風', '東')
            ],
            logger=GameLog(gameID=0)
        )
        tile = Card('索', 9)  # Tile that completes a Chow
        action = player.handleSpecialActions(tile, oppID=0)
        self.assertEqual(action, tile)
        self.assertIn([Card('索', 7), Card('索', 8), Card('索', 9)], player.openHand)
        for meld in player.openHand:
            for tile in meld:
                self.assertTrue(tile.toDisplay)
        
        # pong
        player = Player(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 7), # missing pong
                Card('風', '南'), Card('風', '南'), Card('風', '南'),
                Card('箭', '中'), Card('風', '東')
            ],
            logger=GameLog(gameID=0)
        )
        tile = Card('索', 7)  # Tile that completes a Pong
        action = player.handleSpecialActions(tile, oppID=3)
        self.assertEqual(action, tile)
        self.assertIn([Card('索', 7), Card('索', 7), Card('索', 7)], player.openHand)
        for meld in player.openHand:
            for tile in meld:
                self.assertTrue(tile.toDisplay)

        # kong
        player = Player(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 7), Card('索', 7), # missing kong
                Card('風', '南'), Card('風', '南'), Card('風', '南'),
                Card('箭', '中'), Card('風', '東')
            ],
            logger=GameLog(gameID=0)
        )
        tile = Card('索', 7)  # Tile that completes a Kong
        action = player.handleSpecialActions(tile, oppID=3)
        self.assertEqual(action, tile)
        self.assertIn([Card('索', 7), Card('索', 7), Card('索', 7), Card('索', 7)], player.openHand)
        for meld in player.openHand:
            for tile in meld:
                self.assertTrue(tile.toDisplay)

    def test_canchow(self):
        player = Player(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 8), 
                Card('風', '南'), Card('風', '南'), Card('風', '南'), 
                Card('箭', '中'), Card('箭', '中')
            ]
        )
        tile = Card('索', 9)
        self.assertTrue(player.canChow(
            deck=player.hand,
            tile=tile,
            oppID=0
        ))
        # negative case 1: tile is not chow-able
        tile = Card('萬', 8)
        self.assertFalse(player.canChow(
            deck=player.hand,
            tile=tile,
            oppID=0
        ))
        # negative case 2: player is not the previous player
        tile = Card('萬', 4)
        self.assertFalse(player.canChow(
            deck=player.hand,
            tile=tile,
            oppID=2
        ))
    
    def test_handleSpecialActions_ShangTingPlayer(self):
        # chow
        player = ShangTingPlayer(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 7), Card('索', 8)
            ],
            logger=GameLog(gameID=0)
        )
        expectedTile = Card('索', 9)  # Tile that completes a Chow
        actualTile = player.handleSpecialActions(expectedTile, oppID=0)
        self.assertEqual(actualTile, expectedTile)
        self.assertIn([Card('索', 7), Card('索', 8), Card('索', 9)], player.openHand)

        # pong
        player = ShangTingPlayer(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 8), Card('索', 8)
            ],
            logger=GameLog(gameID=0)
        )
        expectedTile = Card('索', 8)  # Tile that completes a Pong
        actualTile = player.handleSpecialActions(expectedTile, oppID=2)
        self.assertEqual(actualTile, expectedTile)
        self.assertIn([Card('索', 8), Card('索', 8), Card('索', 8)], player.openHand)

        # kong
        player = ShangTingPlayer(
            Id=1, 
            wind='東', 
            hand=[
                Card('萬', 1), Card('萬', 2), Card('萬', 3),
                Card('筒', 4), Card('筒', 5), Card('筒', 6),
                Card('索', 8), Card('索', 8), Card('索', 8)
            ],
            logger=GameLog(gameID=0)
        )
        expectedTile = Card('索', 8)  # Tile that completes a Kong
        actualTile = player.handleSpecialActions(expectedTile, oppID=2)
        self.assertEqual(actualTile, expectedTile)
        self.assertIn([Card('索', 8), Card('索', 8), Card('索', 8), Card('索', 8)], player.openHand)
        
if __name__ == '__main__':
    unittest.main()