from chinese_chess.pieces.base import Piece, PieceColor

class General(Piece):
    def __init__(self, color, position):
        super().__init__("帥" if color == PieceColor.RED else "將", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)

            if not board.is_valid_position(new_pos):
                continue

            if not (3 <= new_x <= 5):
                continue

            if self.color == PieceColor.RED:
                if new_y > 2:
                    continue
            else: 
                if new_y < 7:
                    continue

            piece_at_new = board.get_piece(new_pos)
            if piece_at_new is None or piece_at_new.color != self.color:
                moves.append(new_pos)

        if self.color == PieceColor.RED:
            for scan_y in range(y + 1, 10):
                scan_pos = (x, scan_y)
                piece = board.get_piece(scan_pos)
                if piece is None:
                    continue
                if isinstance(piece, General) and piece.color != self.color:
                    moves.append(scan_pos)
                break
        else:
            for scan_y in range(y - 1, -1, -1):
                scan_pos = (x, scan_y)
                piece = board.get_piece(scan_pos)
                if piece is None:
                    continue
                if isinstance(piece, General) and piece.color != self.color:
                    moves.append(scan_pos)
                break

        return moves