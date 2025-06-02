from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from chinese_chess.pieces.general import General
import numpy as np
import random

def minimax(board: Board, depth, maximizingPlayer):
    # Reach the target depth or terminate state: return current heuristic value.
    if depth == 0 or board.terminate():
        return get_heuristic(board), None
    
    # Agent's turn: maximize the profit.
    if maximizingPlayer:
        cur_max = -np.inf
        cur_best_move = set()
        
        # Go through all possible pieces.
        for x in range(10):
            for y in range(9):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.RED:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    # Go down the tree.
                    piece.position = new_pos
                    ori_piece = board.place_piece(piece)
                    score, _ = minimax(board, depth - 1, False)
                    
                    # Update the result.
                    if score > cur_max:
                        cur_max = score
                        cur_best_move = {(old_pos, new_pos)}
                    elif score == cur_max:
                        cur_best_move.add((old_pos, new_pos))

                    # Resume the original board.
                    piece.position = old_pos
                    ori_piece.position = new_pos
                    board.place_piece(piece)
                    board.place_piece(ori_piece)

        return cur_max, cur_best_move
    
    # Opponent's turn: minimize the profit.
    else:
        cur_min = np.inf
        cur_worst_move = set()
        
        # Go through all possible pieces.
        for x in range(10):
            for y in range(9):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.BLACK:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    # Go down the tree.
                    piece.position = new_pos
                    ori_piece = board.place_piece(piece)
                    score, _ = minimax(board, depth - 1, True)
                    
                    # Update the result.
                    if score < cur_min:
                        cur_min = score
                        cur_worst_move = {(old_pos, new_pos)}
                    elif score == cur_min:
                        cur_worst_move.add((old_pos, new_pos))

                    # Resume the original board.
                    piece.position = old_pos
                    ori_piece.position = new_pos
                    board.place_piece(piece)
                    board.place_piece(ori_piece)

        return cur_min, cur_worst_move


def alphabeta(board, depth, maximizingPlayer, alpha, beta):
    # Reach the target depth or terminate state: return current heuristic value.
    if depth == 0 or board.terminate():
        return get_heuristic(board), None
    
    # Agent's turn: maximize the profit.
    if maximizingPlayer:
        cur_max = -np.inf
        cur_best_move = set()
        
        # Go through all possible pieces.
        for x in range(10):
            for y in range(9):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.RED:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    piece.position = new_pos
                    ori_piece = board.place_piece(piece)
                    score, _ = alphabeta(board, depth - 1, False, alpha, beta)

                    # Update the result.
                    if score > cur_max:
                        cur_max = score
                        cur_best_move = {(old_pos, new_pos)}
                    elif score == cur_max:
                        cur_best_move.add((old_pos, new_pos))

                    # Prune the branch.
                    alpha = max(alpha, cur_max)
                    if beta <= alpha:
                        return cur_max, cur_best_move

                    # Resume the original board.
                    piece.position = old_pos
                    ori_piece.position = new_pos
                    board.place_piece(piece)
                    board.place_piece(ori_piece)
        return cur_max, cur_best_move
    
    # Opponent's turn: minimize the profit.
    else:
        cur_min = np.inf
        cur_worst_move = set()
        
        # Go through all possible pieces.
        for x in range(10):
            for y in range(9):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.BLACK:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    # Go down the tree.
                    piece.position = new_pos
                    ori_piece = board.place_piece(piece)
                    score, _ = alphabeta(board, depth - 1, True, alpha, beta)
                    
                    # Update the result.
                    if score < cur_min:
                        cur_min = score
                        cur_worst_move = {(old_pos, new_pos)}
                    elif score == cur_min:
                        cur_worst_move.add((old_pos, new_pos))

                    # Prune the branch.
                    beta = min(beta, cur_min)
                    if beta <= alpha:
                        return cur_min, cur_best_move 

                    # Resume the original board.                  
                    piece.position = old_pos
                    ori_piece.position = new_pos
                    board.place_piece(piece)
                    board.place_piece(ori_piece)
        return cur_min, cur_worst_move


def agent_minimax(board):
    return random.choice(list(minimax(board, 1, True)[1]))


def agent_alphabeta(board):
    return random.choice(list(alphabeta(board, 1, True, -np.inf, np.inf)[1]))


def agent_reflex(board):
    for x in range(10):
        for y in range(9):
            old_pos = (x, y)
            piece: Piece = board.get_piece(old_pos)
            if piece == None:
                continue
            moves = piece.valid_moves(board)
            if len(moves) != 0:
                return (x, y), random.choice(moves)

def get_heuristic(board):
    red_general = None
    black_general = None
    for x in range(10):
        for y in range(9):
            piece = board.grid[y][x]
            if isinstance(piece, General) and piece.color == PieceColor.RED:
                red_general = (x, y)
                break
            if isinstance(piece, General) and piece.color == PieceColor.BLACK:
                black_general = (x, y)
                break
    if red_general is None:
        return -np.inf
    elif black_general is None:
        return np.inf
    
    score = 0
    
    return score