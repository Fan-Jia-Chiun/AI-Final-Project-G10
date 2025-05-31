from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece

def place_piece(board: Board, piece, position):
    pass

def single_player_mode(board: Board):
    isRedTurn = True
    while True:
        print("Single player mode: You are playing against AI.")
        # Implement AI logic here
        # For now, just simulate a move
        move = input("Enter your move (e.g., 'e2 e4'): ")
        if move.lower() == "exit":
            break
        try:
            start, end = move.split()
            old_pos, new_pos = board.translate_position(start, end)
            
            piece: Piece = board.get_piece(old_pos)
            print(piece)
            if piece is None:
                raise Exception("No piece at start position.")
            
            if piece.color != (PieceColor.RED if isRedTurn else PieceColor.BLACK):
                raise Exception("It's not your turn.")
            
            valid_moves = piece.valid_moves(board)
            if new_pos not in valid_moves:
                raise Exception("Invalid move.")

            # Move the piece
            piece.position = new_pos
            board.place_piece(piece)
            removed_piece = board.remove_piece(old_pos)
            if removed_piece:
                print(f"Removed piece: {removed_piece.display()}")

            board.display()
            isRedTurn = not isRedTurn
            if board.terminate():
                print("Game over!")
                break
        except Exception as e:
            print(f"Invalid move: {e}")

def two_players_mode(board: Board):
    isRedTurn = True
    while True:
        print(f'It is {"Red" if isRedTurn else "Black"}\'s turn.')
        move = input("Enter your move (e.g., 'e2 e4'): ")
        if move.lower() == "exit":
            break
        if move.lower() == "valid":
            pos = input("Enter position (e.g., 'e2'): ")
            pos = board.translate_position(pos)
            piece: Piece = board.get_piece(pos)
            print(piece.valid_moves(board))
            continue
        try:
            start, end = move.split()
            old_pos = board.translate_position(start)
            new_pos = board.translate_position(end)
            
            piece: Piece = board.get_piece(old_pos)
            if piece is None:
                raise Exception("No piece at start position.")
            
            if piece.color != (PieceColor.RED if isRedTurn else PieceColor.BLACK):
                raise Exception("It's not your turn.")
            
            valid_moves = piece.valid_moves(board)
            if new_pos not in valid_moves:
                raise Exception("Invalid move.")

            # Move the piece
            piece.position = new_pos
            old_piece = board.place_piece(piece)
            board.remove_piece(old_pos)

            if old_piece:
                print(f"Removed piece: {old_piece.display()}")

            board.display()
            isRedTurn = not isRedTurn
            if board.terminate():
                print("Game over!")
                break
        except Exception as e:
            print(f"Invalid move: {e}")

if __name__ == "__main__":
    board = Board()
    board.display()

    mode = input("Enter mode (1 for single player, 2 for two players): ")
    if mode == "1":
        print("Single player mode selected.")
        single_player_mode(board)
    elif mode == "2":
        print("Two players mode selected.")
        two_players_mode(board)
    else:
        print("Invalid mode selected.")