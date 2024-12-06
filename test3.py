class Mancala:
    def __init__(self):
        # Initial setup of the Mancala board
        self.board = {
            'player1': [4, 4, 4, 4, 4, 4],
            'player2': [4, 4, 4, 4, 4, 4],
            'store1': 0,
            'store2': 0
        }
        self.current_player = 'player1'

    def display_board(self):
        print("Computer's side:")
        print("  L  K  J  I  H  G")
        print('  ', ' '.join(str(x) for x in self.board['player1']), self.board['store1'])
        print("0", " " * 18, "1")
        print("Your side:")
        print("  A  B  C  D  E  F")
        print('  ', ' '.join(str(x) for x in self.board['player2']), self.board['store2'])

    def possible_moves(self):
        return [chr(ord('I') + i) for i in range(6) if self.board[self.current_player][i] > 0]

    def play_move(self, move):
        # Translate the move to a pit index
        pit_index = ord(move) - ord('I')
        seeds = self.board[self.current_player][pit_index]
        self.board[self.current_player][pit_index] = 0

        # Distribute seeds
        index = pit_index
        while seeds > 0:
            index += 1
            if self.current_player == 'player1' and index == 6:
                index = 0
            elif self.current_player == 'player2' and index == 5:
                index = 0
            if self.current_player == 'player1':
                self.board['player1'][index] += 1
            else:
                self.board['player2'][index] += 1
            seeds -= 1

        # Capture seeds
        if self.current_player == 'player1' and 0 <= index < 6 and self.board['player1'][index] == 1:
            self.board['store1'] += self.board['player1'][index] + self.board['player2'][5 - index]
            self.board['player1'][index] = 0
            self.board['player2'][5 - index] = 0
        elif self.current_player == 'player2' and 0 <= index < 6 and self.board['player2'][index] == 1:
            self.board['store2'] += self.board['player2'][index] + self.board['player1'][5 - index]
            self.board['player2'][index] = 0
            self.board['player1'][5 - index] = 0

        # Switch player
        self.current_player = 'player2' if self.current_player == 'player1' else 'player1'

    def game_over(self):
        # Check if the game is over
        return all(seeds == 0 for seeds in self.board['player1']) or all(seeds == 0 for seeds in self.board['player2'])

    def winner(self):
        if self.board['store1'] > self.board['store2']:
            return "Computer wins!"
        elif self.board['store1'] < self.board['store2']:
            return "You win!"
        else:
            return "It's a draw!"

# Running the game
mancala_game = Mancala()
while not mancala_game.game_over():
    mancala_game.display_board()
    if mancala_game.current_player == 'player1':
        print("Computer's turn:")
        move = mancala_game.possible_moves()[0]  # Simulate computer choosing a move
        print(f"Computer chooses pit {move}")
    else:
        move = input(f"Your turn:\nPossible moves: {mancala_game.possible_moves()}\nEnter your move (choose a pit): ").upper()
        while move not in mancala_game.possible_moves():
            print("Invalid move. Try again.")
            move = input("Enter your move (choose a pit): ").upper()
    mancala_game.play_move(move)

mancala_game.display_board()
print(mancala_game.winner())




