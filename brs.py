import game
import json
import copy
import time

from pprint import pprint

MIN_TURN = 0
MAX_TURN = 1


def progress_game(game_state, hero, move):
    """Let the hero perform a move on the given game field"""

    game_state = copy.deepcopy(game_state)
    hero = next(x for x in game_state.heroes if x == hero)

    if 'North' == move:
        hero.pos = ( hero.pos[0], hero.pos[1]-1 )
    elif 'East' == move:
        hero.pos = ( hero.pos[0]+1, hero.pos[1] )
    elif 'South' == move:
        hero.pos = ( hero.pos[0], hero.pos[1]+1 )
    elif 'West' == move:
        hero.pos = ( hero.pos[0]-1, hero.pos[1] )
    elif 'Stay' == move:
        pass
    else:
        raise Exception("Eeeh, unknown direction")

    if hero.pos in game_state.mines_locs:
        hero.change_life(-20)
        hero.gold += 1
        if game_state.get_hero() == hero:
            print("Yay, we mined!")
        else:
            print("Booh, the enemy mined!")

    if game_state.get_gold() > 0:
        print("Yay, we got some gold! {}".format(game_state.get_gold()))
    return game_state


def evaluate_game_state(hero):
    return hero.gold


def generate_moves(game_state, hero):
    """Generates possible moves for a player, without evaluating them.
    Returns an array containing a subset of [(hero, "North"), (hero, "East"), (hero, "South"), (hero, "West"),
    (hero, "Stay"]
    """
    x, y = hero.pos
    moves = []

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


def search(alpha, beta, depth, turn, game_state, hero):
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
        return evaluate_game_state(hero)

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
        v = -search(-alpha, -beta, depth - 1, turn, new_state, m[0])

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

