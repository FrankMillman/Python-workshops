from types import SimpleNamespace
from random import randint

"""
Original version of baseball game
"""

#----------
# constants
#----------
HOME = 0
AWAY = 1
OUT = 0

#-----------------
# global variables
#-----------------

# list from 1-9 for each team
teams = []
teams.append(list(range(1, 10)))
teams.append(list(range(1, 10)))

# SimpleNamespace for each team to keep track of the score
scores = []
scores.append(SimpleNamespace(score=0, innings_completed=0, outs_this_innings=0))
scores.append(SimpleNamespace(score=0, innings_completed=0, outs_this_innings=0))

# set up bases
bases = [None, None, None, None]

# to start the game, the AWAY team bats first
batting = AWAY

#----------------------------------------------------
# functions required to process each step in the game
#----------------------------------------------------

def game_over():
    """Return True if both teams have completed 9 innings, else False."""
    if scores[HOME].innings_completed == 9 and scores[AWAY].innings_completed == 9:
        return True
    else:
        return False

def get_score():
    """Use randint to get next score and return the value."""
    return randint(0, 4)

def handle_out():
    """Current batter is out.

    Batter returns to team.    
    If this is the third 'out' this innings, end this innings, start next innings.
    Else next player comes out to bat.
    """
    global batting  # if 3 outs, change batting team - it is a global variable, so must declare 'global'
    teams[batting].append(bases[0])  # return batter to team
    scores[batting].outs_this_innings += 1
    if scores[batting].outs_this_innings == 3:  # change innings
        if bases[3] is not None:
            teams[batting].append(bases[3])
            bases[3] = None
        if bases[2] is not None:
            teams[batting].append(bases[2])
            bases[2] = None
        if bases[1] is not None:
            teams[batting].append(bases[1])
            bases[1] = None
        scores[batting].innings_completed += 1
        scores[batting].outs_this_innings = 0
        batting = not batting  # if it was HOME, it is now AWAY, and vice-versa

    bases[0] = get_batter()

def handle_score(score):
    """Current batter has scored.

    For each player on the bases, move them the required bases.
    For each player that returns to home base, add 1 to score.
    """
    if score == 1:
        if bases[3] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[3])
            bases[3] = None
        if bases[2] is not None:
            bases[3] = bases[2]
            bases[2] = None
        if bases[1] is not None:
            bases[2] = bases[1]
            bases[1] = None
        bases[1] = bases[0]
        bases[0] = get_batter()
    elif score == 2:
        if bases[3] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[3])
            bases[3] = None
        if bases[2] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[2])
            bases[2] = None
        if bases[1] is not None:
            bases[3] = bases[1]
            bases[1] = None
        bases[2] = bases[0]
        bases[0] = get_batter()
    elif score == 3:
        if bases[3] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[3])
            bases[3] = None
        if bases[2] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[2])
            bases[2] = None
        if bases[1] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[1])
            bases[1] = None
        bases[3] = bases[0]
        bases[0] = get_batter()
    elif score == 4:
        if bases[3] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[3])
            bases[3] = None
        if bases[2] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[2])
            bases[2] = None
        if bases[1] is not None:
            scores[batting].score += 1
            teams[batting].append(bases[1])
            bases[1] = None
        scores[batting].score += 1
        teams[batting].append(bases[0])
        bases[0] = get_batter()

def get_batter():
    """Get next batter."""
    batter = teams[batting].pop(0)
    return batter

#-------------
# main routine
#-------------

def run_game():
    bases[0] = get_batter()
    while not game_over():
        score = get_score()
        if score == OUT:
            handle_out()
        else:
            handle_score(score)
        # print(teams)
        # print(score)
        # print(scores)
        # print(bases)
        # input()

#--------------
# print results
#--------------

def print_results():
    print(f'Home score is {scores[HOME].score}. Away score is {scores[AWAY].score}.')

    if scores[HOME].score > scores[AWAY].score:
        print('Home team won')
    elif scores[HOME].score < scores[AWAY].score:
        print('Away team won')
    else:
        print('Result is a draw')

if __name__ == '__main__':
    run_game()
    print_results()
