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

    #sets up menue-window to start the game
    def main_screen(self):
        while self.user_input == 0:
            if self.turn_counter == 0:
                x = input("'1' für Neues Spiel\n'3' für Beenden\n")
            else:
                x = input("'1' für Neues Spiel\n'2' für Rematch\n'3' für Beenden\n")
            if int(x) == 1:
                self.match()
            elif int(x) == 2 and self.turn_counter != 0:
                self.rematch()
            elif int(x) == 3:
                print("\nBeendet.....")
                self.user_input = 1
            else:
                print("\nUngültige Eingabe bitte erneut eingeben....Enter drücken....\n")

    #function for rematch with same Player/Bot-name
    def rematch(self):
        self.reset_board()
        while not self.win_det() and self.turn_counter != 9:
            self.player_turn()
        if self.turn_counter == 9:
            print("Unentschieden")
        if self.win_det():
            if self.turn_counter % 2:
                print(f"{self.players[0][0]} hat gewonnen!")
            else:
                print(f"{self.players[1][0]} hat gewonnen!")

    #function to start a match from scratch
    def match(self):
        self.reset_board()
        self.get_players()
        while not self.win_det() and self.turn_counter != 9:
            self.player_turn()
        if self.turn_counter == 9:
            print("Unentschieden")
        if self.win_det():
            if self.turn_counter % 2:
                print(f"{self.players[0][0]} hat gewonnen!")
            else:
                print(f"{self.players[1][0]} hat gewonnen!")

    #resets the board and sets user_input to 0 for the menue's while-loop
    def reset_board(self):
        self.board = [[8 for i in range(3)] for i in range(3)]
        self.turn_counter = 0
        self.user_input = 0

    #creates a player-list
    def get_players(self):
        if input("Multiplayer  J/N?\n") == "J":
            self.bot_participate = False
            for i in range(2):
                player = (input(f'Spieler {i + 1} Name: '), i)
                self.players.append(player)
        else:
            self.bot_participate = True
            for i in range(2):
                name = "Spieler"
                if i == 1:
                    name = "Bot"
                player = (input(f'{name} Name: '), i)
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
                row, col = input(f"@Spieler {self.players[1][0]}: Reihe, Spalte ").split(",")
                while turn:
                    if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                        self.board[int(row) - 1][int(col) - 1] = self.players[1][1]
                        turn = False
                    else:
                        row, col = input(
                            f"@Spieler {self.players[1][0]} Diese Platz ist schon belegt bitte erneut eingeben: Reihe, Spalte ").split(",")
        else:
            self.active = True
            row, col = input(f"@Spieler {self.players[0][0]}: Reihe, Spalte ").split(",")
            while turn:
                if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                    self.board[int(row) - 1][int(col) - 1] = self.players[0][1]
                    turn = False
                else:
                    row, col = input(
                        f"@Spieler {self.players[0][0]} Diese Platz ist schon belegt bitte erneut eingeben: Reihe, Spalte ").split(",")
        self.turn_counter += 1
        self.show_board()

    #plays the best move for the bot (depending on minimax value)
    def bot_turn(self, x_board):
        print(f"@Bot {self.players[1][0]}")
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