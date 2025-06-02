from chinese_chess.pieces.base import Piece, PieceColor

class Elephant(Piece):
    def __init__(self, color, position):
        super().__init__("相" if color == PieceColor.RED else "象", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(2, 2), (-2, 2), (2, -2), (-2, -2)]

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            new_pos = (new_x, new_y)

            block = (x + dx // 2, y + dy // 2)

            if not board.is_valid_position(new_pos):
                continue

            if not board.is_empty(block):
                continue

            if self.color == PieceColor.RED:
                if new_y > 4:
                    continue
            else:
                if new_y < 5:
                    continue

            piece_at_new = board.get_piece(new_pos)
            if piece_at_new is None:
                moves.append(new_pos)
            else:
                if piece_at_new.color != self.color:
                    moves.append(new_pos)

        return moves