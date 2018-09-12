import actions
import players

class Single_Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.action1 = None
        self.player2 = player2
        self.action2 = None
        self.winner = 'Nobody'

    def play_game(self):
        self.action1 = self.player1.choose_action()
        self.action2 = self.player2.choose_action()
        if self.action1 < self.action2:
            self.player1.recive_result(self.action1, self.action2, self.player2)
            self.player2.recive_result(self.action2, self.action1, self.player2)
            self.winner = self.player2.get_name()
        elif self.action1 == self.action2:
            self.player1.recive_result(self.action1, self.action2, None)
            self.player2.recive_result(self.action2, self.action1, None)
        else:
            self.player1.recive_result(self.action1, self.action2, self.player1)
            self.player2.recive_result(self.action2, self.action1, self.player1)
            self.winner = self.player1.get_name()

    def __str__(self):
        return self.player1.get_name() + ': ' + self.action1.__str__() +'. ' + self.player2.get_name() +': '+ self.action2.__str__() + '. -> ' + self.winner + ' wins.'

def main():
    player1 = players.randomPlayer()
    player2 = players.randomPlayer()
    game = Single_Game(player1,player2)
    game.play_game()
    print(game)

main()