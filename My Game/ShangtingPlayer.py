from player import Player;
from Card import Card;
from gameLog import GameLog;
from utils import break_into_melds_and_pair, find_jokers;

class ShangTingPlayer(Player):
    def __init__(self, Id: int, wind: str, hand: list='東', logger: GameLog = None):
        super().__init__(Id, wind, hand, logger)

    def discard(self):
        originalLength = len(self.hand)
        originalHand = self.hand.copy()
        # strategy
        def minimizeShangTing(deck: list[Card]):
            targetTile: Card = deck[-1] # discard the new tile by default
            shangTingDist = ShangTingPlayer.evalShangTing(deck.copy()) # init
            for tile in deck:
                hypotheticalDeck = deck.copy()
                hypotheticalDeck.remove(tile)
                hypotheticalDist = ShangTingPlayer.evalShangTing(hypotheticalDeck)
                if (hypotheticalDist < shangTingDist):
                    shangTingDist = hypotheticalDist
                    targetTile = tile
            return targetTile, shangTingDist  
        tile_to_remove, targetShangTing = minimizeShangTing(self.hand)
        if (targetShangTing is None):
            raise ValueError("ShangTing distance calculation failed.")

        # logs
        self.logger.log_move(self.Id, f"discards a tile: {tile_to_remove.suit}-{tile_to_remove.rank}")
        self.logger.log(f"Original {originalLength} Tiles:")
        for tile in originalHand:
            self.logger.log(f"{tile.suit} {tile.rank}")

        self.logger.log(f"Remaining {len(self.hand)} Tiles")
        for tile in self.hand:
            self.logger.log(f"{tile.suit} {tile.rank}")
        
        return tile_to_remove

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
