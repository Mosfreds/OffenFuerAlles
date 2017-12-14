import game
import json
import copy
import time

from pprint import pprint

MIN_TURN = 0
MAX_TURN = 1




def progress_game(game_state, hero, move):
    """Let the hero perform a move on the given game field"""

    # copy current game state
    new_game_state = copy.deepcopy(game_state)
    new_hero = new_game_state.get_hero(hero.bot_id)

    old_x, old_y = new_hero.pos
    new_x, new_y = new_hero.pos
    is_vertical_move = False

    # get new position
    if move == 'North':
        new_x -= 1
        is_vertical_move = True
    elif move == 'West':
        new_y -= 1
    elif move == 'South':
        new_x += 1
        is_vertical_move = True
    elif move == 'East':
        new_y += 1
    else:
        return do_logic(new_game_state, new_hero)

    # if out of bounds
    if new_x < 0 or new_x > new_game_state.board_size:
        return do_logic(new_game_state, new_hero)
    if new_y < 0 or new_y > new_game_state.board_size:
        return do_logic(new_game_state, new_hero)

    # get symbols
    new_pos_sym = new_game_state.board_map[new_x][new_y]
    swap_sym = new_game_state.get_symbol_at_loc(
        old_x, old_y)

    # check if new position is wall or another hero
    if new_pos_sym == '#' or new_pos_sym == 'H' or new_pos_sym == '@':
        return do_logic(new_game_state, new_hero)

    # change position
    new_hero.pos = (new_x, new_y)

    new_hero.bot_last_move = move

    # adapt the game field
    if is_vertical_move:
        # two rows need to be changed
        old_line_before = ''
        old_line_after = ''

        if old_y > 0:
            old_line_before = new_game_state.board_map[old_x][0:old_y]

        if old_y < new_game_state.board_size:
            old_line_after = new_game_state.board_map[old_x][old_y + 1:]

        new_line_before = ''
        new_line_after = ''

        if new_y > 0:
            new_line_before = new_game_state.board_map[new_x][0:new_y]
        if new_y < new_game_state.board_size:
            new_line_after = new_game_state.board_map[new_x][new_y + 1:]

        new_game_state.board_map[new_x] = new_line_before + hero.sym + new_line_after
        new_game_state.board_map[old_x] = old_line_before + swap_sym + old_line_after

    else:
        # only one row needs to be changed
        line_before = ''
        line_after = ''

        if old_y > 0:
            line_before = new_game_state.board_map[old_x][0:min(old_y, new_y)]
        if new_y < new_game_state.board_size:
            line_after = new_game_state.board_map[old_x][max(old_y, new_y) + 1:]

        if new_y < old_y:
            new_game_state.board_map[old_x] = line_before + hero.sym + swap_sym + line_after
        else:
            new_game_state.board_map[old_x] = line_before + swap_sym + hero.sym + line_after

    return do_logic(new_game_state, new_hero)


def do_logic(game_state, hero):
    """
    Evaluates the game field at the end of the turn
    and does the logic stuff

    """
    current_pos_sym = game_state.get_symbol_at_loc(
        hero.pos[0], hero.pos[1])

    # active hero stands on a mine
    if current_pos_sym == '$':

        # search for the mine
        for m in game_state.mines_locs:

            # standing on the mine
            if m[0] == hero.pos[0] and m[1] == hero.pos[1]:

                # this mine does not belongs to the hero
                if game_state.mines[m] == '-':
                    mine_owner_id = 0
                else:
                    mine_owner_id = int(game_state.mines[m])

                if not int(game_state.mines[m]) == int(hero.bot_id):

                    # check if someone else owns the mine
                    mine_owner = None

                    if mine_owner_id > 0:
                        mine_owner = game_state.get_hero(mine_owner_id)

                    # fight for the mine
                    hero.change_life(-20)

                    # still alive
                    if hero.is_alive():

                        # get the mine
                        hero.mines.append(m)
                        game_state.mines[m] = hero.id

                        # mine owner loses the mine
                        if mine_owner is not None:
                            mine_owner.mines.remove(m)

                    else:
                        # move hero to spawn position
                        game_state.let_hero_die(hero)

    # active hero stands on a tavern
    elif current_pos_sym == 'T':
        hero.rest()

    # attack nearby heros
    for h in game_state.heroes:
        h_distance = abs(hero.pos[0] - h.pos[0]) + abs(hero.pos[1] - h.pos[1])
        if h_distance == 1:
            hero.attack_hero(game_state, h)
            if not h.is_alive():
                game_state.let_hero_die(h)

    # get gold
    hero.earn_money()

    # thirst
    hero.being_thirsty()

    game_state.uncrash_heros()

    return game_state


def evaluate_game_state(game_state):
    return game_state.get_gold() * 100 / game_state.get_life()


def generate_moves(game_state, hero):
    """Generates possible moves for a player, without evaluating them.
    Returns an array containing a subset of [(hero, "North"), (hero, "East"), (hero, "South"), (hero, "West"),
    (hero, "Stay"]
    """
    x, y = hero.pos
    moves = ["Stay"]

    if x > 0 and game_state.board_map[x - 1][y] != '#':
        moves.append("West")
    if x < game_state.board_size - 1 and game_state.board_map[x + 1][y] != '#':
        moves.append("East")
    if y > 0 and game_state.board_map[x][y - 1] != '#':
        moves.append("North")
    if y < game_state.board_size - 1 and game_state.board_map[x][y + 1] != '#':
        moves.append("South")

    return [(hero, m) for m in moves]


def opponents(game_state):
    return [h for h in game_state.heroes if h.bot_id != game_state.hero_id]


def search(alpha, beta, depth, turn, game_state):
    """
    if depth <= 0:
        #return eval()

    moves = []
    if turn == MAX_TURN:
        moves = generate_moves(max_player)
        turn = MIN_TURN
    else:
        for o in opponents:
            moves += generate_moves(o)
        turn = MAX_TURN

    for m in moves:
        do_move(m)
        v = -search(-beta, -alpha, depth-1, turn)
        undo_move(m)

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha
    """
    if depth <= 0:
        return evaluate_game_state(game_state)

    moves = []
    if MAX_TURN == turn:
        moves = generate_moves(
            game_state, game_state.get_hero())
        turn = MIN_TURN
    else:
        for o in opponents(game_state):
            for m in generate_moves(game_state, o):
                moves.append(m)
        turn = MAX_TURN

    for m in moves:
        new_state = progress_game(game_state, m[0], m[1])
        v = -search(-alpha, -beta, depth - 1, turn, new_state)

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha


if __name__ == "__main__":

    json_file = open('test/example_state.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)
    game = game.Game(json_data)

    print(len(game.board_map), len(game.board_map[0]), game.board_size)
    for i in range(len(game.board_map)):
        print(game.board_map[i])
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))
    t = time.time() * 1000.0
    game = progress_game(game, game.heroes[3], 'South')
    t = (time.time() * 1000.0) - t
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))

    game = progress_game(game, game.heroes[0], 'South')
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))

    game = progress_game(game, game.heroes[3], 'South')
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))
    game = progress_game(game, game.heroes[0], 'East')
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))

    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')
    game = progress_game(game, game.heroes[2], 'North')

    game = progress_game(game, game.heroes[1], 'North')
    game = progress_game(game, game.heroes[1], 'East')
    game = progress_game(game, game.heroes[1], 'East')
    game = progress_game(game, game.heroes[1], 'East')
    game = progress_game(game, game.heroes[1], 'East')
    game = progress_game(game, game.heroes[1], 'East')
    game = progress_game(game, game.heroes[1], 'South')

    game = progress_game(game, game.heroes[3], 'Stay')
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))
    for i in range(len(game.board_map)):
        print(game.board_map[i])
    game = progress_game(game, game.heroes[0], 'Stay')
    print(game.get_gold(), game.get_life(), len(game.get_hero().mines))
    print(game.heroes[0].gold, game.heroes[0].life, len(game.heroes[0].mines))
    game = progress_game(game, game.heroes[2], 'North')
    for i in range(len(game.board_map)):
        print(game.board_map[i])
    print(t, ' nano s')
    #new_game = progress_game(game, game.heroes[3], 'North')
    #new_game = progress_game(new_game, new_game.heroes[3], 'West')
    #for i in range(len(new_game.board_map)):
    #    print(new_game.board_map[i])

    #print(new_game.get_gold(), new_ga#me.get_life())
    # new_game2 = progress_game(new_game, new_game.heroes[2], 'North')
    # for i in range(len(new_game2.board_map)):
    #    print(new_game2.board_map[i])

    # for l in new_game2.heroes_locs:
    #    print(l)
