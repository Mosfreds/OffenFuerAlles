import game

class BRS:
    MIN_TURN = 0
    MAX_TURN = 1

    def progress_game(self, game_state, hero, move):
        hero_num = 0
        for h in game_state.heroes:
            if hero.id == h.id:
                break
            hero_num += 1

        hero_loc = game_state.heroes_locs[hero_num]


        return game_state.hero.gold()

    def evalute_game_state(self, game):
        pass

    def generate_moves(self, game_state, player):
        """Generates possible moves for a player, without evaluating them.
        Returns an array containing a subset of ["North", "East", "South", "West", "Stay"]
        """
        pass

    def search(self, alpha, beta, depth, turn):
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
