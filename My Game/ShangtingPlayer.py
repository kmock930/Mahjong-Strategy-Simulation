from player import Player;
from Card import Card;
from Rules import Rules;
from gameLog import GameLog;
from utils import break_into_melds_and_pair, find_jokers, find_possible_melds;
import random

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

    def handleSpecialActions(self, tile, oppID):
        '''
        Handle Special Actions based on the ShangTing distance.
        Prioritizing: Chow > Pong > Kong (as a tie breaker)
        '''
        if tile is None:
            return None
        hypotheticalHand = self.hand.copy() + [tile]
        actions: list[tuple] = []
        best_action = None
        best_shangting = ShangTingPlayer.evalShangTing(hypotheticalHand)

        # evaluate chow
        possible_melds: list[list[Card]] = []
        if self.canChow(self.hand, tile, oppID):
            possible_melds = [
                [Card(tile.suit, tile.rank - 2), Card(tile.suit, tile.rank - 1), tile],
                [Card(tile.suit, tile.rank - 1), tile, Card(tile.suit, tile.rank + 1)],
                [tile, Card(tile.suit, tile.rank + 1), Card(tile.suit, tile.rank + 2)]
            ]
            # Filter valid melds
            possible_melds = [
                meld 
                for meld in possible_melds 
                if meld in find_possible_melds(hypotheticalHand)
            ]
            for meld in possible_melds:
                if all(tileInMeld in hypotheticalHand for tileInMeld in meld):
                    temp_hand = hypotheticalHand.copy()
                    for meld_tile in meld:
                        temp_hand.remove(meld_tile)
                    shangting_dist = ShangTingPlayer.evalShangTing(temp_hand)

                    if shangting_dist < best_shangting:
                        best_shangting = shangting_dist
                        best_action = ('chow', meld, best_shangting)
                            
            if (best_action is not None):
                actions.append(best_action)
            else:
                actions.append(('chow', random.choice(possible_melds), best_shangting))

        # evaluate kong
        if self.canGong(self.hand, tile):
            temp_hand = hypotheticalHand.copy()
            for _ in range(4):
                temp_hand.remove(tile)
            shangting_dist = ShangTingPlayer.evalShangTing(temp_hand)
            if shangting_dist < best_shangting:
                best_shangting = shangting_dist
                best_action = ('kong', tile, best_shangting)

            if (best_action is not None):
                actions.append(best_action)
            else:
                actions.append(('kong', tile, best_shangting))

        # evaluate pong
        if self.canPong(self.hand, tile):
            temp_hand = hypotheticalHand.copy()
            for _ in range(3):
                temp_hand.remove(tile)
            shangting_dist = ShangTingPlayer.evalShangTing(temp_hand)
            if shangting_dist < best_shangting:
                best_shangting = shangting_dist
                best_action = ('pong', tile, best_shangting)

            if (best_action is not None):
                actions.append(best_action)
            else:
                actions.append(('pong', [tile]*3, best_shangting))

        # execute the best action
        if actions is not None and len(actions) > 0:
            best_action = min(actions, key=lambda x: x[2]) # min ShangTing
            match (best_action[0]):
                case 'chow':
                    return self.chow(tile, best_action[1])
                case 'kong':
                    return self.kong(tile)
                case 'pong':
                    return self.pong(tile)
                case _: # default
                    return None
        return None


    def win(self, incomingTile: Card, closedDeck: list[Card], incomingPlayerId: int, gameID: int, upperScoreLimit: int, discardedTiles: list[Card]):
        rules = Rules(
            incomingTile=incomingTile,
            closedDeck=closedDeck,
            openDeck=self.openHand,
            incomingPlayerId=incomingPlayerId,
            flowerDeck=self.flowers,
            currentPlayerId=self.Id,
            gameID=gameID,
            upperScoreLimit=upperScoreLimit
        )
        huPoints = rules.evalScore()
        if (huPoints is not None and huPoints >= 0):
            if (
                ShangTingPlayer.evalShangTing(self.hand) == 1 or # listen
                huPoints > upperScoreLimit * 0.3 or # larger score
                len(discardedTiles) > 144 * 0.7 # late game
            ):
                del rules
                return super().declareHu(
                    incomingTile=incomingTile, 
                    closedDeck=closedDeck, 
                    incomingPlayerId=incomingPlayerId, 
                    gameID=gameID, 
                    upperScoreLimit=upperScoreLimit
                )
        # assume not declaring Hu
        specialAction: Card = self.handleSpecialActions(incomingTile, incomingPlayerId)
        if (specialAction is not None):
            return specialAction
        else:
            return self.discard()

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
