from chinese_chess.board import Board
from chinese_chess.pieces.base import PieceColor, Piece
from agents import agent_minimax, agent_alphabeta, agent_reflex, agent_basic_alphabeta
import time

def place_piece(board: Board, piece, position):
    pass

def single_player_mode(board: Board):
    isRedTurn = True
    print("Single player mode: You are playing against AI.")
    while True:
        # Select the type of agent.
        agent = input("Select the type of agent2/black (minimax, alphabeta, basic_alphabeta, reflex): ").lower()
        if agent == "exit":
            return
        if agent not in ['minimax', 'alphabeta', 'basic_alphabeta', 'reflex']:
            print("Invalid agent name.")
            continue
        if agent == 'minimax':
            agent = agent_minimax
            print("Minimax Mode")
        elif agent == 'alphabeta':
            agent = agent_alphabeta
            print("Alphabeta Mode")
        elif agent == 'basic_alphabeta':
            agent = agent_basic_alphabeta
            print("Basic Alphabeta Mode")
        else:
            agent = agent_reflex
            print("Reflex Mode")
        break
    
    while True:
        if isRedTurn:
            # AI's turn (red side)
            start_ts = time.time()
            print("It's AI's turn.")
            
            # 讓 agent 決定走哪一手
            old_pos, new_pos = agent(board, PieceColor.RED)
            start = chr(old_pos[0] + ord('a')) + str(old_pos[1] + 1)
            end = chr(new_pos[0] + ord('a')) + str(new_pos[1] + 1)
            print(f"AI move: {start} -> {end}")
            
            # 直接呼叫 make_move
            board.make_move(old_pos, new_pos)
            captured = board.history[-1]['captured']
            if captured is not None:
                print(f"AI captured: {captured.display()}")
            
            elapsed = time.time() - start_ts
            print(f"AI took {elapsed:.2f} seconds to make a move.")
            
            # 顯示棋盤
            board.display()
            print()
            isRedTurn = not isRedTurn
            
            if board.terminate(True):
                print("Game over!")
                break

        else:
            # User's turn (black side)
            move = input("Enter your move (e.g., 'e2 e4'): ")
            if move.lower() == "exit":
                break
            if move.lower() == "valid":
                pos = input("Enter position (e.g., 'e2'): ")
                pos = board.translate_position(pos)
                piece: Piece = board.get_piece(pos)
                if piece is None:
                    print("Invalid position.")
                    continue
                for m in piece.valid_moves(board):
                    cor = chr(m[0] + ord('a')) + str(m[1] + 1)
                    print(cor, end=' ')
                print()
                continue
            
            try:
                start_str, end_str = move.split()
                old_pos = board.translate_position(start_str)
                new_pos = board.translate_position(end_str)
                
                piece: Piece = board.get_piece(old_pos)
                if piece is None:
                    raise Exception("No piece at start position.")
                
                # 確認走子顏色對不對
                if piece.color != (PieceColor.RED if isRedTurn else PieceColor.BLACK):
                    raise Exception("It's not your turn.")
                
                valid_moves = piece.valid_moves(board)
                if new_pos not in valid_moves:
                    raise Exception("Invalid move.")
                
                print(f"User move: {start_str} -> {end_str}")
                
                # 同樣用 make_move
                board.make_move(old_pos, new_pos)
                captured = board.history[-1]['captured']
                if captured is not None:
                    print(f"User captured: {captured.display()}")
                
                board.display()
                print()
                isRedTurn = not isRedTurn
                
                if board.terminate(True):
                    print("Game over!")
                    break
            
            except Exception as e:
                print(f"Invalid move: {e}")

def two_AI_mode(board: Board):
    isRedTurn = True
    print("Two AI mode: AI v.s. AI")
    
    # 選 agent1/red
    while True:
        agent1 = input("Select the type of agent2/black (minimax, alphabeta, basic_alphabeta, reflex): ").lower()
        agent1_total_moves_time = []
        if agent1 == "exit":
            return
        if agent1 not in ['minimax', 'alphabeta', 'basic_alphabeta', 'reflex']:
            print("Invalid agent name.")
            continue
        if agent1 == 'minimax':
            agent1 = agent_minimax
            print("Minimax Mode")
        elif agent1 == 'alphabeta':
            agent1 = agent_alphabeta
            print("Alphabeta Mode")
        elif agent1 == 'basic_alphabeta':
            agent1 = agent_basic_alphabeta
            print("Basic Alphabeta Mode")
        else:
            agent1 = agent_reflex
            print("Reflex Mode")
        break

    # 選 agent2/black
    while True:
        agent2 = input("Select the type of agent2/black (minimax, alphabeta, basic_alphabeta, reflex): ").lower()
        agent2_total_moves_time = []
        if agent2 == "exit":
            return
        if agent2 not in ['minimax', 'alphabeta', 'basic_alphabeta', 'reflex']:
            print("Invalid agent name.")
            continue
        if agent2 == 'minimax':
            agent2 = agent_minimax
            print("Minimax Mode")
        elif agent2 == 'alphabeta':
            agent2 = agent_alphabeta
            print("Alphabeta Mode")
        elif agent2 == 'basic_alphabeta':
            agent2 = agent_basic_alphabeta
            print("Basic Alphabeta Mode")
        else:
            agent2 = agent_reflex
            print("Reflex Mode")
        break

    while True:
        print(f"It's {'Red' if isRedTurn else 'Black'} (AI{1 if isRedTurn else 2})'s turn.")
        
        # 讓對應 agent 做決策
        start_ts = time.time()
        if isRedTurn:
            old_pos, new_pos = agent1(board, PieceColor.RED)
        else:
            old_pos, new_pos = agent2(board, PieceColor.BLACK)
        start = chr(old_pos[0] + ord('a')) + str(old_pos[1] + 1)
        end = chr(new_pos[0] + ord('a')) + str(new_pos[1] + 1)
        print(f"AI{1 if isRedTurn else 2} move: {start} -> {end}")
        
        # 用 make_move
        board.make_move(old_pos, new_pos)
        captured = board.history[-1]['captured']
        if captured is not None:
            print(f"AI{1 if isRedTurn else 2} captured: {captured.display()}")

        elapsed = time.time() - start_ts
        print(f"AI took {elapsed:.2f} seconds to make a move.")

        if isRedTurn:
            agent1_total_moves_time.append(elapsed)
        else:
            agent2_total_moves_time.append(elapsed)

        board.display()
        print()
        isRedTurn = not isRedTurn
        
        if board.terminate(True):
            print("Game over!")
            print("Agent1: ", agent1.__name__, "Total time:", sum(agent1_total_moves_time), "seconds")
            print("Agent1: ", agent1.__name__, "Average time:", sum(agent1_total_moves_time) / len(agent1_total_moves_time) if agent1_total_moves_time else 0, "seconds per move")
            print("Agent1: ", agent1.__name__, "Max cost time:", max(agent1_total_moves_time) if agent1_total_moves_time else 0, "seconds for a move")
            print("----------------------")
            print("Agent2: ", agent2.__name__, "Total time:", sum(agent2_total_moves_time), "seconds")
            print("Agent2: ", agent2.__name__, "Average time:", sum(agent2_total_moves_time) / len(agent2_total_moves_time) if agent2_total_moves_time else 0, "seconds per move")
            print("Agent2: ", agent2.__name__, "Max cost time:", max(agent2_total_moves_time) if agent2_total_moves_time else 0, "seconds for a move")
            break


def two_players_mode(board: Board):
    isRedTurn = True
    print("Two players mode: 1P v.s. 2P")
    
    while True:
        print(f"It's {'Red' if isRedTurn else 'Black'}'s turn.")
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
            print(f"User{1 if isRedTurn else 2} move: {start} -> {end}")

            # ← 這裡用 make_move 取代原本手動改 pos + place + remove
            board.make_move(old_pos, new_pos)
            captured = board.history[-1]['captured']
            if captured is not None:
                print(f"Captured: {captured.display()}")

            board.display()
            print()
            isRedTurn = not isRedTurn
            if board.terminate(True):
                print("Game over!")
                break
        except Exception as e:
            print(f"Invalid move: {e}")


if __name__ == "__main__":
    board = Board()
    board.display()

    mode = input("Enter mode (1 for player against AI, 2 for two AI, 3 for two players): ")
    if mode == "1":
        print("Single player mode selected.")
        single_player_mode(board)
    elif mode == "2":
        print("Two AIs mode selected.")
        two_AI_mode(board)
    elif mode == "3":
        print("Two players mode selected.")
        two_players_mode(board)
    else:
        print("Invalid mode selected.")