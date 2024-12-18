import unittest
import sys;
sys.path.append('My Game');
from Card import Card

class TestCard(unittest.TestCase):

    def test_card_equality(self):
        card1 = Card(suit="萬", rank=5)
        card2 = Card(suit="萬", rank=5)
        card3 = Card(suit="筒", rank=5)
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)

    def test_card_hash(self):
        card1 = Card(suit="萬", rank=5)
        card2 = Card(suit="萬", rank=5)
        card3 = Card(suit="筒", rank=5)
        self.assertEqual(hash(card1), hash(card2))
        self.assertNotEqual(hash(card1), hash(card3))

    def test_card_repr(self):
        card = Card(suit="萬", rank=5)
        self.assertEqual(repr(card), "Card(suit='萬', rank=5)")

    def test_card_encode_number_suits(self):
        card1 = Card(suit="萬", rank=1)
        card2 = Card(suit="筒", rank=1)
        card3 = Card(suit="索", rank=1)
        self.assertEqual(card1.encode(), 0)
        self.assertEqual(card2.encode(), 36)
        self.assertEqual(card3.encode(), 72)

    def test_card_encode_wind_and_arrow_suits(self):
        card1 = Card(suit="風", rank='東')
        card2 = Card(suit="箭", rank='中')
        self.assertEqual(card1.encode(), 108)
        self.assertEqual(card2.encode(), 140)

    def test_card_encode_flower_suit(self):
        card1 = Card(suit="花", rank='春')
        card2 = Card(suit="花", rank='夏')
        self.assertEqual(card1.encode(), 144)
        self.assertEqual(card2.encode(), 145)

    def test_card_encode_invalid_suit(self):
        with self.assertRaises(ValueError):
            Card(suit="Invalid", rank=1).encode()

    def test_card_encode_invalid_rank(self):
        with self.assertRaises(ValueError):
            Card(suit="風", rank="Invalid").encode()

if __name__ == '__main__':
    unittest.main()