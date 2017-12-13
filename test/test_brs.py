import brs
import game
import json
import unittest

from pprint import pprint


class TestBrs(unittest.TestCase):
    def setUp(self):
        with open('example_state.json') as data_file:
            self.game = game.Game(json.load(data_file))



    def test_generate_moves(self):
        m = brs.generate_moves(self.game, self.game.hero)
        self.assertEqual(len(m), 5)
        pprint(m)

        m = brs.generate_moves(self.game, self.game.heroes[1])
        self.assertEqual(len(m), 3)

        m = brs.generate_moves(self.game, self.game.heroes[2])
        self.assertEqual(len(m), 3)

        m = brs.generate_moves(self.game, self.game.heroes[3])
        self.assertEqual(len(m), 5)


    def test_opponents(self):
        opponents = brs.opponents(self.game)
        self.assertEqual(len(opponents), 3)
        self.assertEqual([], [h for h in opponents if h.bot_id == self.game.hero.bot_id])


    def test_print_map(self):
        for l in self.game.board_map:
            print(l)
