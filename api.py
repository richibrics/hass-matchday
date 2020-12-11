from consts import *
from objects import *
from requests import Session

def Main():
    tournaments = [4332]
    teams = [133667]
    objects = []
    session=Session()
    for tournament in tournaments:
        print("\n\nNew\n")
        objects.append(Tournament(tournament,session))

    for team in teams:
        print("\n\nNew\n")
        objects.append(Team(team,session))


if __name__ == "__main__":
    Main()