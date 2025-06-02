from chinese_chess.pieces.base import Piece, PieceColor

class Chariot(Piece):
    def __init__(self, color, position):
        super().__init__("俥" if color == PieceColor.RED else "車", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            for step in range(1, 10):
                new_x = x + dx * step
                new_y = y + dy * step
                new_pos = (new_x, new_y)

                if not board.is_valid_position(new_pos):
                    break

                piece_at_new = board.get_piece(new_pos)

                if piece_at_new is None:
                    moves.append(new_pos)
                else:
                    if piece_at_new.color != self.color:
                        moves.append(new_pos)
                    break

        return moves