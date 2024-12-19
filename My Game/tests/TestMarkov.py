import unittest
import sys
sys.path.append('My Game')
from MarkovPlayer import MarkovPlayer
from Card import Card
from gameLog import GameLog

class TestMarkovPlayerIntegration(unittest.TestCase):
    def setUp(self):
        """
        Setup for MarkovPlayer integration tests.
        """
        self.player = MarkovPlayer(
            Id=1, wind='東', 
            hand=[Card('萬', 1), Card('萬', 2), Card('萬', 3)],
            logger=GameLog(gameID=0)
        )
        self.base_state = {
            "hand": [Card('萬', 1), Card('萬', 2), Card('萬', 3)],
            "open_melds": [],
            "discarded_tiles": [],
            "flowers": []
        }

    def test_discard(self):
        """
        Test the discard method with Markov-based decision-making.
        """
        self.base_state["ID"] = self.player.Id
        discarded_tile = self.player.discard()
        self.assertIsNotNone(discarded_tile)
        self.assertNotIn(discarded_tile, self.player.hand)
        self.assertEqual(len(self.player.hand), 2)  # Initial hand has 3 tiles, one is discarded

    def test_handle_special_actions_chow(self):
        """
        Test the handleSpecialActions method for a Chow action.
        """
        self.base_state["ID"] = 1
        tile = Card('萬', 4)
        self.player.hand.extend([Card('萬', 3), Card('萬', 5)])  # Add tiles to enable Chow
        result = self.player.handleSpecialActions(tile, oppID=0)
        self.assertEqual(result, tile)
        self.assertTrue(any(Card('萬', 4) in meld for meld in self.player.openHand))
        for meld in self.player.openHand:
            for tile in meld:
                self.assertTrue(tile.toDisplay)

    def test_handle_special_actions_pong(self):
        """
        Test the handleSpecialActions method for a Pong action.
        """
        self.base_state["ID"] = 1
        tile = Card('萬', 1)
        self.player.hand.extend([Card('萬', 1)])  # Add tiles to enable Pong
        result = self.player.handleSpecialActions(tile, oppID=2)
        self.assertEqual(result, tile)
        self.assertIn([Card('萬', 1), Card('萬', 1), Card('萬', 1)], self.player.openHand)

    def test_handle_special_actions_kong(self):
        """
        Test the handleSpecialActions method for a Kong action.
        """
        self.base_state["ID"] = 1
        tile = Card('萬', 1)
        self.player.hand.extend([Card('萬', 1), Card('萬', 1)])  # Add tiles to enable Kong
        result = self.player.handleSpecialActions(tile, oppID=2)
        self.assertEqual(result, tile)
        self.assertIn([Card('萬', 1), Card('萬', 1), Card('萬', 1), Card('萬', 1)], self.player.openHand)

    def test_simulate_action_hu(self):
        """
        Test the simulate_action method for Hu (winning) scenario.
        """
        state = self.base_state.copy()
        state["action_tile"] = Card.encode(Card('萬', 1))
        state["action_player"] = 0
        state['gameID'] = 0
        state['upperScoreLimit'] = 10
        state["ID"] = 0
        state["hand"] = [Card('萬', 1), Card('萬', 1), Card('萬', 1), Card('筒', 2), Card('筒', 2)]
        next_state, reward = self.player.simulate_action("hu", state)
        self.assertGreaterEqual(reward, 10)  # Base reward for Hu plus any winning score

if __name__ == "__main__":
    unittest.main()
