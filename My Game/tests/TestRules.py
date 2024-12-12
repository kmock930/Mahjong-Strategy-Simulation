import unittest;
import sys;
sys.path.append('My Game');
from Rules import Rules;
from Card import Card;
from utils import is_valid_pair, is_valid_meld, break_into_melds_and_pair;

class TestRules(unittest.TestCase):
    def setUp(self):
        """
        Set up reusable Rules object and example tiles for testing.
        """
        self.rules = Rules(
            incomingTile=None,
            closedDeck=[],
            openDeck=[],
            incomingPlayerId=0,
            currentPlayerId=0
        );

    def test_isThirteenOrphans(self):
        """
        Test for Thirteen Orphans hand.
        """
        thirteen_orphans = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='索', rank=1), Card(suit='索', rank=9),
            Card(suit='風', rank='東'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='北'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='發'), Card(suit='箭', rank='白'),
            Card(suit='萬', rank=1)  # Duplicate tile
        ]
        self.assertTrue(self.rules.isThirteenOrphans(thirteen_orphans))

    def test_isNotThirteenOrphans(self):
        """
        Test for Thirteen Orphans hand.
        """
        not_thirteen_orphans = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='索', rank=1), Card(suit='索', rank=9),
            Card(suit='風', rank='東'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='北'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='發'), Card(suit='箭', rank='白'),
            Card(suit='萬', rank=2)  # Duplicate tile
        ]
        self.assertFalse(self.rules.isThirteenOrphans(not_thirteen_orphans))

    def test_isPureTerminal(self):
        pureTerminal = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='索', rank=1), Card(suit='索', rank=1),
        ]
        self.assertTrue(self.rules.isPureTerminals(pureTerminal))

    def test_isNotPureTerminal(self):
        not_pureTerminal = [
            Card(suit='萬', rank=2), Card(suit='萬', rank=9),
            Card(suit='萬', rank=2), Card(suit='萬', rank=9),
            Card(suit='萬', rank=2), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='索', rank=1), Card(suit='索', rank=1),
        ]
        self.assertFalse(self.rules.isPureTerminals(not_pureTerminal))

    def test_isMixedTerminal(self):
        mixedTerminal = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='發'),
        ]
        self.assertTrue(self.rules.isMixedTerminals(mixedTerminal))

    def test_isNotMixedTerminal(self):
        mixedTerminal = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=9),
            Card(suit='筒', rank=2), Card(suit='筒', rank=9),
            Card(suit='筒', rank=3), Card(suit='筒', rank=9),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='發'),
        ]
        self.assertFalse(self.rules.isMixedTerminals(mixedTerminal))

    def test_ishonors(self):
        honors = [
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'), 
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中')
        ]
        self.assertTrue(self.rules.isAllHonors(honors))

    def test_isNothonors(self):
        honors = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3), 
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中')
        ]
        self.assertFalse(self.rules.isAllHonors(honors))

    def test_isBigDragon(self):
        bigDragon = [
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), 
            Card(suit='箭', rank='發'), Card(suit='箭', rank='發'), Card(suit='箭', rank='發'),
            Card(suit='箭', rank='白'), Card(suit='箭', rank='白'), Card(suit='箭', rank='白'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='索', rank=1), Card(suit='索', rank=1)
        ]
        self.assertTrue(self.rules.isBigThreeDragons(bigDragon))

    def test_isNotBigDragon(self):
        bigDragon = [
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), 
            Card(suit='箭', rank='發'), Card(suit='箭', rank='發'), Card(suit='箭', rank='發'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='索', rank=1), Card(suit='索', rank=1)
        ]
        self.assertFalse(self.rules.isBigThreeDragons(bigDragon))

    def test_isSmallDragon(self):
        smallDragon = [
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), 
            Card(suit='箭', rank='發'), Card(suit='箭', rank='發'), Card(suit='箭', rank='發'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='索', rank=1), Card(suit='索', rank=1), Card(suit='索', rank=1),
            Card(suit='箭', rank='白'), Card(suit='箭', rank='白')
        ]
        self.assertTrue(self.rules.isSmallThreeDragons(smallDragon))

    def test_isNotSmallDragon(self):
        smallDragon = [
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), 
            Card(suit='箭', rank='發'), Card(suit='箭', rank='發'), Card(suit='箭', rank='發'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='索', rank=1), Card(suit='索', rank=1), Card(suit='索', rank=1),
            Card(suit='萬', rank=1), Card(suit='萬', rank=1)
        ]
        self.assertFalse(self.rules.isSmallThreeDragons(smallDragon))

    def test_isBigWind(self):
        bigWinds = [
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中')
        ]
        self.assertTrue(self.rules.isBigFourWinds(bigWinds))

    def test_isNotBigWind(self):
        bigWinds = [
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'), Card(suit='箭', rank='中'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北'), Card(suit='風', rank='北'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南')
        ]
        self.assertFalse(self.rules.isBigFourWinds(bigWinds))

    def test_isSmallWind(self):
        smallWinds = [
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'),Card(suit='箭', rank='中'),
            Card(suit='風', rank='北'), Card(suit='風', rank='北')
        ]
        self.assertTrue(self.rules.isSmallFourWinds(smallWinds))

    def test_isNotSmallWind(self):
        smallWinds = [
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),
            Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'), Card(suit='風', rank='南'),
            Card(suit='風', rank='西'), Card(suit='風', rank='西'), Card(suit='風', rank='西'),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中'),Card(suit='箭', rank='中'),
            Card(suit='索', rank=5), Card(suit='索', rank=5)
        ]
        self.assertFalse(self.rules.isSmallFourWinds(smallWinds))

    def test_isMixedSuit(self):
        mixedSuit = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='萬', rank=4), Card(suit='萬', rank=5), Card(suit='萬', rank=6),
            Card(suit='萬', rank=7), Card(suit='萬', rank=8), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='箭', rank='中'), Card(suit='箭', rank='中')
        ]
        self.assertTrue(self.rules.isMixedSuit(mixedSuit))

    def test_isNotMixedSuit(self):
        mixedSuit = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='萬', rank=4), Card(suit='萬', rank=5), Card(suit='萬', rank=6),
            Card(suit='萬', rank=7), Card(suit='萬', rank=8), Card(suit='萬', rank=9),
            Card(suit='筒', rank=1), Card(suit='筒', rank=2), Card(suit='筒', rank=3),
            Card(suit='筒', rank=7), Card(suit='筒', rank=7)
        ]
        self.assertFalse(self.rules.isMixedSuit(mixedSuit))

    def test_isAllOneSuit(self):
        allInOneSuit = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='萬', rank=4), Card(suit='萬', rank=5), Card(suit='萬', rank=6),
            Card(suit='萬', rank=7), Card(suit='萬', rank=8), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='萬', rank=4), Card(suit='萬', rank=4)
        ]
        self.assertTrue(self.rules.isAllOneSuit(allInOneSuit))

    def test_isNotAllOneSuit(self):
        allInOneSuit = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='萬', rank=4), Card(suit='萬', rank=5), Card(suit='萬', rank=6),
            Card(suit='萬', rank=7), Card(suit='萬', rank=8), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3),
            Card(suit='筒', rank=4), Card(suit='筒', rank=4)
        ]
        self.assertFalse(self.rules.isAllOneSuit(allInOneSuit))

    def test_isNineGates(self):
        nineGates = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1),
            Card(suit='萬', rank=2), Card(suit='萬', rank=3), Card(suit='萬', rank=4),
            Card(suit='萬', rank=5), Card(suit='萬', rank=6), Card(suit='萬', rank=7),
            Card(suit='萬', rank=8), 
            Card(suit='萬', rank=9), Card(suit='萬', rank=9), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1)
        ]
        self.assertTrue(self.rules.isNineGates(nineGates))

    def test_isNotNineGates(self):
        nineGates = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1),
            Card(suit='萬', rank=2), Card(suit='萬', rank=3), Card(suit='萬', rank=4),
            Card(suit='萬', rank=5), Card(suit='萬', rank=6), Card(suit='萬', rank=7),
            Card(suit='索', rank=8), 
            Card(suit='萬', rank=9), Card(suit='萬', rank=9), Card(suit='萬', rank=9),
            Card(suit='萬', rank=1)
        ]
        self.assertFalse(self.rules.isNineGates(nineGates))
    '''
    def test_standardWinning(self):
        """
        Test for a standard winning hand.
        """
        standard_hand = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1),  # Pong
            Card(suit='筒', rank=2), Card(suit='筒', rank=3), Card(suit='筒', rank=4),  # Sequence
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),  # Pong
            Card(suit='筒', rank=9), Card(suit='筒', rank=9)  # Pair
        ]
        openDeck = [
            [Card(suit='索', rank=5), Card(suit='索', rank=5), Card(suit='索', rank=5)],  # Pong
        ]
        self.assertTrue(self.rules.isStandardHand(standard_hand, openDeck))

    def test_NotStandardWinning(self):
        """
        Test for a standard winning hand.
        """
        standard_hand = [
            Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1),  # Kong
            Card(suit='筒', rank=2), Card(suit='筒', rank=3), Card(suit='筒', rank=4),  # Sequence
            Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'),  # Pong
            Card(suit='索', rank=5), Card(suit='索', rank=5), Card(suit='索', rank=5),
            Card(suit='筒', rank=9), Card(suit='筒', rank=8)  # Pair
        ]
        self.assertFalse(self.rules.isStandardHand(standard_hand, []))
    '''
    def test_isValidMeld(self):
        """
        Test for a valid meld.
        """
        # Kong
        valid_meld = [Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1)]
        self.assertTrue(is_valid_meld(valid_meld))
        # Pong
        valid_meld = [Card(suit='萬', rank=1), Card(suit='萬', rank=1), Card(suit='萬', rank=1)]
        self.assertTrue(is_valid_meld(valid_meld))
        # Chow
        valid_meld = [Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=3)]
        self.assertTrue(is_valid_meld(valid_meld))

    def test_isNotValidMeld(self):
        """
        Test for an invalid meld.
        """
        # Kong
        invalid_meld = [Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='東'), Card(suit='風', rank='南')]
        self.assertFalse(is_valid_meld(invalid_meld))
        # Pong
        invalid_meld = [Card(suit='萬', rank=1), Card(suit='萬', rank=1)]
        self.assertFalse(is_valid_meld(invalid_meld))
        # Chow
        invalid_meld = [Card(suit='萬', rank=1), Card(suit='萬', rank=2), Card(suit='萬', rank=4)]
        self.assertFalse(is_valid_meld(invalid_meld))

    def test_isValidPair(self):
        """
        Test for a valid pair.
        """
        valid_pair = [Card(suit='萬', rank=1), Card(suit='萬', rank=1)]
        self.assertTrue(is_valid_pair(valid_pair))

    def test_isNotValidPair(self):
        """
        Test for an invalid pair.
        """
        invalid_pair = [Card(suit='萬', rank=1), Card(suit='萬', rank=2)]
        self.assertFalse(is_valid_pair(invalid_pair))

    def test_breakIntoMeldsAndPair(self):
        """
        Test for breaking tiles into melds and a pair.
        """
        tiles = [
            Card('萬', 1), Card('萬', 2), Card('萬', 3),  # Sequence
            Card('萬', 4), Card('萬', 5), Card('萬', 6),  # Sequence
            Card('萬', 7), Card('萬', 8), Card('萬', 9),  # Sequence
            Card('筒', 1), Card('筒', 1),                 # Pair
            Card('筒', 2), Card('筒', 3), Card('筒', 4)   # Sequence
        ]
        ret, melds = break_into_melds_and_pair(tiles)
        self.assertTrue(ret)
        self.assertEqual(len(melds), 5)
        self.assertEqual(melds[-1], [Card('筒', 1), Card('筒', 1)])  # Check the pair

        # Test case where melds should prioritize Pong
        tiles = [
            Card('萬', 1), Card('萬', 1), Card('萬', 1),  # Pong
            Card('萬', 2), Card('萬', 3), Card('萬', 4),  # Sequence
            Card('萬', 5), Card('萬', 6), Card('萬', 7),  # Sequence
            Card('萬', 9), Card('萬', 9),  # Pair
            Card('筒', 1), Card('筒', 1), Card('筒', 1)  # Pong
        ]
        ret, melds = break_into_melds_and_pair(tiles)
        self.assertTrue(ret)
        self.assertEqual(len(melds), 5)
        self.assertEqual(melds[-1], [Card('萬', 9), Card('萬', 9)])  # Check the pair

    def test_notBreakIntoMeldsAndPair(self):
        # Test case where melds cannot be formed
        tiles = [
            Card('萬', 1), Card('萬', 2), Card('萬', 3),  # Sequence
            Card('萬', 4), Card('萬', 5), Card('萬', 6),  # Sequence
            Card('萬', 7), Card('萬', 8), Card('萬', 9),  # Sequence
            Card('筒', 1), Card('筒', 2),  # Invalid pair
            Card('筒', 2), Card('筒', 3), Card('筒', 4)   # Sequence
        ]
        ret, melds = break_into_melds_and_pair(tiles)
        self.assertFalse(ret)

if __name__ == '__main__':
    unittest.main()