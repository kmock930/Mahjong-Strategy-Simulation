from mjai import Bot
import sys

class RulebaseBot(Bot):
    def think(self) -> str:
        if self.can_tsumo_agari:
            return self.action_tsumo_agari()
        elif self.can_ron_agari:
            return self.action_ron_agari()
        elif self.can_riichi:
            return self.action_riichi()

        ...

if __name__ == "__main__":
    RulebaseBot(player_id=int(sys.argv[1])).start()