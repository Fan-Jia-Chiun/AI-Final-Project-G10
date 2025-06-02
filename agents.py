from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from chinese_chess.pieces.advisor import Advisor
from chinese_chess.pieces.chariot import Chariot
from chinese_chess.pieces.canon import Canon
from chinese_chess.pieces.elephant import Elephant
from chinese_chess.pieces.general import General
from chinese_chess.pieces.horse import Horse
from chinese_chess.pieces.soldier import Soldier
import numpy as np
import random

def minimax(board: Board, depth: int, maximizingPlayer: bool, color: PieceColor):
    if depth == 0 or board.terminate():
        return get_heuristic(board, maximizingPlayer), None

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

                moves = piece.valid_moves(board)

                for new_pos in moves:
                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != color:
                        return np.inf, {(old_pos, new_pos)}

                for new_pos in moves:
                    board.make_move(old_pos, new_pos)
                    val, _ = minimax(board, depth - 1, False, color)
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

                moves = piece.valid_moves(board)

                for new_pos in moves:
                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != opp_color:
                        return -np.inf, {(old_pos, new_pos)}

                for new_pos in moves:
                    board.make_move(old_pos, new_pos)
                    val, _ = minimax(board, depth - 1, True, color)
                    board.undo_move()

                    if val < worst_value:
                        worst_value = val
                        worst_moves = {(old_pos, new_pos)}
                    elif val == worst_value:
                        worst_moves.add((old_pos, new_pos))

        return worst_value, worst_moves




def alphabeta(board: Board, depth: int, maximizingPlayer: bool,
              alpha: float, beta: float, color: PieceColor):
    if depth == 0 or board.terminate():
        return get_heuristic(board, maximizingPlayer), None

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

                moves = piece.valid_moves(board)

                for new_pos in moves:
                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != color:
                        return np.inf, {(old_pos, new_pos)}

                for new_pos in moves:
                    board.make_move(old_pos, new_pos)
                    val, _ = alphabeta(board, depth - 1, False, alpha, beta, color)
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

                moves = piece.valid_moves(board)

                for new_pos in moves:
                    target = board.get_piece(new_pos)
                    if isinstance(target, General) and target.color != opp_color:
                        return -np.inf, {(old_pos, new_pos)}

                for new_pos in moves:
                    board.make_move(old_pos, new_pos)
                    val, _ = alphabeta(board, depth - 1, True, alpha, beta, color)
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
    # Randomly choose one available move.
    # Assume depth = 5.
    return random.choice(list(minimax(board, 3, True, color)[1]))


def agent_alphabeta(board, color: PieceColor):
    # Randomly choose one available move.
    # Assume depth = 5.
    return random.choice(list(alphabeta(board, 4, True, -np.inf, np.inf, color)[1]))


def agent_reflex(board, color: PieceColor):
    # Find the first unempty grid and randomly return an available move.
    candidates = []
    for x in range(9):
        for y in range(10):
            pos = (x, y)
            piece = board.get_piece(pos)
            if piece is None or piece.color != color:
                continue
            moves = piece.valid_moves(board)
            for new_pos in moves:
                candidates.append((pos, new_pos))
    if candidates:
        return random.choice(candidates)
    return None


def get_heuristic(board, maximizingPlayer):
    red_general = None
    black_general = None
    for x in range(9):
        for y in range(10):
            piece = board.grid[y][x]
            if isinstance(piece, General):
                if piece.color == PieceColor.RED:
                    red_general = (x, y)
                else:
                    black_general = (x, y)

    if red_general is None:
        return -np.inf
    if black_general is None:
        return np.inf 

    score = 0.0

    material_value = {
        Chariot: 9.0,
        Canon:   8.0,
        Horse:   5.0,
        Elephant:3.0,
        Advisor: 3.0,
        Soldier: 1.0,
        General: 0.0
    }

    red_threats = 0
    black_threats = 0

    for x in range(9):
        for y in range(10):
            piece = board.get_piece((x, y))
            if piece is None:
                continue

            base_val = material_value.get(type(piece), 0.0)
            if piece.color == PieceColor.RED:
                score += base_val
            else:
                score -= base_val

            moves = piece.valid_moves(board)
            mobility_score = 0.1 * len(moves)
            if piece.color == PieceColor.RED:
                score += mobility_score
            else:
                score -= mobility_score

            cx, cy = 4, 4
            dist_center = np.hypot(x - cx, y - cy)
            pos_weight = 0.05 * (5 - dist_center) 
            if pos_weight < 0:
                pos_weight = 0
            if piece.color == PieceColor.RED:
                score += pos_weight
            else:
                score -= pos_weight

            if piece.color == PieceColor.RED:
                if black_general in moves:
                    red_threats += 1
            else:
                if red_general in moves:
                    black_threats += 1

            if isinstance(piece, Soldier):
                sx, sy = piece.position
                if piece.color == PieceColor.RED:
                    if sy >= 5:
                        dist_to_black_general = abs(sy - black_general[1])
                        adv_bonus = 0.2 * (5 - dist_to_black_general)
                        if adv_bonus < 0:
                            adv_bonus = 0
                        score += adv_bonus
                else:
                    if sy <= 4:
                        dist_to_red_general = abs(sy - red_general[1])
                        adv_bonus = 0.2 * (5 - dist_to_red_general)
                        if adv_bonus < 0:
                            adv_bonus = 0
                        score -= adv_bonus

    score -= 0.5 * red_threats
    score += 0.5 * black_threats

    return score