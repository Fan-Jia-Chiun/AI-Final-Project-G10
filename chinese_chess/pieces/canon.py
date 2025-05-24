from chinese_chess.pieces.base import Piece, PieceColor

class Canon(Piece):
    def __init__(self, color, position):
        super().__init__("炮" if color == PieceColor.RED else "砲", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            is_piece_bettween = False
            for step in range(1, 10):
                new_pos = (x + dx * step, y + dy * step)
                if not board.is_valid_position(new_pos):
                    break
                piece_at_new_pos = board.get_piece(new_pos)
                if piece_at_new_pos is None and not is_piece_bettween:
                    moves.append(new_pos)
                elif is_piece_bettween:
                    if piece_at_new_pos is not None and piece_at_new_pos.color != self.color:
                        moves.append(new_pos)
                    break
        
        return [m for m in moves if board.is_valid_position(m)]