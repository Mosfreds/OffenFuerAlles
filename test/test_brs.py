import brs
import game
import json
import unittest

from pprint import pprint


class TestBrs(unittest.TestCase):
    def setUp(self):
        with open('example_state.json') as data_file:
            self.game = game.Game(json.load(data_file))
        pprint(self.game)



    def test_generate_moves(self):
        pprint(brs.BRS().generate_moves(self.game, self.game.hero))
