from chinese_chess.pieces.base import Piece, PieceColor

class General(Piece):
    def __init__(self, color, position):
        super().__init__("帥" if color == PieceColor.RED else "將", color, position)
    
    def valid_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if board.is_valid_position(new_pos):
                piece_at_new_pos = board.get_piece(new_pos)
                if piece_at_new_pos is None or piece_at_new_pos.color != self.color:
                    if self.color == PieceColor.RED and new_pos[1] <= 2:
                        moves.append(new_pos)
                    elif self.color == PieceColor.BLACK and new_pos[1] >= 7:
                        moves.append(new_pos)
        
        if self.color == PieceColor.RED:
            for ny in range(y + 1, 10):
                new_pos = (x, ny)
                piece = board.get_piece(new_pos)
                if piece != None:
                    if isinstance(piece, General):
                        moves.append(new_pos)
                    else:
                        break
        else:
            for ny in range(y - 1, -1, -1):
                new_pos = (x, ny)
                piece = board.get_piece(new_pos)
                if piece != None:
                    if isinstance(piece, General):
                        moves.append(new_pos)
                    else:
                        break
                    
        return moves