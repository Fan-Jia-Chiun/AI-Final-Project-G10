from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from chinese_chess.pieces.advisor import Advisor
from chinese_chess.pieces.chariot import Chariot
from chinese_chess.pieces.canon import Canon
from chinese_chess.pieces.elephant import Elephant
from chinese_chess.pieces.general import General
from chinese_chess.pieces.horse import Horse
from chinese_chess.pieces.soldier import Soldier
import numpy as np, random

def minimax(board: Board,
            depth: int,
            maximizingPlayer: bool,
            color: PieceColor,
            last_move: tuple = None):

    if depth == 0 or board.terminate():
        raw = get_heuristic(board)
        score = raw if color == PieceColor.RED else -raw
        return score, None

    if maximizingPlayer:
        best_value = -np.inf
        best_moves = set()

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != color:
                        return np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = minimax(board,
                                     depth - 1,
                                     False,
                                     color,
                                     last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val > best_value:
                        best_value = val
                        best_moves = {(old_pos, new_pos)}
                    elif val == best_value:
                        best_moves.add((old_pos, new_pos))

        return best_value, best_moves

    else:
        worst_value = np.inf
        worst_moves = set()
        opp_color = PieceColor.RED if color == PieceColor.BLACK else PieceColor.BLACK

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != opp_color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != opp_color:
                        return -np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = minimax(board,
                                     depth - 1,
                                     True,
                                     color,
                                     last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val < worst_value:
                        worst_value = val
                        worst_moves = {(old_pos, new_pos)}
                    elif val == worst_value:
                        worst_moves.add((old_pos, new_pos))

        return worst_value, worst_moves

def basic_alphabeta(board: Board,
                    depth: int,
                    maximizingPlayer: bool,
                    alpha: float,
                    beta: float,
                    color: PieceColor,
                    last_move: tuple = None):
    if depth == 0 or board.terminate():
        raw = get_basic_heuristic(board)
        score = raw if color == PieceColor.RED else -raw
        return score, None

    if maximizingPlayer:
        best_value = -np.inf
        best_moves = set()

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != color:
                        return np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = basic_alphabeta(board,
                                             depth - 1,
                                             False,
                                             alpha, beta,
                                             color,
                                             last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val > best_value:
                        best_value = val
                        best_moves = {(old_pos, new_pos)}
                    elif val == best_value:
                        best_moves.add((old_pos, new_pos))

                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        return best_value, best_moves

        return best_value, best_moves

    else:
        worst_value = np.inf
        worst_moves = set()
        opp_color = PieceColor.RED if color == PieceColor.BLACK else PieceColor.BLACK

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != opp_color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != opp_color:
                        return -np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = basic_alphabeta(board,
                                             depth - 1,
                                             True,
                                             alpha, beta,
                                             color,
                                             last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val < worst_value:
                        worst_value = val
                        worst_moves = {(old_pos, new_pos)}
                    elif val == worst_value:
                        worst_moves.add((old_pos, new_pos))

                    beta = min(beta, worst_value)
                    if beta <= alpha:
                        return worst_value, worst_moves

        return worst_value, worst_moves

def alphabeta(board: Board,
              depth: int,
              maximizingPlayer: bool,
              alpha: float,
              beta: float,
              color: PieceColor,
              last_move: tuple = None):
    if depth == 0 or board.terminate():
        raw = get_heuristic(board)
        score = raw if color == PieceColor.RED else -raw
        return score, None

    if maximizingPlayer:
        best_value = -np.inf
        best_moves = set()

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != color:
                        return np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = alphabeta(board,
                                       depth - 1,
                                       False,
                                       alpha, beta,
                                       color,
                                       last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val > best_value:
                        best_value = val
                        best_moves = {(old_pos, new_pos)}
                    elif val == best_value:
                        best_moves.add((old_pos, new_pos))

                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        return best_value, best_moves

        return best_value, best_moves

    else:
        worst_value = np.inf
        worst_moves = set()
        opp_color = PieceColor.RED if color == PieceColor.BLACK else PieceColor.BLACK

        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != opp_color:
                    continue

                for new_pos in piece.valid_moves(board):
                    if last_move is not None:
                        prev_old, prev_new = last_move
                        if new_pos == prev_old and old_pos == prev_new:
                            continue

                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != opp_color:
                        return -np.inf, {(old_pos, new_pos)}

                    board.make_move(old_pos, new_pos)
                    val, _ = alphabeta(board,
                                       depth - 1,
                                       True,
                                       alpha, beta,
                                       color,
                                       last_move=(old_pos, new_pos))
                    board.undo_move()

                    if val < worst_value:
                        worst_value = val
                        worst_moves = {(old_pos, new_pos)}
                    elif val == worst_value:
                        worst_moves.add((old_pos, new_pos))

                    beta = min(beta, worst_value)
                    if beta <= alpha:
                        return worst_value, worst_moves

        return worst_value, worst_moves

def agent_minimax(board, color: PieceColor):
    return random.choice(list(
        minimax(board, depth=3, maximizingPlayer=True, color=color, last_move=None)[1]
    ))


def agent_basic_alphabeta(board, color: PieceColor):
    return random.choice(list(
        basic_alphabeta(board, depth=4, maximizingPlayer=True,
                        alpha=-np.inf, beta=np.inf,
                        color=color, last_move=None)[1]
    ))


def agent_alphabeta(board, color: PieceColor):
    return random.choice(list(
        alphabeta(board, depth=4, maximizingPlayer=True,
                  alpha=-np.inf, beta=np.inf,
                  color=color, last_move=None)[1]
    ))


def agent_reflex(board, color: PieceColor):
    candidates = []
    for x in range(9):
        for y in range(10):
            pos = (x, y)
            piece = board.get_piece(pos)
            if piece is None or piece.color != color:
                continue
            for new_pos in piece.valid_moves(board):
                candidates.append((pos, new_pos))
    return random.choice(candidates) if candidates else None

def get_basic_heuristic(board):
    red_general = black_general = None
    for x in range(9):
        for y in range(10):
            p = board.grid[y][x]
            if isinstance(p, General):
                if p.color == PieceColor.RED:
                    red_general = (x, y)
                else:
                    black_general = (x, y)

    if red_general is None:
        return -np.inf
    if black_general is None:
        return np.inf

    WEIGHTS = {
        "material": {
            Chariot: 9.0,
            Canon:   8.0,
            Horse:   5.0,
            Elephant:3.0,
            Advisor: 3.0,
            Soldier: 1.0,
            General: 0.0
        },
        "king_threat"     : 0.5,
    }

    score = 0.0
    red_threats   = 0
    black_threats = 0
    for x in range(9):
        for y in range(10):
            piece = board.get_piece((x, y))
            if piece is None:
                continue
            val = WEIGHTS["material"].get(type(piece), 0.0)
            score += val if piece.color == PieceColor.RED else -val

            moves = piece.valid_moves(board)

            if piece.color == PieceColor.RED and black_general in moves:
                red_threats += 1
            elif piece.color == PieceColor.BLACK and red_general in moves:
                black_threats += 1
        
    score -= WEIGHTS["king_threat"] * red_threats
    score += WEIGHTS["king_threat"] * black_threats

    return score

def get_heuristic(board):
    red_general = black_general = None
    for x in range(9):
        for y in range(10):
            p = board.grid[y][x]
            if isinstance(p, General):
                if p.color == PieceColor.RED:
                    red_general = (x, y)
                else:
                    black_general = (x, y)

    if red_general is None:
        return -np.inf
    if black_general is None:
        return np.inf

    WEIGHTS = {
        "material": {
            Chariot: 9.0,
            Canon:   8.0,
            Horse:   5.0,
            Elephant:3.0,
            Advisor: 3.0,
            Soldier: 1.0,
            General: 0.0
        },
        "mobility"        : 0.15,
        "center_control"  : 0.05,
        "cross_half_major": 0.4,
        "general_pressure": 2.0,
        "soldier_adv"     : 0.2,
        "king_threat"     : 0.5,
        "capture_bonus"   : 1.2
    }

    score         = 0.0
    red_threats   = 0
    black_threats = 0

    gx_red, gy_red     = red_general
    gx_black, gy_black = black_general

    for x in range(9):
        for y in range(10):
            piece = board.get_piece((x, y))
            if piece is None:
                continue

            val = WEIGHTS["material"].get(type(piece), 0.0)
            score += (val if piece.color == PieceColor.RED else -val)

            moves = piece.valid_moves(board)
            mob   = WEIGHTS["mobility"] * len(moves)
            score += (mob if piece.color == PieceColor.RED else -mob)

            for new_pos in moves:
                target = board.get_piece(new_pos)
                if target is not None and target.color != piece.color:
                    tgt_val = WEIGHTS["material"].get(type(target), 0.0)
                    bonus  = WEIGHTS["capture_bonus"] * tgt_val
                    score += (bonus if piece.color == PieceColor.RED else -bonus)

            dx, dy = x - 4, y - 4
            center_bonus = WEIGHTS["center_control"] * (max(0, 5 - abs(dx)) + max(0, 5 - abs(dy)))
            score += (center_bonus if piece.color == PieceColor.RED else -center_bonus)

            if piece.color == PieceColor.RED and black_general in moves:
                red_threats += 1
            elif piece.color == PieceColor.BLACK and red_general in moves:
                black_threats += 1

            if isinstance(piece, Soldier):
                if piece.color == PieceColor.RED and y >= 5:
                    d = abs(y - gy_black)
                    score += WEIGHTS["soldier_adv"] * max(0, 5 - d)
                elif piece.color == PieceColor.BLACK and y <= 4:
                    d = abs(y - gy_red)
                    score -= WEIGHTS["soldier_adv"] * max(0, 5 - d)

            if isinstance(piece, (Chariot, Canon, Horse)):
                if piece.color == PieceColor.RED and y >= 5:
                    score += WEIGHTS["cross_half_major"] * (y - 4)
                elif piece.color == PieceColor.BLACK and y <= 4:
                    score -= WEIGHTS["cross_half_major"] * (5 - y)

                if piece.color == PieceColor.RED:
                    dist_g = np.hypot(x - gx_black, y - gy_black)
                    score += WEIGHTS["general_pressure"] / (1 + dist_g)
                else:
                    dist_g = np.hypot(x - gx_red, y - gy_red)
                    score -= WEIGHTS["general_pressure"] / (1 + dist_g)

    score -= WEIGHTS["king_threat"] * red_threats
    score += WEIGHTS["king_threat"] * black_threats

    return score
