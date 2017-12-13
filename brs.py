import game
import json
import copy

from pprint import pprint

MIN_TURN = 0
MAX_TURN = 1


def get_symbol_at_loc(game_state, x, y):
    current_sym = game_state.board_map[x][y]

    if current_sym == "H" or current_sym == "@":
        for pos in game_state.mines_locs:
            if pos[0] == x and pos[1] == y:
                return '$'
        for pos in game_state.spawn_points_locs:
            if pos[0] == x and pos[1] == y:
                return 'X'
        for pos in game_state.taverns_locs:
            if pos[0] == x and pos[1] == y:
                return 'T'
        return ' '
    else:
        return current_sym


def progress_game(game_state, hero, move):

    # check if this is out hero
    is_our_hero = game_state.hero.bot_id == hero.bot_id

    # copy current game state
    new_game_state = copy.deepcopy(game_state)

    old_x = hero.pos[0]
    old_y = hero.pos[1]
    new_x = hero.pos[0]
    new_y = hero.pos[1]
    is_vertical_move = False;

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
        return new_game_state

    # if out of bounds
    if new_x < 0 or new_x > new_game_state.board_size:
        return new_game_state
    if new_y < 0 or new_y > new_game_state.board_size:
        return new_game_state

    # get symbols
    hero_sym = new_game_state.board_map[old_x][old_y]
    new_pos_sym = new_game_state.board_map[new_x][new_y]
    swap_sym = get_symbol_at_loc(new_game_state, old_x, old_y)

    # check if new position is wall or another hero
    if new_pos_sym == '#' or new_pos_sym == 'H' or new_pos_sym == '@':
        return new_game_state

    # change position
    if is_our_hero:
        new_game_state.hero.pos = (new_x, new_y)

    # change position in heroes list
    for j in range(len(new_game_state.heroes)):
        if hero.bot_id == new_game_state.heroes[j].bot_id:
            new_game_state.heroes[j].pos = (new_x, new_y)
            if not is_our_hero:
                new_game_state.heroes_locs[j] = (new_x, new_y)

    if is_vertical_move:
        old_line_before = ''
        old_line_after = ''

        if old_y > 0:
            old_line_before = new_game_state.board_map[old_x][0:old_y]

        if old_y < new_game_state.board_size:
            old_line_after = new_game_state.board_map[old_x][old_y+1:]

        new_line_before = ''
        new_line_after = ''

        if new_y > 0:
            new_line_before = new_game_state.board_map[new_x][0:new_y]
        if new_y < new_game_state.board_size:
            new_line_after = new_game_state.board_map[new_x][new_y+1:]

        new_game_state.board_map[new_x] = new_line_before + hero_sym + new_line_after
        new_game_state.board_map[old_x] = old_line_before + swap_sym + old_line_after

    else:
        line_before = ''
        line_after = ''

        if old_y > 0:
            line_before = new_game_state.board_map[old_x][0:min(old_y, new_y)]
        if new_y < new_game_state.board_size:
            line_after = new_game_state.board_map[old_x][max(old_y, new_y)+1:]

        if new_y < old_y:
            new_game_state.board_map[old_x] = line_before + hero_sym + swap_sym + line_after
        else:
            new_game_state.board_map[old_x] = line_before + swap_sym + hero_sym + line_after

    return new_game_state

def evalute_game_state(game_state):
    return game_state.hero.gold * 100 / game_state.hero.life


def generate_moves(game_state, hero):
    """Generates possible moves for a player, without evaluating them.
    Returns an array containing a subset of [(hero, "North"), (hero, "East"), (hero, "South"), (hero, "West"),
    (hero, "Stay"]
    """
    x, y = hero.pos
    moves = ["Stay"]

    if x > 0 and game_state.board_map[x-1][y] != '#':
        moves.append("West")
    if x < game_state.board_size - 1 and game_state.board_map[x+1][y] != '#':
        moves.append("East")
    if y > 0 and game_state.board_map[x][y-1] != '#':
        moves.append("North")
    if y < game_state.board_size - 1 and game_state.board_map[x][y+1] != '#':
        moves.append("South")

    return [(hero, m) for m in moves]


def opponents(game_state):
    return [h for h in game_state.heroes if h.bot_id != game_state.hero.bot_id]


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
        return evalute_game_state(game_state)

    moves = []
    if MAX_TURN == turn:
        moves = generate_moves(game_state, game_state.hero)
        turn = MIN_TURN
    else:
        for o in opponents(game_state):
            for m in generate_moves(game_state, o):
                moves.append(m)
        turn = MAX_TURN

    for m in moves:
        new_state = progress_game(game_state, m[0], m[1])
        v = -search(-alpha, -beta, depth-1, turn, new_state)

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha
