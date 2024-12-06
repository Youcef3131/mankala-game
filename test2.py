import copy
import math


class MancalaBoard:
    def __init__(self):
        # Initialiser les fosses et les magasins
        self.board = {chr(i): 4 for i in range(65, 77)}  # Pits A-L avec 4 graines chacune
        self.board["P1"] = 0  # Magasin du joueur 1
        self.board["P2"] = 0  # Magasin du joueur 2

        # Définir les fosses par joueur
        self.player1_pits = tuple(chr(i) for i in range(65, 71))  # A-F
        self.player2_pits = tuple(chr(i) for i in range(71, 77))  # G-L

        # Opposé et suivant
        self.opposite_pits = {chr(i): chr(76 - (i - 65)) for i in range(65, 77)}  # Opposés
        self.next_pits = {
            "A": "B", "B": "C", "C": "D", "D": "E", "E": "F", "F": "P1",
            "G": "H", "H": "I", "I": "J", "J": "K", "K": "L", "L": "P2",
            "P1": "G",  # Après le magasin de Player 1, va vers les fosses de Player 2
            "P2": "A"   # Après le magasin de Player 2, va vers les fosses de Player 1
        }

    def possible_moves(self, player):
        pits = self.player1_pits if player == "P1" else self.player2_pits
        return [pit for pit in pits if self.board[pit] > 0]

    def do_move(self, player, pit):
        seeds = self.board[pit]
        self.board[pit] = 0
        current = pit
        while seeds > 0:
            current = self.next_pits[current]
            if (player == "P1" and current == "P2") or (player == "P2" and current == "P1"):
                continue
            self.board[current] += 1
            seeds -= 1

        if current in self.player1_pits + self.player2_pits and self.board[current] == 1:
            opposite = self.opposite_pits[current]
            if player == "P1" and current in self.player1_pits:
                self.board["P1"] += self.board[opposite] + 1
                self.board[current] = self.board[opposite] = 0
            elif player == "P2" and current in self.player2_pits:
                self.board["P2"] += self.board[opposite] + 1
                self.board[current] = self.board[opposite] = 0

    def is_game_over(self):
        return all(self.board[pit] == 0 for pit in self.player1_pits) or \
               all(self.board[pit] == 0 for pit in self.player2_pits)

    def collect_remaining_seeds(self):
        for pit in self.player1_pits:
            self.board["P1"] += self.board[pit]
            self.board[pit] = 0
        for pit in self.player2_pits:
            self.board["P2"] += self.board[pit]
            self.board[pit] = 0

    def display_board(self):
        print("\nCurrent Board:")
        print("Your side")
        print("   " + "  ".join(self.player2_pits[::-1]))
        print("   " + "  ".join(str(self.board[pit]) for pit in self.player2_pits[::-1]))
        print(f"{self.board['P2']}                   {self.board['P1']}")
        print("   " + "  ".join(self.player1_pits))
        print("   " + "  ".join(str(self.board[pit]) for pit in self.player1_pits))
        print("Computer's side:\n")


class Game:
    def __init__(self):
        self.state = MancalaBoard()
        self.player_side = {"P1": "P1", "P2": "P2"}

    def game_over(self):
        if self.state.is_game_over():
            self.state.collect_remaining_seeds()
            return True
        return False

    def find_winner(self):
        if self.state.board["P1"] > self.state.board["P2"]:
            return "Computer", self.state.board["P1"]
        elif self.state.board["P2"] > self.state.board["P1"]:
            return "You", self.state.board["P2"]
        else:
            return "Draw", self.state.board["P1"]

    def evaluate(self):
        return self.state.board["P1"] - self.state.board["P2"]


class Play:
    def __init__(self):
        self.game = Game()

    def minimax_alpha_beta_pruning(self, game, player, depth, alpha, beta):
        if game.game_over() or depth == 1:
            return game.evaluate(), None

        best_value = -math.inf if player == "P1" else math.inf
        best_pit = None
        possible_moves = game.state.possible_moves(game.player_side[player])

        for pit in possible_moves:
            child_game = copy.deepcopy(game)
            child_game.state.do_move(game.player_side[player], pit)
            value, _ = self.minimax_alpha_beta_pruning(child_game, "P2" if player == "P1" else "P1", depth - 1, alpha, beta)

            if player == "P1":  # Maximize for computer
                if value > best_value:
                    best_value, best_pit = value, pit
                if best_value >= beta:
                    break
                # alpha = max(alpha, best_value)
                if best_value > alpha:
                    alpha = best_value
            else:  # Minimize for human
                if value < best_value:
                    best_value, best_pit = value, pit
                if best_value <=alpha:
                    break
                if best_value < beta:
                    beta = best_value
                # beta = min(beta, best_value)

            # if alpha >= beta:
            #     break

        return best_value, best_pit

    def human_turn(self):
        self.game.state.display_board()
        print("Your turn:")
        possible_moves = self.game.state.possible_moves("P2")
        print("Possible moves:", possible_moves)
        while True:
            pit = input(f"Enter your move (choose a pit from {possible_moves}): ").strip().upper()
            if pit in possible_moves:
                break
            print("Invalid move. Try again.")
        self.game.state.do_move("P2", pit)

    def computer_turn(self, depth=5):
        self.game.state.display_board()
        print("\nComputer's turn:")
        _, best_move = self.minimax_alpha_beta_pruning(self.game, "P1", depth, -math.inf, math.inf)
        print(f"Computer chooses pit {best_move}\n")
        self.game.state.do_move("P1", best_move)

    def play(self):
        print("Welcome to Mancala!")
        print("You are player 2 (top side). The computer is player 1 (bottom side).\n")
        while not self.game.game_over():
            self.computer_turn()
            if self.game.game_over():
                break
            self.human_turn()
        winner, score = self.game.find_winner()
        print(f"Game Over! Winner: {winner} with score {score}")


# Lancer le jeu
if __name__ == "__main__":
    Play().play()
