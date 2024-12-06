import copy
import math

class MancalaBoard:
    def __init__(self):
        # Initialize the board with 4 seeds in each pit
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,  # Player 1 pits
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,  # Player 2 pits
            1: 0,  # Player 1's store (rightmost pit for Player 1)
            2: 0   # Player 2's store (rightmost pit for Player 2)
        }
        
        # Player 1's pits
        self.player1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # Player 2's pits
        self.player2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
        
        # Opposite pits mapping
        self.opposite_pits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        # Next pit in sequence (counterclockwise)
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 1,
            1: 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L',
            'L': 2, 2: 'A'
        }
    
    def possibleMoves(self, player):
        """
        Returns possible moves for a given player
        """
        if player == 'player1':
            return [pit for pit in self.player1_pits if self.board[pit] > 0]
        else:
            return [pit for pit in self.player2_pits if self.board[pit] > 0]
    
    def doMove(self, player, pit):
        """
        Execute a move for a given player from a specific pit
        Returns True if the player gets an extra turn, False otherwise
        """
        # Collect seeds from the chosen pit
        seeds = self.board[pit]
        self.board[pit] = 0
        
        # Determine the current pit and player's store
        current_pit = self.next_pit[pit]
        player_store = 1 if player == 'player1' else 2
        
        # Sow the seeds
        while seeds > 0:
            # Skip opponent's store
            if current_pit == (2 if player == 'player1' else 1):
                current_pit = self.next_pit[current_pit]
                continue
            
            # Drop a seed
            self.board[current_pit] += 1
            seeds -= 1
            
            # Move to next pit
            current_pit = self.next_pit[current_pit]
        
        # Check for capture
        last_pit = self.next_pit[current_pit]
        if last_pit in (self.player1_pits if player == 'player1' else self.player2_pits) and \
           self.board[last_pit] == 1:
            opposite_pit = self.opposite_pits[last_pit]
            if self.board[opposite_pit] > 0:
                # Capture the seeds
                captured = self.board[last_pit] + self.board[opposite_pit]
                self.board[player_store] += captured
                self.board[last_pit] = 0
                self.board[opposite_pit] = 0
        
        # Return True if last seed lands in player's store (extra turn)
        return current_pit == player_store

class Game:
    def __init__(self):
        self.state = MancalaBoard()
        self.playerSide = {
            'MAX': 'player1',
            'MIN': 'player2'
        }
    
    def gameOver(self):
        """
        Check if the game is over
        """
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player1_pits)
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player2_pits)
        
        if player1_empty or player2_empty:
            # Collect remaining seeds
            if player1_empty:
                for pit in self.state.player2_pits:
                    self.state.board[2] += self.state.board[pit]
                    self.state.board[pit] = 0
            else:
                for pit in self.state.player1_pits:
                    self.state.board[1] += self.state.board[pit]
                    self.state.board[pit] = 0
            
            return True
        return False
    
    def findWinner(self):
        """
        Determine the winner and their score
        """
        player1_score = self.state.board[1]
        player2_score = self.state.board[2]
        
        if player1_score > player2_score:
            return 'player1', player1_score
        elif player2_score > player1_score:
            return 'player2', player2_score
        else:
            return 'Tie', player1_score
    
    def evaluate(self):
        """
        Evaluate the current game state
        """
        return self.state.board[1] - self.state.board[2]

class Play:
    def __init__(self):
        self.game = Game()
    
    def humanTurn(self):
        """
        Allow human to make a move
        """
        while True:
            print("\nYour current board:")
            self.displayBoard()
            
            # Show possible moves
            possible_moves = self.game.state.possibleMoves('player2')
            print("Possible moves:", possible_moves)
            
            move = input("Enter your move (choose a pit from " + str(possible_moves) + "): ").upper()
            
            if move in possible_moves:
                # Perform the move
                extra_turn = self.game.state.doMove('player2', move)
                
                # Check if game is over
                if self.game.gameOver():
                    self.endGame()
                    return
                
                # If no extra turn, computer plays
                if not extra_turn:
                    return
            else:
                print("Invalid move. Try again.")
    
    def computerTurn(self):
        """
        Computer makes a move using Minimax Alpha-Beta Pruning
        """
        depth = 4  # Adjust search depth as needed
        _, best_move = self.minimaxAlphaBetaPruning(self.game, 'MAX', depth, -math.inf, math.inf)
        
        print(f"\nComputer chooses pit {best_move}")
        extra_turn = self.game.state.doMove('player1', best_move)
        
        # Check if game is over
        if self.game.gameOver():
            self.endGame()
            return
        
        # If no extra turn, human plays
        if not extra_turn:
            return
    
    def minimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        """
        Minimax algorithm with Alpha-Beta Pruning
        """
        if game.gameOver() or depth == 0:
            return game.evaluate(), None
        
        if player == 'MAX':
            best_value = -math.inf
            best_pit = None
            
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.playerSide[player], pit)
                
                value, _ = self.minimaxAlphaBetaPruning(child_game, 'MIN', depth - 1, alpha, beta)
                
                if value > best_value:
                    best_value = value
                    best_pit = pit
                
                alpha = max(alpha, best_value)
                
                if beta <= alpha:
                    break
            
            return best_value, best_pit
        
        else:  # 'MIN'
            best_value = math.inf
            best_pit = None
            
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                child_game.state.doMove(game.playerSide[player], pit)
                
                value, _ = self.minimaxAlphaBetaPruning(child_game, 'MAX', depth - 1, alpha, beta)
                
                if value < best_value:
                    best_value = value
                    best_pit = pit
                
                beta = min(beta, best_value)
                
                if beta <= alpha:
                    break
            
            return best_value, best_pit
    
    def displayBoard(self):
        """
        Display the current state of the Mancala board
        """
        print("Computer's side:")
        print("   L  K  J  I  H  G")
        print("  ", end="")
        for pit in ['L', 'K', 'J', 'I', 'H', 'G']:
            print(f"{self.game.state.board[pit]:2d} ", end="")
        print(f"\n{self.game.state.board[2]:2d}                  {self.game.state.board[1]:2d}")
        print("   A  B  C  D  E  F")
        print("  ", end="")
        for pit in ['A', 'B', 'C', 'D', 'E', 'F']:
            print(f"{self.game.state.board[pit]:2d} ", end="")
        print("\nYour side")
    
    def endGame(self):
        """
        End the game and display the winner
        """
        winner, score = self.game.findWinner()
        print("\nGame Over!")
        self.displayBoard()
        
        if winner == 'Tie':
            print("It's a tie!")
        else:
            print(f"Winner: {winner} with {score} seeds!")
    
    def play(self):
        """
        Main game loop
        """
        print("Welcome to Mancala!")
        print("You are player 2 (bottom side). The computer is player 1 (top side).")
        
        current_player = 'computer'
        
        while not self.game.gameOver():
            if current_player == 'computer':
                print("\nComputer's turn:")
                self.computerTurn()
                current_player = 'human'
            else:
                print("\nYour turn:")
                self.humanTurn()
                current_player = 'computer'

# Start the game
if __name__ == "__main__":
    game = Play()
    game.play()