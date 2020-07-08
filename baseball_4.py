from random import randint

"""
OOP version - create classes for Team and Game
"""

#----------
# constants
#----------
HOME = 0
AWAY = 1
OUT = 0

#---------------
# define classes
#---------------

class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        # self.lineup = list(range(1, 10))
        self.lineup = [chr(i+65) for i in range(9)]
        self.score = 0
        self.innings_completed = 0
        self.outs_this_innings = 0

class Game:
    def __init__(self):
        self.teams = []
        self.teams.append(Team(HOME))
        self.teams.append(Team(AWAY))
        self.bases = [None, None, None, None]

        # to start the game, the AWAY team bats first
        self.batting = AWAY
        self.bases[0] = self.get_batter()

    #--------------------------------------------------
    # methods required to process each step in the game
    #--------------------------------------------------

    def game_over(self):
        """Return True if both teams have completed 9 innings, else False."""
        if self.teams[HOME].innings_completed == 9 and self.teams[AWAY].innings_completed == 9:
            return True
        else:
            return False

    def get_score(self):
        """Use randint to get next score and return the value."""
        return randint(0, 4)

    def check_run(self, base):
        """If there is a player on the base, a run has been scored."""
        if self.bases[base] is not None:
            self.teams[self.batting].score += 1
            self.teams[self.batting].lineup.append(self.bases[base])
            self.bases[base] = None

    def check_move(self, base, score):
        """If there is a player on the base, move to next base."""
        if self.bases[base] is not None:
            self.bases[base+score] = self.bases[base]
            self.bases[base] = None

    def handle_out(self):
        """Current batter is out.

        Batter returns to team.    
        If this is the third 'out' this innings, end this innings, start next innings.
        Else next player comes out to bat.
        """
        team = self.teams[self.batting]
        team.lineup.append(self.bases[0])  # return batter to team
        team.outs_this_innings += 1
        if team.outs_this_innings == 3:  # change innings
            if self.bases[3] is not None:
                team.lineup.append(self.bases[3])
                self.bases[3] = None
            if self.bases[2] is not None:
                team.lineup.append(self.bases[2])
                self.bases[2] = None
            if self.bases[1] is not None:
                team.lineup.append(self.bases[1])
                self.bases[1] = None
            team.innings_completed += 1
            team.outs_this_innings = 0
            self.batting = not self.batting  # if it was HOME, it is now AWAY, and vice-versa

        self.bases[0] = self.get_batter()

    def handle_score(self, score):
        """Current batter has scored.

        For each player on the self.bases, move them the required self.bases.
        For each player that returns to home base, add 1 to score.
        """
        if score == 1:
            self.check_run(base=3)
            self.check_move(base=2, score=1)
            self.check_move(base=1, score=1)
            self.check_move(base=0, score=1)
        elif score == 2:
            self.check_run(base=3)
            self.check_run(base=2)
            self.check_move(base=1, score=2)
            self.check_move(base=0, score=2)
        elif score == 3:
            self.check_run(base=3)
            self.check_run(base=2)
            self.check_run(base=1)
            self.check_move(base=0, score=3)
        elif score == 4:
            self.check_run(base=3)
            self.check_run(base=2)
            self.check_run(base=1)
            self.check_run(base=0)
        self.bases[0] = self.get_batter()

    def get_batter(self):
        """Get next batter."""
        batter = self.teams[self.batting].lineup.pop(0)
        return batter

    def run_game(self):
        while not self.game_over():
            score = self.get_score()
            if score == OUT:
                self.handle_out()
            else:
                self.handle_score(score)

    def print_results(self):
        home = self.teams[HOME].score
        away = self.teams[AWAY].score
        print(f'Home score is {home}. Away score is {away}.')

        if home > away:
            print('Home team won')
        elif home < away:
            print('Away team won')
        else:
            print('Result is a draw')

if __name__ == '__main__':
    game = Game()
    game.run_game()
    game.print_results()
