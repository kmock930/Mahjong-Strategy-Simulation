import unittest
import sys
sys.path.append('My Game')
from Card import Card
from utils import find_possible_melds
from ShangtingPlayer import ShangTingPlayer

class TestFindJoker(unittest.TestCase):
    '''
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
    '''
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

if __name__ == '__main__':
    unittest.main()