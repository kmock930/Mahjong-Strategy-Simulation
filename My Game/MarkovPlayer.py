from player import Player;
from Card import Card;
from Rules import Rules;
from gameLog import GameLog;
from utils import is_valid_meld;

class MarkovPlayer(Player):
    discarded_tiles: list[Card]
    models: dict[str, dict]

    def __init__(self, Id: int, wind: str, hand: list, logger: GameLog = None, openMelds: list[list[Card]] = [], discardedTiles: list[Card] = []):
        super().__init__(Id, wind, hand, logger)
        self.discarded_tiles = discardedTiles
        self.models = {
            "chow": self.initialize_models(),
            "pong": self.initialize_models(),
            "kong": self.initialize_models(),
            "win": self.initialize_models(),
        }

    def initialize_models(self):
        """
        Initialize a simple Markov model for each action.
        This could be a dictionary storing state-action frequencies.
        """
        return {}
    
    def update_models(self, action: str, state, next_state, reward: int|float|None):
        """
        Update the Markov model for the given action.
        :param action: The action taken.
        :param state: The current state.
        :param next_state: The resulting state after the action.
        :param reward: The reward received for this transition.
        """
        # Error handling
        if action not in self.models:
            raise ValueError(f"Invalid action: {action}")
        key = (tuple(state["hand"]), action, tuple(next_state["hand"]))
        if key not in self.models[action]:
            self.models[action][key] = {"count": 0, "reward": 0}

        self.models[action][key]["count"] += 1
        self.models[action][key]["reward"] += reward

    def predict(self, action, state):
        """
        Predict the expected reward for a given action in the current state.
        :param action: The action to evaluate.
        :param state: The current state.
        :return: Expected reward for the action.
        """
        if action not in self.models:
            raise ValueError(f"Invalid action: {action}")

        best_reward = float("-inf")
        for (stored_state, stored_action, stored_next_state), data in self.models[action].items():
            if tuple(state["hand"]) == stored_state and stored_action == action:
                avg_reward = data["reward"] / data["count"]
                if avg_reward > best_reward:
                    best_reward = avg_reward

        return best_reward if best_reward != float("-inf") else 0
    
    def choose_action(self, state, legal_actions: list):
        """
        Decide the best action to take based on the Markov models.
        :param state: The current state of the game.
        :param legal_actions: A list of legal actions available in the current state.
        :return: The chosen action.
        """
        best_action = None
        best_reward = float("-inf")

        for action in legal_actions:
            expected_reward = self.predict(action, state)
            if expected_reward > best_reward:
                best_reward = expected_reward
                best_action = action
        return best_action

    def play_turn(self, game_state, legal_actions):
        """
        Play a turn in the game by choosing the best action and updating the models.
        :param game_state: The current game state.
        :param legal_actions: Legal actions available for the player.
        """
        action = self.choose_action(game_state, legal_actions)
        next_state, reward = self.simulate_action(action, game_state)
        self.update_models(action, game_state, next_state, reward)
        return action

    def simulate_action(self, action, state):
        """
        Simulate the result of an action to update models.
        :param action: The action to simulate.
        :param state: The current state.
        :return: A tuple of (next_state, reward).
        """
        # Implement specific logic for simulating the result of actions
        next_state = state.copy()
        if "ID" in state:
            next_state["ID"] = state["ID"] + 1 if state["ID"] is not None else None
        reward = 0

        if action == "discard":
            tile_to_discard = state["hand"][0]  # Example: Discard the first tile
            next_state["hand"].remove(tile_to_discard)
            next_state["discarded_tiles"].append(tile_to_discard)
            reward = -0.1  # Base penalty for discarding

        elif action == "chow":
            # Simulate Chow logic
            reward = 0.5

        elif action == "pong":
            # Simulate Pong logic
            reward = 1

        elif action == "kong":
            # Simulate Kong logic
            reward = 1.5

        elif action == "hu":
            # Simulate Hu logic (winning)
            rules_nextState = Rules(
                incomingTile=Card.decode(state["action_tile"]),
                closedDeck=next_state["hand"],
                openDeck=next_state.get("open_melds", []), # optional
                incomingPlayerId=state["action_player"],
                currentPlayerId=self.Id,
                gameID=state["gameID"],
                upperScoreLimit=state["upperScoreLimit"],
                flowerDeck=next_state.get("flowers", []) # optional
            )
            winning_score = rules_nextState.evalScore(
                isFirstRound=next_state["ID"]==0,
                isLastPlayer=len(self.discarded_tiles) == 4 # next round will be the last player
            )
            reward = 10
            if (winning_score is not None):
                reward += winning_score

        return next_state, reward

    # Override the default discard strategy
    def discard(self):
        """
        Override the default discard strategy with a Markov-based decision.
        """
        # Simulate and evaluate discarding each tile
        best_tile = None
        best_reward = float("-inf")
        for tile in self.hand:
            hypothetical_state = {
                "hand": [t for t in self.hand if t != tile],
                "open_melds": self.openHand,
                "discarded_tiles": self.discarded_tiles + [tile]
            }
            _, reward = self.simulate_action("discard", hypothetical_state)
            if reward > best_reward:
                best_tile = tile
                best_reward = reward

        # Log and perform the discard
        if best_tile:
            self.hand.remove(best_tile)
            self.logger.log_move(self.Id, f"discards a tile: {best_tile.suit}-{best_tile.rank}")
        return best_tile

    # Override the default handleSpecialActions
    def handleSpecialActions(self, tile: Card, oppID: int):
        """
        Override to handle special actions based on Markov model predictions.
        """
        if tile is None:
            return None

        legal_actions = []
        if self.canChow(self.hand, tile, oppID):
            legal_actions.append("chow")
        if self.canPong(self.hand, tile):
            legal_actions.append("pong")
        if self.canGong(self.hand, tile):
            legal_actions.append("kong")

        best_action = self.choose_action(
            {"hand": self.hand, "open_melds": self.openHand, "discarded_tiles": self.discarded_tiles},
            legal_actions
        )

        if best_action == "chow":
            meld = self.find_best_chow_meld(tile)
            return self.chow(tile, meld)
        elif best_action == "pong":
            return self.pong(tile)
        elif best_action == "kong":
            return self.kong(tile)
        return None

    def find_best_chow_meld(self, tile: Card):
        """
        Find the best chow meld to form with the given tile.
        :param tile: The tile to form a chow with.
        :return: The best chow meld as a list of cards.
        """
        potential_melds = []
        for i in range(len(self.hand) - 1):
            for j in range(i + 1, len(self.hand)):
                meld = [self.hand[i], self.hand[j], tile]
                if is_valid_meld(meld):
                    potential_melds.append(meld)

        best_meld = None
        best_reward = float("-inf")
        for meld in potential_melds:
            hypothetical_state = {
                "hand": [t for t in self.hand if t not in meld],
                "open_melds": self.openHand + [meld],
                "discarded_tiles": self.discarded_tiles
            }
            _, reward = self.simulate_action("chow", hypothetical_state)
            if reward > best_reward:
                best_meld = meld
                best_reward = reward
        return best_meld
