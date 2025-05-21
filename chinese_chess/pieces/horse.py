from chinese_chess.pieces.base import Piece, PieceColor

## Implementation of the Horse piece
class Horse(Piece):
    def __init__(self, color, position):
        super().__init__("傌" if color == PieceColor.RED else "馬", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [
            ((1, 2), (0, 1)),
            ((-1, 2), (0, 1)),
            ((1, -2), (0, -1)),
            ((-1, -2), (0, -1)),
            ((2, 1), (1, -1)),
            ((2, -1), (1, 1)),
            ((-2, 1), (-1, 0)),
            ((-2, -1), (-1, 0))
        ]

        # Check the 8 possible moves for the horse
        for (dx, dy), (block_dx, block_dy) in directions:
            block = (x + block_dx, y + block_dy)
            if (board.is_empty(block)):
                new_pos = (x + dx, y + dy)
                if board.is_valid_position(new_pos):
                    piece_at_new_pos = board.get_piece(new_pos)
                    if piece_at_new_pos is None or piece_at_new_pos.color != self.color:
                        moves.append(new_pos)
        
        return moves