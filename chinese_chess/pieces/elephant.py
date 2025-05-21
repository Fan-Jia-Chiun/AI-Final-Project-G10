from chinese_chess.pieces.base import Piece, PieceColor

class Elephant(Piece):
    def __init__(self, color, position):
        super().__init__("相" if color == PieceColor.RED else "象", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(2, 2), (-2, 2), (2, -2), (-2, -2)]

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            block = (x + dx // 2, y + dy // 2)
            if board.is_valid_position(new_pos) and board.is_empty(block):
                piece_at_new_pos = board.get_piece(new_pos)
                if piece_at_new_pos is None or piece_at_new_pos.color != self.color:
                    moves.append(new_pos)
        
        return moves