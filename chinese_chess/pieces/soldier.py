from chinese_chess.pieces.base import Piece, PieceColor
from chinese_chess.pieces.general import General

class Soldier(Piece):
    def __init__(self, color, position):
        super().__init__("兵" if color == PieceColor.RED else "卒", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        if self.color == "red":
            if y < 5 and (board.is_empty((x, y + 1)) or (type(board.get_piece((x, y + 1))) == General)):
                moves.append((x, y + 1))
            else:
                if x > 0 and (board.is_empty((x - 1, y)) or (type(board.get_piece((x - 1, y))) == General)):
                    moves.append((x - 1, y))
                if x < 9 and (board.is_empty((x + 1, y)) or (type(board.get_piece((x + 1, y))) == General)):
                    moves.append((x + 1, y))
                if y < 9 and (board.is_empty((x, y + 1)) or (type(board.get_piece((x, y + 1))) == General)):
                    moves.append((x, y + 1))
        else:
            if y > 4 and (board.is_empty((x, y - 1)) or (type(board.get_piece((x, y - 1))) == General)):
                moves.append((x, y - 1))
            else:
                if x > 0 and (board.is_empty((x - 1, y)) or (type(board.get_piece((x - 1, y))) == General)):
                    moves.append((x - 1, y))
                if x < 9 and (board.is_empty((x + 1, y)) or (type(board.get_piece((x + 1, y))) == General)):
                    moves.append((x + 1, y))
                if y > 0 and (board.is_empty((x, y - 1)) or (type(board.get_piece((x, y - 1))) == General)):
                    moves.append((x, y - 1))

        return [move for move in moves if board.is_valid_position(move)]