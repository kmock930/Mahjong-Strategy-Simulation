import unittest
import sys;
sys.path.append('server/My Game');
from Card import Card

class TestCard(unittest.TestCase):
    # encode
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
    
    # decode
    def test_decode_wan(self):
        self.assertEqual(Card.decode(0), Card("萬", 1))
        self.assertEqual(Card.decode(8), Card("萬", 9))

    def test_decode_tong(self):
        self.assertEqual(Card.decode(36), Card("筒", 1))
        self.assertEqual(Card.decode(44), Card("筒", 9))

    def test_decode_suo(self):
        self.assertEqual(Card.decode(72), Card("索", 1))
        self.assertEqual(Card.decode(80), Card("索", 9))

    def test_decode_feng(self):
        self.assertEqual(Card.decode(108), Card("風", '東'))
        self.assertEqual(Card.decode(111), Card("風", '北'))

    def test_decode_jian(self):
        self.assertEqual(Card.decode(136), Card("箭", '中'))
        self.assertEqual(Card.decode(138), Card("箭", '白'))

    def test_decode_hua(self):
        self.assertEqual(Card.decode(144), Card("花", '春'))
        self.assertEqual(Card.decode(151), Card("花", '竹'))

    def test_decode_invalid(self):
        with self.assertRaises(ValueError):
            Card.decode(200)

if __name__ == '__main__':
    unittest.main()