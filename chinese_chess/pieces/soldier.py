from chinese_chess.pieces.base import Piece, PieceColor

class Soldier(Piece):
    def __init__(self, color, position):
        super().__init__("兵" if color == PieceColor.RED else "卒", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position

        if self.color == PieceColor.RED:
            forward = (x, y + 1)
            if board.is_valid_position(forward):
                target = board.get_piece(forward)
                if target is None or target.color != self.color:
                    moves.append(forward)

            if y >= 5:
                left = (x - 1, y)
                if board.is_valid_position(left):
                    target = board.get_piece(left)
                    if target is None or target.color != self.color:
                        moves.append(left)
                right = (x + 1, y)
                if board.is_valid_position(right):
                    target = board.get_piece(right)
                    if target is None or target.color != self.color:
                        moves.append(right)

        else:
            forward = (x, y - 1)
            if board.is_valid_position(forward):
                target = board.get_piece(forward)
                if target is None or target.color != self.color:
                    moves.append(forward)

            if y <= 4:
                left = (x - 1, y)
                if board.is_valid_position(left):
                    target = board.get_piece(left)
                    if target is None or target.color != self.color:
                        moves.append(left)

                right = (x + 1, y)
                if board.is_valid_position(right):
                    target = board.get_piece(right)
                    if target is None or target.color != self.color:
                        moves.append(right)

        return moves