import os


class Game:
    players = []
    active = False
    dummy = 8
    board = [[8 for i in range(3)] for i in range(3)]
    turn_counter = 0
    user_input = 0

    def __init__(self):
        self.main_screen()

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
                print("\nUngültige Eingabe bitte erneut eingeben....\n")
            os.system("clear")

    def rematch(self):
        self.reset_board()
        while not self.win_det() and self.turn_counter != 9:
            self.player_turn()
        if self.turn_counter == 9:
            print("Alle Züge aufgebraucht")
        if self.win_det():
            if self.turn_counter % 2:
                print(f"{self.players[0][0]} hat gewonnen!")
            else:
                print(f"{self.players[1][0]} hat gewonnen!")

    def match(self):
        self.reset_board()
        self.get_players()
        while not self.win_det() and self.turn_counter != 9:
            self.player_turn()
        if self.turn_counter == 9:
            print("Alle Züge aufgebraucht")
        if self.win_det():
            if self.turn_counter % 2:
                print(f"{self.players[0][0]} hat gewonnen!")
            else:
                print(f"{self.players[1][0]} hat gewonnen!")

    def reset_board(self):
        self.board = [[8 for i in range(3)] for i in range(3)]
        self.turn_counter = 0
        self.user_input = 0

    def get_players(self):
        for i in range(2):
            player = (input(f'Spieler {i + 1} Name: '), i)
            self.players.append(player)

    def show_board(self):
        for i in self.board:
            print(i)

    def player_turn(self):
        turn = True
        if self.turn_counter == 0:
            self.show_board()
        if self.active:
            self.active = False
            row, col = input(f"@Spieler {self.players[1][0]}: Reihe, Spalte ").split(",")
            while turn:
                if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                    self.board[int(row) - 1][int(col) - 1] = self.players[1][1]
                    turn = False
                else:
                    row, col = input(
                        f"@Spieler {self.players[1][0]} Diese Platz ist schon belegt bitte erneut eingeben: Reihe, Spalte ").split(
                        ",")
        else:
            self.active = True
            row, col = input(f"@Spieler {self.players[0][0]}: Reihe, Spalte ").split(",")
            while turn:
                if self.board[int(row) - 1][int(col) - 1] == self.dummy:
                    self.board[int(row) - 1][int(col) - 1] = self.players[0][1]
                    turn = False
                else:
                    row, col = input(
                        f"@Spieler {self.players[0][0]} Diese Platz ist schon belegt bitte erneut eingeben: Reihe, Spalte ").split(
                        ",")
        self.turn_counter += 1
        self.show_board()

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
