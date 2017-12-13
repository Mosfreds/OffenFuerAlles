#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# Pure random A.I, you may NOT use it to win ;-)
#
########################################################################

import brs
import random

from operator import itemgetter

class AI:
    """Pure random A.I, you may NOT use it to win ;-)"""
    def __init__(self):
        pass

    def process(self, game):
        """Do whatever you need with the Game object game"""
        self.game = game

    def decide(self):
        """Must return a tuple containing in that order:
          1 - path_to_goal :
                  A list of coordinates representing the path to your
                 bot's goal for this turn:
                 - i.e: [(y, x) , (y, x), (y, x)]
                 where y is the vertical position from top and x the
                 horizontal position from left.

          2 - action:
                 A string that will be displayed in the 'Action' place.
                 - i.e: "Go to mine"

          3 - decision:
                 A list of tuples containing what would be useful to understand
                 the choice you're bot has made and that will be printed
                 at the 'Decision' place.

          4- hero_move:
                 A string in one of the following: West, East, North,
                 South, Stay

          5 - nearest_enemy_pos:
                 A tuple containing the nearest enenmy position (see above)

          6 - nearest_mine_pos:
                 A tuple containing the nearest enenmy position (see above)

          7 - nearest_tavern_pos:
                 A tuple containing the nearest enenmy position (see above)"""

        SEARCH_DEPTH = 100/20 + 1   # Look one fight ahead.
        alpha = brs.progress_game(self.game, self.game.hero, "Stay").hero.gold
        beta = min(self.game.heroes, key=lambda h : h.gold).gold
        possible_moves = brs.generate_moves(self.game, self.game.hero)
        actions = [i[1] for i in possible_moves]
        decisions = [(a, brs.search(alpha,
                                    beta,
                                    SEARCH_DEPTH,
                                    brs.MAX_TURN,
                                    brs.progress_game(self.game, self.game.hero, a))) for a in actions]
        best_action = max(decisions, key=itemgetter(1))

        path_to_goal = []
        nearest_enemy_pos = random.choice(self.game.heroes).pos
        nearest_mine_pos = random.choice(self.game.mines_locs)
        nearest_tavern_pos = random.choice(self.game.mines_locs)

        return (path_to_goal,
                best_action[0],
                decisions,
                best_action[0],
                nearest_enemy_pos,
                nearest_mine_pos,
                nearest_tavern_pos)


if __name__ == "__main__":
    pass
