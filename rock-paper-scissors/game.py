import actions
import players
import matplotlib.pyplot as plt

# Class for containing and executing a single game. Takes two players as arguments, can play successive games
class Single_Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.action1 = None
        self.player2 = player2
        self.action2 = None
        self.winner = None
        self.winnerStr = 'Nobody'

    # Asks the players for their actions, then finds the winner
    def play_game(self):
        self.action1 = self.player1.choose_action()
        self.action2 = self.player2.choose_action()
        if self.action1 < self.action2:
            self.winner = self.player2
            self.player1.recive_result(self.action1, self.action2)
            self.player2.recive_result(self.action2, self.action1)
            self.winnerStr = self.winner.get_name()
        elif self.action1 == self.action2:
            self.winner = None
            self.player1.recive_result(self.action1, self.action2)
            self.player2.recive_result(self.action2, self.action1)
            self.winnerStr = 'Nobody'
        else:
            self.winner = self.player1
            self.player1.recive_result(self.action1, self.action2)
            self.player2.recive_result(self.action2, self.action1)
            self.winnerStr = self.winner.get_name()

    # Textual representation of the current game state
    def __str__(self):
        return self.player1.get_name() + ': ' + self.action1.__str__() +'. ' + self.player2.get_name() +': '+ self.action2.__str__() + '. -> ' + self.winner + ' wins.'

# Class for simulating a series of games. Takes no arguments, all attributes are set by the user.
class Tournament:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.num_games = 0
        self.win_history = []
        self.win_rate = [] 

    # Asks the user for the type of players they want.
    def set_players(self):
        player_types = [players.randomPlayer, players.sequentialPlayer, players.Most_Common, players.Historian]
        while self.player1 == None:
            print("Please select the first player type from the following list by number:")
            i = 0
            for element in player_types:
                print(str(i) + ": "+element.get_name(element))
                i += 1
            choice = input(">> ")
            if int(choice) in range(0,len(player_types)):
                self.player1 = self.choose_new_player(int(choice))
        while self.player2 == None:
            print("Please select the second player type from the following list by number:")
            i = 0
            for element in player_types:
                print(str(i) + ": "+element.get_name(element))
                i += 1
            choice = input(">> ")
            if int(choice) in range(0,len(player_types)):
                self.player2 = self.choose_new_player(int(choice))

    # Helpermethod for generating new player objects
    def choose_new_player(self, n):
        player = None
        if(n == 0):
            player = players.randomPlayer()
        elif n == 1:
            player = players.sequentialPlayer()
        elif n == 2:
            player = players.Most_Common()
        elif n == 3:
            i = 0
            while i == 0:
                print("How much memory should the historian have?")
                choice = input(">> ")
                if int(choice) > 0:
                    i = int(choice)
                    player = players.Historian(i)
        return player
    
    # Queries the user for the number of games to be played
    def set_n_games(self):
        while self.num_games == 0:
            print("How many games would you like to play?")
            choice = input(">>")
            try:
                choice = int(choice)
                if(choice < 0):
                    raise TypeError("Cannot be less than zero")
                self.num_games = choice
            except TypeError:
                print("Invalid input. Try again")

    # Plots the results using matplotlib
    def plot(self):
        plt.axhline(y=0.5, color = 'r', linestyle =':')
        plt.plot(self.win_rate)
        plt.ylabel(self.player1.get_name() + "Win rate")
        plt.axis([0, len(self.win_rate)-1, 0 , 1])
        plt.show()
        
    # Calculates the winrate for player 1 in range [0,1]
    def calc_winrate(self):
        i = 0
        temp_sum = 0
        for element in self.win_history:
            i += 1
            if(element == 1):
                temp_sum += element
            self.win_rate.append(temp_sum/i)
    
    # Main class methon, actually executes the simulation.
    def play(self):
        self.set_players()
        self.set_n_games()
        self.game = Single_Game(self.player1, self.player2)
        for j in range(0, self.num_games):
            self.game.play_game()
            if self.game.winner == self.player1:
                self.win_history.append(1)
            elif self.game.winner == self.player2:
                self.win_history.append(2)
            else:
                self.win_history.append(0)
        self.calc_winrate()
        self.plot()

def main():
    game = Tournament()
    game.play()
main()