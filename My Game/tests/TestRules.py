import unittest;
import sys;
sys.path.append('My Game');
from Rules import Rules;
from Card import Card;

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

if __name__ == '__main__':
    unittest.main()