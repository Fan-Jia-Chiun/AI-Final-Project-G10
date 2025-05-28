from chinese_chess.pieces.advisor import Advisor
from chinese_chess.pieces.base import PieceColor
from chinese_chess.pieces.canon import Canon
from chinese_chess.pieces.chariot import Chariot
from chinese_chess.pieces.elephant import Elephant
from chinese_chess.pieces.general import General
from chinese_chess.pieces.horse import Horse
from chinese_chess.pieces.soldier import Soldier

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(10)]  # 10x9 的棋盤
        self.setup_board()
    
    def setup_board(self):
        # Intialize the board with red pieces
        self.grid[0][0] = Chariot(PieceColor.RED, (0, 0))
        self.grid[0][1] = Horse(PieceColor.RED, (1, 0))
        self.grid[0][2] = Elephant(PieceColor.RED, (2, 0))
        self.grid[0][3] = Advisor(PieceColor.RED, (3, 0))
        self.grid[0][4] = General(PieceColor.RED, (4, 0))
        self.grid[0][5] = Advisor(PieceColor.RED, (5, 0))
        self.grid[0][6] = Elephant(PieceColor.RED, (6, 0))
        self.grid[0][7] = Horse(PieceColor.RED, (7, 0))
        self.grid[0][8] = Chariot(PieceColor.RED, (8, 0))
        self.grid[2][1] = Canon(PieceColor.RED, (1, 2))
        self.grid[2][7] = Canon(PieceColor.RED, (7, 2))
        for i in range(0, 9, 2):
            self.grid[3][i] = Soldier(PieceColor.RED, (i, 3))

        # Initialize the board with black pieces
        self.grid[9][0] = Chariot(PieceColor.BLACK, (0, 9))
        self.grid[9][1] = Horse(PieceColor.BLACK, (1, 9))
        self.grid[9][2] = Elephant(PieceColor.BLACK, (2, 9))
        self.grid[9][3] = Advisor(PieceColor.BLACK, (3, 9))
        self.grid[9][4] = General(PieceColor.BLACK, (4, 9))
        self.grid[9][5] = Advisor(PieceColor.BLACK, (5, 9))
        self.grid[9][6] = Elephant(PieceColor.BLACK, (6, 9))
        self.grid[9][7] = Horse(PieceColor.BLACK, (7, 9))
        self.grid[9][8] = Chariot(PieceColor.BLACK, (8, 9))
        self.grid[7][1] = Canon(PieceColor.BLACK, (1, 7))
        self.grid[7][7] = Canon(PieceColor.BLACK, (7, 7))
        for i in range(0, 9, 2):
            self.grid[6][i] = Soldier(PieceColor.BLACK, (i, 6))
    
    def display(self):
        for row in self.grid:
            print(" ".join([piece.display() if piece is not None else "空" for piece in row]))

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < 9 and 0 <= y < 10

    def is_empty(self, position):
        x, y = position
        return self.grid[y][x] is None

    def get_piece(self, position):
        x, y = position
        return self.grid[y][x]

    def place_piece(self, piece):
        x, y = piece.position
        old_piece = self.grid[y][x]
        self.grid[y][x] = piece
        return old_piece

    def remove_piece(self, position):
        x, y = position
        piece = self.grid[y][x]
        self.grid[y][x] = None
        return piece

    def translate_position(self, position):
        x = ord(position[0]) - ord("a")
        y = int(position[1:]) - 1
        if not self.is_valid_position((x, y)):
            raise ValueError("Invalid position")
        return (x, y)
    
    def terminate(self):
        red_general = None
        black_general = None
        for row in self.grid:
            for piece in row:
                if isinstance(piece, General) and piece.color == PieceColor.RED:
                    red_general = piece
                    break
                if isinstance(piece, General) and piece.color == PieceColor.BLACK:
                    black_general = piece
                    break
        if red_general is None:
            print("Black wins!")
            return True
        elif black_general is None:
            print("Red wins!")
            return True
        
        return False