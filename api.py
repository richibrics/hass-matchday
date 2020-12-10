from consts import *
from objects import *
from requests import Session

def Main():
    tournaments = [53]
    teams = [2692]
    objects = []
    session=Session()
    for tournament in tournaments:
        objects.append(Tournament(tournament,session))

    for team in teams:
        objects.append(Team(team,session))


if __name__ == "__main__":
    Main()