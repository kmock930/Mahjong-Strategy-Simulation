from player import Player;
from Card import Card;
from collections import Counter
import math;

def is_valid_meld(meld: list[Card]) -> bool:
    """Check if a meld is valid (either a triplet or a sequence)."""
    # negative case checking
    if len(meld) not in (3,4):
        return False;
    if not all(tile.suit == meld[0].suit for tile in meld):
        return False;

    # positive case checking
    if (len(meld) == 4 and meld[0].rank == meld[1].rank == meld[2].rank == meld[3].rank):  # Kong
        return True;
    if (len(meld) == 3 and meld[0].rank == meld[1].rank == meld[2].rank):  # Triplet
        return True;

    if (any(tile.suit not in ('萬', '筒', '索') for tile in meld)):
        return False;
    # sort a meld by rank
    meld.sort(key=lambda tile: tile.rank);
    # Determine if it is a meld in sequence
    if (len(meld) == 3 and meld[0].rank + 1 == meld[1].rank and meld[1].rank + 1 == meld[2].rank):  # Sequence
        return True;
    return False;

def is_valid_pair(pair: list[Card]) -> bool:
    """Check if a pair is valid."""
    return len(pair) == 2 and pair[0].suit == pair[1].suit and pair[0].rank == pair[1].rank;

def break_into_melds_and_pair(tiles: list[Card]) -> tuple[bool, list[list[Card]]]:
    """Break down tiles into 4 melds and a pair if possible."""
    # Try each possible pair
    for i in range(len(tiles) - 1):
        for j in range(i + 1, len(tiles)):
            if tiles[i].suit == tiles[j].suit and tiles[i].rank == tiles[j].rank:
                # Found a pair
                pair = [tiles[i], tiles[j]];

                # removing the pair from meld's consideration
                remaining_tiles = tiles.copy();
                if (is_valid_pair(pair)):
                    remaining_tiles.remove(tiles[i]);
                    remaining_tiles.remove(tiles[j]);
                else:
                    return False;
                
                # check if the remaining tiles consists of melds
                melds: list[list[Card]] = [];
                counterTiles = Counter([(tile.suit, tile.rank) for tile in remaining_tiles]);
                
                # Check for melds of 4 tiles (Kong) or 3 tiles (pong)
                for (suit, rank), count in counterTiles.items():
                    if count >= 3:
                        meld = [Card(suit, rank)] * count;
                        if (is_valid_meld(meld)):
                            remaining_tiles = [tile for tile in remaining_tiles if not (tile.suit == suit and tile.rank == rank)];
                            melds.append(meld);
                
                # Check for melds of 3 tiles in sequence (Chow)
                for chosenTile in tiles:
                    if (chosenTile.suit not in ('萬', '筒', '索')):
                        break;
                    possibleChows = [
                        [
                            (chosenTile.suit, chosenTile.rank),
                            (chosenTile.suit, chosenTile.rank - 1),
                            (chosenTile.suit, chosenTile.rank - 2)
                        ],
                        [
                            (chosenTile.suit, chosenTile.rank),
                            (chosenTile.suit, chosenTile.rank + 1),
                            (chosenTile.suit, chosenTile.rank + 2)
                        ],
                        [
                            (chosenTile.suit, chosenTile.rank),
                            (chosenTile.suit, chosenTile.rank - 1),
                            (chosenTile.suit, chosenTile.rank + 1)
                        ]
                    ];
                    for meld in possibleChows:
                        uniqueSuits = set(meld[i][0] for i in range(len(meld)));
                        uniqueRanks = set(meld[i][1] for i in range(len(meld)));
                        isChow: bool = True;
                        meldTiles: list[Card] = [];
                        for tile in remaining_tiles:
                            isChow = isChow and (tile.suit in uniqueSuits and tile.rank in uniqueRanks);
                            if (isChow == True):
                                meldTiles.append(tile);
                        isChow = isChow and len(meldTiles) == 3 and is_valid_meld(meldTiles);  
                        if (isChow):  
                            melds.append(meldTiles);
                            remaining_tiles = [
                                tile 
                                for tile in remaining_tiles.copy()
                                if tile not in meldTiles
                            ];
                            break;
                        else:
                            continue;

    return len(remaining_tiles) == 0, melds + [pair];
