from chinese_chess.pieces.base import Piece, PieceColor

class Advisor(Piece):
    def __init__(self, color, position):
        super().__init__("仕" if color == PieceColor.RED else "士", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)
            
            if not board.is_valid_position(new_pos):
                continue
            
            piece_at_new = board.get_piece(new_pos)
            if piece_at_new is not None and piece_at_new.color == self.color:
                continue

            if self.color == PieceColor.RED:
                if 3 <= new_x <= 5 and 0 <= new_y <= 2:
                    moves.append(new_pos)
            else:
                if 3 <= new_x <= 5 and 7 <= new_y <= 9:
                    moves.append(new_pos)

        return moves