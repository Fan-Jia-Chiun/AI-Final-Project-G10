from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from agents import agent_minimax, agent_alphabeta, agent_reflex

def place_piece(board: Board, piece, position):
    pass

def single_player_mode(board: Board):
    isRedTurn = True
    print("Single player mode: You are playing against AI.")
    while True:
        # Select the type of agent.
        agent = input("Select the type of agent (minimax, alphabeta, reflex): ").lower()
        if agent == "exit":
            return
        if agent not in ['minimax', 'alphabeta', 'reflex']:
            print("Invalid agent name.")
            continue
        if agent == 'minimax':
            agent = agent_minimax
            print("Minimax Mode")
        elif agent == 'alphabeta':
            agent = agent_alphabeta
            print("Alphabeta Mode")
        else:
            agent = agent_reflex
            print("Reflex Mode")
        break
    
    while True:
        if isRedTurn:
            # AI's turn (red side)
            print("It's AI's turn.")
            
            # Agent makes decision.
            old_pos, new_pos = agent(board)
            start = chr(old_pos[0] + ord('a')) + str(old_pos[1] + 1)
            end = chr(new_pos[0] + ord('a')) + str(new_pos[1] + 1)
            print(f"AI move: {start} -> {end}")
            
            # Move the piece
            piece: Piece = board.get_piece(old_pos)
            piece.position = new_pos
            board.place_piece(piece)
            removed_piece = board.remove_piece(old_pos)
            # if removed_piece:
            #     print(f"Removed piece: {removed_piece.display()}")
            
            # Display current situation.
            board.display()
            print()
            isRedTurn = not isRedTurn
            if board.terminate():
                print("Game over!")
                break
        else:
            # User's turn (black side)
            
            # User makes decision.
            move = input("Enter your move (e.g., 'e2 e4'): ")
            if move.lower() == "exit":
                break
            if move.lower() == "valid":
                pos = input("Enter position (e.g., 'e2'): ")
                pos = board.translate_position(pos)
                piece: Piece = board.get_piece(pos)
                if piece == None:
                    print("Invalid position.")
                    continue
                for m in piece.valid_moves(board):
                    cor = chr(m[0] + ord('a')) + str(m[1] + 1)
                    print(cor, end = ' ')
                print()
                continue
            
            try:
                # Judge whether the position is available.
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
                board.place_piece(piece)
                removed_piece = board.remove_piece(old_pos)
                if removed_piece:
                    print(f"Removed piece: {removed_piece.display()}")
    
                # Display current situation.
                board.display()
                print()
                isRedTurn = not isRedTurn
                if board.terminate():
                    print("Game over!")
                    break
            
            # Handle exception.
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
            if piece == None:
                print("Invalid position.")
                continue
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
            # if old_piece:
            #     print(f"Removed piece: {old_piece.display()}")

            board.display()
            print()
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