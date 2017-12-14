#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Hero:
    """The Hero object"""
    def __init__(self, hero):
        try:
            # Training bots have no elo or userId
            self.elo = hero['elo']
            self.user_id = hero['userId']
            self.bot_last_move = hero['lastDir']
        except KeyError:
            self.elo = 0
            self.user_id = 0
            self.last_move = None

        self.bot_id = hero['id']
        self.life = hero['life']
        self.gold = hero['gold']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.spawn_pos = (hero['spawnPos']['x'], hero['spawnPos']['y'])
        self.crashed = hero['crashed']
        self.mine_count = hero['mineCount']
        self.mines = []
        self.name = hero['name']
        self.sym = 'H'

    def rest(self):
        if self.gold >= 2:
            self.gold -= 2
            self.life = min(self.life + 50, 100)

    def change_life(self, add_life):
        self.life = min(self.life + add_life, 100)

        if self.life <= 0:
            self.die()

    def being_thirsty(self):
        self.life = max(self.life -1, 1)

    def attack_hero(self, game, defender):
        defender.change_life(-20)
        if not defender.is_alive():
            for mine in defender.mines:
                self.mines.append(mine)
                game.mines[mine] = self.bot_id

            defender.mines = []
        return

    def die(self):
        self.crashed = True

    def earn_money(self):
        self.gold += len(self.mines)

    def is_alive(self):
        return not self.crashed and self.life > 0

class Game:
    """The game object that gather
    all game state informations"""
    def __init__(self, state):
        self.state = state
        self.mines = {}
        self.mines_locs = []
        self.spawn_points_locs = {}
        self.taverns_locs = []
        self.hero_id = None
        self.heroes = []
        self.heroes_locs = []
        self.walls_locs = []
        self.url = None
        self.turn = None
        self.max_turns = None
        self.finished = None
        self.board_size = None
        self.board_map = []

        self.process_data(self.state)

    #@property
    #def hero(self):
    #    for hero in self.heroes:
    #        if hero.bot_id == self.hero_id:
    #            return hero

    #@hero.setter
    #def hero(self, h):
    #    for i in range(len(self.heroes)):
    #        if self.heroes[i].bot_id == self.hero_id:
    #            self.heroes[i] = h

    def process_data(self, state):
        """Parse the game state"""
        self.set_url(state['viewUrl'])
        self.process_hero(state['hero'])
        self.process_game(state['game'])

    def set_url(self, url):
        """Set the game object url var"""
        self.url = url

    def process_hero(self, hero):
        """Process the hero data"""
        self.hero_id = Hero(hero).bot_id

    def process_game(self, game):
        """Process the game data"""
        process = {'board': self.process_board,
                    'heroes': self.process_heroes}
        self.turn = game['turn']
        self.max_turns = game['maxTurns']
        self.finished = game['finished']
        for key in sorted(game.keys()):  # TODO: board must go before heroes
            if key in process:
                process[key](game[key])

        for hero in self.heroes:
            for mloc in self.mines_locs:
                if not self.mines[mloc] == '-':
                    if int(self.mines[mloc]) == hero.bot_id:
                        hero.mines.append(mloc)
        self.get_hero().sym = '@'

    def process_board(self, board):
        """Process the board datas
            - Retrieve walls locs, tavern locs
            - Converts tiles in a displayable form"""
        self.board_size = board['size']
        tiles = board['tiles']
        map_line = ""
        char = None
        for y in range(0, len(tiles), self.board_size * 2):
            line = tiles[y:y+self.board_size*2]
            for x in range(0, len(line), 2):
                tile = line[x:x+2]
                tile_coords = (y//self.board_size//2, x//2)
                if tile[0] == " ":
                    # It's passable
                    char = " "
                elif tile[0] == "#":
                    # It's a wall
                    char = "#"
                    self.walls_locs.append(tile_coords)
                elif tile[0] == "$":
                    # It's a mine
                    char = "$"
                    self.mines_locs.append(tile_coords)
                    self.mines[tile_coords] = tile[1]
                    #if tile[1] == str(self.hero.bot_id):
                     #   # This mine is belong to me:-)
                      #  self.hero.mines.append(tile_coords)
                elif tile[0] == "[":
                    # It's a tavern
                    char = "T"
                    self.taverns_locs.append(tile_coords)
                elif tile[0] == "@":
                    # It's a hero
                    char = "H"
                    self.heroes_locs.append(tile_coords)
                    if int(tile[1]) == self.hero_id:
                        char = "@"

                map_line = map_line + str(char)
            self.board_map.append(map_line)
            map_line = ""

    def process_heroes(self, heroes):
        """Add heroes"""
        for hero in heroes:
            self.spawn_points_locs[(hero['spawnPos']['y'], hero['spawnPos']['x'])] = hero['id']
            self.heroes.append(Hero(hero))

            # Add spawn points to map
            line = list(self.board_map[int(hero['spawnPos']['x'])])

            if line[int(hero['spawnPos']['y'])] != "@" and \
                    line[int(hero['spawnPos']['y'])] != "H":
                line[int(hero['spawnPos']['y'])] = "X"
            line = "".join(line)
            self.board_map[int(hero['spawnPos']['x'])] = line

    def get_hero(self, hero_id=None):
        if hero_id is None:
            hero_id = self.hero_id
        for hero in self.heroes:
            if hero.bot_id == hero_id:
                return hero

    def let_hero_die(self, hero):
        old_x, old_y = hero.pos
        new_x, new_y = hero.spawn_pos

        ori_sym = self.get_symbol_at_loc(hero.pos[0], hero.pos[1])
        cur_sym = self.board_map[hero.pos[0]][hero.pos[1]]

        if not cur_sym == hero.sym:
            ori_sym = cur_sym
        #elif not (old_x == new_x and old_y == new_y):
         #   ori_sym = self.board_map[hero.spawn_pos[0]][hero.spawn_pos[1]]
        #elif(not old_x == new_x) or (not old_y == new_y):
        #    ori_sym = cur_sym

        if old_x == new_x:
            line_before = ''
            line_middle = ''
            line_after = ''

            line_before = self.board_map[old_x][0:min(old_y, new_y)]
            line_middle = self.board_map[old_x][min(old_y, new_y)+1:max(old_y, new_y)]
            line_after = self.board_map[old_x][max(old_y, new_y)+1:]
            if old_y < new_y:
                self.board_map[old_x] = line_before \
                                        + ori_sym + line_middle \
                                        + hero.sym + line_after
            else:
                self.board_map[old_x] = line_before \
                                        + hero.sym + line_middle \
                                        + ori_sym + line_after
        else:
            old_line_before = ''
            old_line_after = ''

            if old_y > 0:
                old_line_before = self.board_map[old_x][0:old_y]

            if old_y < self.board_size:
                old_line_after = self.board_map[old_x][old_y + 1:]

            new_line_before = ''
            new_line_after = ''

            if new_y > 0:
                new_line_before = self.board_map[new_x][0:new_y]
            if new_y < self.board_size:
                new_line_after = self.board_map[new_x][new_y + 1:]

            self.board_map[new_x] = new_line_before + hero.sym + new_line_after
            self.board_map[old_x] = old_line_before + ori_sym + old_line_after

        hero.pos = hero.spawn_pos
        hero.life = 100
        for mine in hero.mines:
            self.mines[mine] = '-'
        hero.mines = []

        for h in self.heroes:
            if h.pos == hero.pos:
                if not h.bot_id == hero.bot_id:
                    self.let_hero_die(h)

    def uncrash_heros(self):
        for h in self.heroes:
            h.crashed = False

    def get_life(self):
        return self.get_hero(self.hero_id).life

    def get_gold(self):
        return self.get_hero(self.hero_id).gold

    def get_symbol_at_loc(self, x, y):
        """Returns the symbol which is under the hero"""
        current_sym = self.board_map[x][y]

        if current_sym == "H" or current_sym == "@":

            # check for mines
            for pos in self.mines_locs:
                if pos[0] == x and pos[1] == y:
                    return '$'

            # check for spawn points
            for pos in self.spawn_points_locs:
                if pos[1] == x and pos[0] == y:
                    return 'X'

            # check for taverns
            for pos in self.taverns_locs:
                if pos[0] == x and pos[1] == y:
                    return 'T'

            # just an empty field
            return ' '
        else:
            return current_sym