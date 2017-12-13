class BRS:
    MIN_TURN = 0
    MAX_TURN = 1

    def progress_game(self, game_state, hero, move):
        pass

    def search(alpha, beta, depth, turn):
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
        pass
