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
'''
def break_into_melds_and_pair(tiles: list[Card]) -> tuple[bool, list[list[Card]]]:
    """Break down tiles into 4 melds and a pair if possible."""
    if len(tiles) < 14:
        return False, []

    # sorting ensures deterministic outcome
    tiles.sort(key=lambda tile: (tile.suit, tile.rank))

    # Try each possible pair
    for i in range(len(tiles) - 1):
        print("Another pair")
        if tiles[i].suit == tiles[i+1].suit and tiles[i].rank == tiles[i+1].rank:
            # Found a pair
            pair = [tiles[i], tiles[i+1]];
                
            # removing the pair from meld's consideration
            remaining_tiles = tiles[:i] + tiles[i+2:]

            if not is_valid_pair(pair):
                continue;
                
            # check if the remaining tiles consists of melds
            melds: list[list[Card]] = [];
            counterTiles = Counter([(tile.suit, tile.rank) for tile in remaining_tiles]);

            # Check for melds of 4 tiles (Kong) or 3 tiles (pong)
            for (suit, rank), count in counterTiles.items():
                if count >= 3:
                    print("Pong: ", suit, rank);
                    meld = [Card(suit, rank)] * 3; #disregard kong
                    melds.append(meld);
                    if (is_valid_meld(meld)):
                        for _ in range(3):
                            remaining_tiles.remove(Card(suit, rank))
                        
                
            # Check for melds of 3 tiles in sequence (Chow)
            for chosenTile in remaining_tiles.copy():
                if (chosenTile.suit not in ('萬', '筒', '索')):
                    continue;
                possible_chow = [
                    Card(chosenTile.suit, chosenTile.rank),
                    Card(chosenTile.suit, chosenTile.rank + 1),
                    Card(chosenTile.suit, chosenTile.rank + 2)
                ]
                if all(any(tile == chow_tile for tile in remaining_tiles) for chow_tile in possible_chow):
                    melds.append(possible_chow)
                    for possibleTile in possible_chow:
                        remaining_tiles.remove(possibleTile)
                    print("Melds: ", len(melds), len(melds[0]))
                    print("Remaining Tiles: ", len(remaining_tiles));
            for meld in melds:
                for tile in meld:
                    print(tile.suit, tile.rank);
                print("next meld")
            print("Remaining Tiles: ", len(remaining_tiles));
            for tile in remaining_tiles:
                print(tile.suit, tile.rank);
            print("Pair: ", pair[0].suit, pair[0].rank, pair[1].suit, pair[1].rank);
            return len(remaining_tiles) == 0, melds + [pair]
    return False, [];
'''
def break_into_melds_and_pair(tiles: list[Card]) -> tuple[bool, list[list[Card]]]:
    """Break down tiles into 4 melds and a pair if possible."""
    # Case: only 1 pair remaining
    if (len(tiles) == 2):
        return is_valid_pair(tiles), [tiles];

    # Sort tiles for deterministic processing
    tiles.sort(key=lambda tile: (tile.suit, tile.rank))

    # Try every possible pair
    for i in range(len(tiles) - 1):
        if tiles[i].suit == tiles[i + 1].suit and tiles[i].rank == tiles[i + 1].rank:
            # Found a valid pair
            pair = [tiles[i], tiles[i + 1]]

            # Remove the pair from remaining_tiles
            remaining_tiles = tiles[:i] + tiles[i+2:]
            melds = []

            if (find_melds(remaining_tiles, melds)):
                return True, melds + [pair]

            # Backtrack and try the next pair
            continue
    
    # If no valid pair leads to a solution
    return False, []

def find_melds(tiles: list[Card], melds: list[list[Card]]) -> bool:
    """Recursively find melds, including Kongs, in the remaining tiles.""" 
    if not tiles:
        return True
           
    # Step 1: Check for Pongs and Kongs
    counter_tiles = Counter((tile.suit, tile.rank) for tile in tiles)
    for (suit, rank), count in counter_tiles.items():
        if count >= 3:
            meld = [Card(suit, rank)] * 3
            melds.append(meld)
            for _ in range(3):
                tiles.remove(Card(suit, rank))
            if find_melds(tiles, melds):
                return True
            melds.pop()  # Backtrack
            for _ in range(3):
                tiles.append(Card(suit, rank))
            tiles.sort(key=lambda tile: (tile.suit, tile.rank))

    # Step 2: Check for Chows
    for chosen_tile in tiles[:]:
        if chosen_tile.suit not in ('萬', '筒', '索'):
            continue
        possible_chow = [
            Card(chosen_tile.suit, chosen_tile.rank),
            Card(chosen_tile.suit, chosen_tile.rank + 1),
            Card(chosen_tile.suit, chosen_tile.rank + 2),
        ]
        if all(any(tile == chow_tile for tile in tiles) for chow_tile in possible_chow):
            melds.append(possible_chow)
            for chow_tile in possible_chow:
                tiles.remove(chow_tile)
            if find_melds(tiles, melds):
                return True
            melds.pop()  # Backtrack
            for chow_tile in possible_chow:
                tiles.append(chow_tile)
            tiles.sort(key=lambda tile: (tile.suit, tile.rank))

    return False
