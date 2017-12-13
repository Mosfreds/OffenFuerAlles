import game

MIN_TURN = 0
MAX_TURN = 1

def progress_game(game_state, hero, move):
    return game_state

def evalute_game_state(game_state):
    return game_state.hero.gold


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
            moves.append(generate_moves(game_state, o))
        turn = MAX_TURN

    for m in moves:
        new_state = progress_game(game_state, m[0], m[1])
        v = -search(-alpha, -beta, depth-1, turn, new_state)

        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha
