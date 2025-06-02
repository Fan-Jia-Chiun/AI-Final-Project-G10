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
                new_pos = (x + dx * step, y + dy * step)
                if not board.is_valid_position(new_pos):
                    break
                piece_at_new_pos = board.get_piece(new_pos)
                if piece_at_new_pos is None:
                    moves.append(new_pos)
                elif piece_at_new_pos.color != self.color and piece_at_new_pos.name not in ["相", "象", "仕", "士", "帥", "將"]:
                    moves.append(new_pos)
                    break
                else:
                    break
        
        return [m for m in moves if board.is_valid_position(m)]