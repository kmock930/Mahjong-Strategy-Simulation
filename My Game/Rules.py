from player import Player;
from Card import Card;

class Rules:
    '''
    Mahjong Rules
    '''
    # determine if a player can pong
    @staticmethod
    def canPong(player: Player, tile: Card) -> bool:
        return player.hand.count(tile) == 3;

    # determine if a player can chow
    @staticmethod
    def canChow(player: Player, tile: Card) -> bool:
        if tile.suit in ['花', '風', '箭']:
            return False;
        else:
            return (player.hand.count(tile) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank+2)) > 0) or \
                   (player.hand.count(tile) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank+1)) > 0) or \
                   (player.hand.count(tile) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank-2)) > 0 and
                    player.hand.count(Card(suit=tile.suit, rank=tile.rank-1)) > 0);

    # determine if a player can kong
    @staticmethod
    def canKong(player: Player, tile: Card) -> bool:
        return player.hand.count(tile) == 4;

    # determine if a player can hu
    @staticmethod
    def canHu(player: Player) -> bool:
        if len(player.hand) < 14:
            return False;

        return (
            # flowers
            player.flowers <= 7 or
            # 4 open melds and a pair
            (len(player.meld) == 4 and len(player.hand) == 2)
            # closed melds on hand and a pair
        );