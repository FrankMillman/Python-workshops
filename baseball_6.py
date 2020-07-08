from random import randint

"""
Add database functionality - create table to record scores, update scores after each game
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
        self.lineup = [chr(i+65) for i in range(9)]
        self.score = 0
        self.innings_completed = 0
        self.outs_this_innings = 0

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
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
        self.teams[self.batting].lineup.append(self.bases[0])  # return batter to team
        self.teams[self.batting].outs_this_innings += 1
        if self.teams[self.batting].outs_this_innings == 3:  # change innings
            if self.bases[3] is not None:
                self.teams[self.batting].lineup.append(self.bases[3])
                self.bases[3] = None
            if self.bases[2] is not None:
                self.teams[self.batting].lineup.append(self.bases[2])
                self.bases[2] = None
            if self.bases[1] is not None:
                self.teams[self.batting].lineup.append(self.bases[1])
                self.bases[1] = None
            self.teams[self.batting].innings_completed += 1
            self.teams[self.batting].outs_this_innings = 0
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

    def print_results(self):
        print(f'Home score is {self.teams[HOME].score}. Away score is {self.teams[AWAY].score}.')

        if self.teams[HOME].score > self.teams[AWAY].score:
            print('Home team won')
        elif self.teams[HOME].score < self.teams[AWAY].score:
            print('Away team won')
        else:
            print('Result is a draw')

    def update_database(self, cur):
        sql = """
            INSERT INTO scores (game_id, home_team_score, away_team_score)
            VALUES (?, ?, ?)
            """
        params = (self.game_id, self.teams[HOME].score, self.teams[AWAY].score)
        cur.execute(sql, params)

def setup_database(conn):
    cur = conn.cursor()
    sql = """
        DROP TABLE IF EXISTS scores
        """
    cur.execute(sql)
    sql = """
        CREATE TABLE scores (
        row_id INTEGER PRIMARY KEY,
        game_id INT,
        home_team_score INT,
        away_team_score INT
        )
        """
    cur.execute(sql)

if __name__ == '__main__':

    games = []
    for game_id in range(3):
        games.append(Game(game_id))

    while not all(game.game_over() for game in games):
        for game in games:
            if not game.game_over():
                score = randint(0, 4)
                if score == OUT:
                    game.handle_out()
                else:
                    game.handle_score(score)

    for game in games:
        game.print_results()

    # to create an sqlite3 connection, you give it a path to a file - if the file does not exist, sqlite3 will create it
    # you can use any directory you choose for this
    # here, we get the current path, so that the database is stored in the same directory as the program
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    import sqlite3
    conn = sqlite3.connect(os.path.join(path, 'baseball_db'))

    # comment this line out after the first time, else it will delete and recreate the table on each run
    setup_database(conn)

    cur = conn.cursor()
    for game in games:
        game.update_database(cur)
    conn.commit()
