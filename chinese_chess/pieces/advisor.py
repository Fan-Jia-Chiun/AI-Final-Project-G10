from chinese_chess.pieces.base import Piece, PieceColor

class Advisor(Piece):
    def __init__(self, color, position):
        super().__init__("仕" if color == PieceColor.RED else "士", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if board.is_valid_position(new_pos):
                piece_at_new_pos = board.get_piece(new_pos)
                if piece_at_new_pos is None or piece_at_new_pos.color != self.color:
                    if self.color == PieceColor.RED and new_pos[0] <= 2 and new_pos[1] <= 2:
                        moves.append(new_pos)
                    elif self.color == PieceColor.BLACK and new_pos[0] >= 7 and new_pos[1] >= 7:
                        moves.append(new_pos)
        
        return moves