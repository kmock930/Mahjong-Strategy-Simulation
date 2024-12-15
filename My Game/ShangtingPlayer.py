from player import Player;
from Rules import Rules;
from Card import Card;
from gameLog import GameLog;
from utils import break_into_melds_and_pair, find_jokers;
from collections import Counter;

class ShangTingPlayer(Player):
    def __init__(self, Id: int, wind: str, hand: list='東', logger: GameLog = None):
        super().__init__(Id, wind, hand, logger)
        self.rules = Rules()
        self.shangting = False

    def discard(self, tile: Card):
        super().discard(tile)
        if self.rules.isShangTing(self.hand):
            self.shangting = True
        return tile

    def win(self):
        super().hu()
        self.shangting = False

    @staticmethod
    def evalShangTing(closedDeck: list[Card]) -> int|float|None:
        '''
        By considering the current set of hand tiles,
        evaluate the ShangTing distance. 
        Range of values: 1 to 8 (1: closest to winning; 8: farthest from winning)
        '''
        # Number of melds
        # closed deck
        ret, closedMelds = break_into_melds_and_pair(closedDeck)
        if (not ret):
            closedMelds = []
        else:
            closedMelds = closedMelds[:-1]  # remove the pair

        num_melds = len(closedMelds)

        # find number of jokers
        jokers = find_jokers(closedDeck)

        # find number of pairs on hand
        uniqueTiles = {}
        for tile in closedDeck:
            if ((tile.suit, tile.rank) in uniqueTiles):
                uniqueTiles[(tile.suit, tile.rank)] += 1
            else:
                uniqueTiles[(tile.suit, tile.rank)] = 1
        # counting pairs
        pairs = 0
        for tile in uniqueTiles:
            if (uniqueTiles[tile] == 2):
                pairs += 1

        # ShangTing distance
        N = [
            8 - 2 * num_melds - jokers,
            3 - jokers,
            4 - jokers
        ]

        # Determine which equation to use
        if (num_melds + jokers <= 5 ):
            return N[0]
        elif (num_melds + jokers > 5 and pairs > 0):
            return N[1]
        elif (num_melds + jokers > 5 and pairs == 0):
            return N[2]
        else:
            raise NotImplementedError("ShangTing distance calculation not implemented for this case")
