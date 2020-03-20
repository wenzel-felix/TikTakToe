class Game:

    #vars
    players = []
    active = False
    turn_counter = 0
    user_input = 0
    bot_participate = False

    #dummy var equals 'empty' board's filler
    dummy = 8
    board = [[8 for i in range(3)] for i in range(3)]

    def __init__(self):
        self.main_screen()

    #sets up menu-window to start the game
    def main_screen(self):
        while self.user_input == 0:
            if self.turn_counter == 0:
                x = input("'1' to start new game\n'3' to exit\n")
            else:
                x = input("'1' to start new game\n'2' for a rematch\n'3' to exit\n")
            if int(x) == 1:
                self.match(True)
            elif int(x) == 2 and self.turn_counter != 0:
                self.match(False)
            elif int(x) == 3:
                print("\nExited.....")
                self.user_input = 1
            else:
                print("\nInvalid input, please try it again.....\n")

    #function to start a match
    def match(self, new_game):
        self.reset_board()
        if new_game:
            self.get_players()
        while not self.win_det() and self.turn_counter != 9:
            self.player_turn()
        if self.turn_counter == 9:
            print("Tie")
        if self.win_det():
            if self.turn_counter % 2:
                print(f"{self.players[0][0]} won!")
            else:
                print(f"{self.players[1][0]} won!")

    #resets the board and sets user_input to 0 for the menu's while-loop
    def reset_board(self):
        self.board = [[8 for i in range(3)] for i in range(3)]
        self.turn_counter = 0
        self.user_input = 0

    #creates a player-list
    def get_players(self):
        if input("multiplayer  y/n?\n") == "y":
            self.bot_participate = False
            for i in range(2):
                player = (input(f'player {i + 1} name: '), i)
                self.players.append(player)
        else:
            self.bot_participate = True
            for i in range(2):
                name = "player"
                if i == 1:
                    name = "bot"
                player = (input(f'{name} name: '), i)
                self.players.append(player)

    #prints the current board
    def show_board(self):
        for i in self.board:
            print(i)

    #resonsible for the player's turns (with bot_turn-function implemented)
    def player_turn(self):
        turn = True
        if self.turn_counter == 0:
            self.show_board()
        if self.active:
            self.active = False
            if self.bot_participate:
                self.bot_turn(self.board)
            else:
                row, col = input(f"@player {self.players[1][0]}: row, column ").split(",")
                while turn:
                    if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                        self.board[int(row) - 1][int(col) - 1] = self.players[1][1]
                        turn = False
                    else:
                        row, col = input(
                            f"@player {self.players[1][0]} this field is not empty, please try again: row, column ").split(",")
        else:
            self.active = True
            row, col = input(f"@player {self.players[0][0]}: row, column ").split(",")
            while turn:
                if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                    self.board[int(row) - 1][int(col) - 1] = self.players[0][1]
                    turn = False
                else:
                    row, col = input(
                        f"@player {self.players[0][0]} this field is not empty, please try again: row, column ").split(",")
        self.turn_counter += 1
        self.show_board()

    #plays the best move for the bot (depending on minimax value)
    def bot_turn(self, x_board):
        print(f"@bot {self.players[1][0]}")
        bestVal = -1000
        bestMove = []
        row, col = -1, -1
        bestMove.append(row)
        bestMove.append(col)

        for i in range(3):
            for x in range(3):
                if x_board[i][x] == self.dummy:
                    x_board[i][x] = self.players[1][1]
                    turn = self.turn_counter
                    moveVal = self.minimax(x_board, 0, False)
                    x_board[i][x] = self.dummy

                    if moveVal > bestVal:
                        bestMove[0] = i
                        bestMove[1] = x
                        bestVal = moveVal
        self.board[bestMove[0]][bestMove[1]] = self.players[1][1]

    #searches for the highest value turn for the bot
    def minimax(self, x_board, depth, isMax):
        score = self.game_value()
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        #simulates the bot moves
        if isMax:
            best = -1000
            for i in range(3):
                for x in range(3):
                    if x_board[i][x] == self.dummy:
                        x_board[i][x] = self.players[1][1]

                        best = max(best, self.minimax(x_board, depth+1, not isMax))

                        x_board[i][x] = self.dummy
            return best
        #simulates the player moves
        else:
            best = 1000
            for i in range(3):
                for x in range(3):
                    if x_board[i][x] == self.dummy:
                        x_board[i][x] = self.players[0][1]

                        best = min(best, self.minimax(x_board, depth+1, isMax))

                        x_board[i][x] = self.dummy
            return best

    #returns the values for the minimax function
    def game_value(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                if self.board[i][1] != self.dummy:
                    if not self.active:
                        return -10
                    else:
                        return 10
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                if self.board[1][i] != self.dummy:
                    if not self.active:
                        return -10
                    else:
                        return 10
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[1][1] != self.dummy:
                if not self.active:
                    return -10
                else:
                    return 10
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[1][1] != self.dummy:
                if not self.active:
                    return -10
                else:
                    return 10
        return 0

    #looks every turn if somebody has won
    def win_det(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1]:
                if self.board[i][1] == self.board[i][2]:
                    if self.board[i][1] != self.dummy:
                        return True
        for i in range(3):
            if self.board[0][i] == self.board[1][i]:
                if self.board[1][i] == self.board[2][i]:
                    if self.board[1][i] != self.dummy:
                        return True
        if self.board[0][0] == self.board[1][1]:
            if self.board[1][1] == self.board[2][2]:
                if self.board[1][1] != self.dummy:
                    return True
        if self.board[0][2] == self.board[1][1]:
            if self.board[1][1] == self.board[2][0]:
                if self.board[1][1] != self.dummy:
                    return True
        return False

g = Game()