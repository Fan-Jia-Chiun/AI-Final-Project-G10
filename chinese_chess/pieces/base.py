from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chinese_chess.board import Board

## Enum for piece colors
class PieceColor:
    RED = "red"
    BLACK = "black"


## Base class for all pieces
class Piece:
    def __init__(self, name: str, color: PieceColor, position: tuple[int, int]):
        self.name = name
        self.color = color
        self.position = position
    
    def valid_moves(self, board: "Board"):
        raise NotImplementedError("Need to be implement")
    
    def display(self):
        color_code = "\033[31m" if self.color == PieceColor.RED else "\033[36m"
        return f"{color_code}{self.name}\033[0m"