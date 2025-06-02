from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from chinese_chess.pieces.advisor import Advisor
from chinese_chess.pieces.chariot import Chariot
from chinese_chess.pieces.canon import Canon
from chinese_chess.pieces.elephant import Elephant
from chinese_chess.pieces.general import General
from chinese_chess.pieces.horse import Horse
from chinese_chess.pieces.soldier import Soldier
import copy
import numpy as np
import random

def minimax(board: Board, depth, maximizingPlayer):
    # Reach the target depth or terminate state: return current heuristic value.
    if depth == 0 or board.terminate():
        return get_heuristic(board, maximizingPlayer), None
    
    # Agent's turn: maximize the profit.
    if maximizingPlayer:
        cur_max = -np.inf
        cur_best_move = set()
        
        # Go through all possible pieces.
        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.RED:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                cur_board = copy.deepcopy(board)
                for new_pos in moves:
                    # Go down the tree.
                    piece.position = new_pos
                    ori_piece = cur_board.place_piece(piece)
                    score, _ = minimax(cur_board, depth - 1, False)
                    
                    # Update the result.
                    if score > cur_max:
                        cur_max = score
                        cur_best_move = {(old_pos, new_pos)}
                    elif score == cur_max:
                        cur_best_move.add((old_pos, new_pos))

        return cur_max, cur_best_move
    
    # Opponent's turn: minimize the profit.
    else:
        cur_min = np.inf
        cur_worst_move = set()
        
        # Go through all possible pieces.
        for x in range(9):
            for y in range(10):
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
                    board.place_piece(piece)
                    if ori_piece != None:
                        ori_piece.position = new_pos
                        board.place_piece(ori_piece)

        return cur_min, cur_worst_move


def alphabeta(board, depth, maximizingPlayer, alpha, beta):
    # Reach the target depth or terminate state: return current heuristic value.
    if depth == 0 or board.terminate():
        return get_heuristic(board, maximizingPlayer), None
    
    # Agent's turn: maximize the profit.
    if maximizingPlayer:
        cur_max = -np.inf
        cur_best_move = set()
        
        # Go through all possible pieces.
        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.RED:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                cur_board = copy.deepcopy(board)
                for new_pos in moves:
                    piece.position = new_pos
                    ori_piece = cur_board.place_piece(piece)
                    score, _ = alphabeta(cur_board, depth - 1, False, alpha, beta)

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
                    board.place_piece(piece)
                    if ori_piece != None:
                        ori_piece.position = new_pos
                        board.place_piece(ori_piece)
        return cur_max, cur_best_move
    
    # Opponent's turn: minimize the profit.
    else:
        cur_min = np.inf
        cur_worst_move = set()
        
        # Go through all possible pieces.
        for x in range(9):
            for y in range(10):
                old_pos = (x, y)
                if board.is_empty(old_pos):
                    continue
                piece: Piece = board.get_piece(old_pos)
                if piece.color != PieceColor.BLACK:
                    continue
                
                # Go through all available moves.
                moves = piece.valid_moves(board)
                cur_board = copy.deepcopy(board)
                for new_pos in moves:
                    # Go down the tree.
                    piece.position = new_pos
                    ori_piece = cur_board.place_piece(piece)
                    score, _ = alphabeta(cur_board, depth - 1, True, alpha, beta)
                    
                    # Update the result.
                    if score < cur_min:
                        cur_min = score
                        cur_worst_move = {(old_pos, new_pos)}
                    elif score == cur_min:
                        cur_worst_move.add((old_pos, new_pos))
                    
                    # Prune the branch.
                    beta = min(beta, cur_min)
                    if beta <= alpha:
                        return cur_min, cur_worst_move
        return cur_min, cur_worst_move


def agent_minimax(board):
    # Randomly choose one available move.
    # Assume depth = 5.
    return random.choice(list(minimax(board, 5, True)[1]))


def agent_alphabeta(board):
    # Randomly choose one available move.
    # Assume depth = 5.
    return random.choice(list(alphabeta(board, 5, True, -np.inf, np.inf)[1]))


def agent_reflex(board):
    # Find the first unempty grid and randomly return an available move.
    for x in range(9):
        for y in range(10):
            old_pos = (x, y)
            piece: Piece = board.get_piece(old_pos)
            if piece == None:
                continue
            moves = piece.valid_moves(board)
            if len(moves) != 0:
                return (x, y), random.choice(moves)

def get_heuristic(board, maximizingPlayer):
    red_general = None
    black_general = None
    
    # 將死
    for x in range(9):
        for y in range(10):
            piece = board.grid[y][x]
            if isinstance(piece, General) and piece.color == PieceColor.RED:
                red_general = (x, y)
                break
            if isinstance(piece, General) and piece.color == PieceColor.BLACK:
                black_general = (x, y)
                break
    
    if red_general is None:
        # Agent fails.
        return -np.inf
    elif black_general is None:
        # Agent wins.
        return np.inf
    score = 0
    for x in range(9):
        for y in range(10):
            pos = (x, y)
            if board.is_empty(pos):
                continue
            piece: Piece = board.get_piece(pos)
            if piece.color == PieceColor.RED:
                if isinstance(piece, Chariot) or isinstance(piece, Canon):
                    w = ((x - 4) ** 2 + (y - 1) ** 2) ** 0.5
                elif isinstance(piece, Horse):
                    w = abs(x - 4)
                else:
                    w = 1
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    if not board.is_empty(new_pos):
                        new_piece = board.get_piece(new_pos)
                        if new_piece.color != PieceColor.BLACK:
                            continue
                        if isinstance(new_piece, General): # 將
                            if maximizingPlayer: # Agent's turn
                                score += 1e9 * w
                            else:
                                score += 1e7 * w
                        elif isinstance(new_piece, Advisor): # 士
                            score += 5e5 * w
                        elif isinstance(new_piece, Chariot): # 車
                            score += 2e5 * w
                        elif isinstance(new_piece, Canon): # 砲
                            score += 1e5 * w
                        elif isinstance(new_piece, Horse): # 馬
                            score += 5e4 * w
                        elif isinstance(new_piece, Elephant): # 象
                            if 2 <= x <= 6:
                                score += 2e4 * w
                            else:
                                score += 1e4 * w
                        else: # 卒
                            # The black soldier has entered red block.
                            if 0 <= new_pos[1] <= 4:
                                center_dis = ((new_pos[0] - 4) ** 2 + (new_pos[1] - 1) ** 2) ** 0.5
                                score += 1e5 * center_dis * w
                            else:
                                score += 1e3 * w
            else:
                moves = piece.valid_moves(board)
                for new_pos in moves:
                    if not board.is_empty(new_pos):
                        new_piece = board.get_piece(new_pos)
                        if new_piece.color != PieceColor.RED:
                            continue
                        if isinstance(new_piece, General): # 帥
                            if not maximizingPlayer:
                                score += -1e10
                            else:
                                score += -1e7
                        elif isinstance(new_piece, Advisor): # 仕
                            score += -1e6                      
                        elif isinstance(new_piece, Chariot): # 俥
                            score += -2e5
                        elif isinstance(new_piece, Canon): # 炮
                            score += -1e5
                        elif isinstance(new_piece, Horse): # 傌
                            score += -5e4
                        elif isinstance(new_piece, Elephant): # 相
                            if 2 <= x <= 6:
                                score += -2e4
                            else:
                                score += -1e4
                        else: # 兵
                            # The black soldier has entered red block.
                            if 0 <= y <= 4:
                                center_dis = ((x - 4) ** 2 + (y - 1) ** 2) ** 0.5
                                score += -1e6 * center_dis
                            else:
                                score += -1e3
     
    return score