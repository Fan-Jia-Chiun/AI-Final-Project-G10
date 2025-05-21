from chinese_chess.pieces.base import Piece, PieceColor

class Soldier(Piece):
    def __init__(self, color, position):
        super().__init__("兵" if color == PieceColor.RED else "卒", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        if self.color == "red":
            if y < 5:
                moves.append((x, y + 1))
            else:
                moves.append((x + 1, y))
                moves.append((x - 1, y))
                if x == 0:
                    moves.append((x + 1, y + 1))
                elif x == 8:
                    moves.append((x - 1, y + 1))
        else:
            if y > 4:
                moves.append((x, y - 1))
            else:
                moves.append((x + 1, y))
                moves.append((x - 1, y))
                if x == 0:
                    moves.append((x + 1, y - 1))
                elif x == 8:
                    moves.append((x - 1, y - 1))

        return [move for move in moves if board.is_valid_position(move)]