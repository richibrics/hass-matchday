from requests import Request, Session
from consts import *
import brotli

def GetFromLink(url, session):
    # print(url)
    # return dict from request's json response
    headers = {'accept': '*/*',
               'user-agent': 'SofascoreApp/6.6.32 (com.SofaScore.iOS; build:414; iOS 14.0.0) Alamofire/4.9.1 deb', 'accept-language': 'it-it', 'accept-encoding': 'gzip, deflate, br', 'cache-control': 'max-age=0'}
    req = Request('GET', url, headers=headers)
    prepped = session.prepare_request(req)
    response = session.send(prepped)
    if response.status_code == 200:
        return response.json()
    else:
        print("API error, exiting...")
        exit(1)


class Team:
    def __init__(self, id, session):
        self.events = []
        self.session = session
        self.GetData(id)
        self.name = self.info['name']
        print(self.name+"\n")
        self.ParseEvents()

    def GetData(self, id):
        # Get Team info from INFO link
        self.info = GetFromLink(TEAM_DETAILS_URL.format(id), self.session)
        self.eventsData = GetFromLink(
            TEAM_LASTNEXT_URL.format(id), self.session)

    def ParseEvents(self):
        for tournament in self.eventsData['last']['tournaments']:
            for event in tournament['events']:
                # Save only X last matches
                self.events.append(Event(event))
        for tournament in self.eventsData['next']['tournaments']:
            for event in tournament['events']:
                # Should skip some matches, keep only the last and the x future events (live included)
                self.events.append(Event(event))


class Tournament:
    def __init__(self, id, session):
        self.events = []
        self.session = session
        self.GetData(id)
        self.name = self.eventsData['tournaments'][0]['tournament']['name']
        print(self.name)
        self.ParseEvents()

    def GetData(self, id):
        # Get Team info from INFO link
        #self.info = GetFromLink(TOURNAMENT_INFO_URL.format(id))
        self.eventsData = GetFromLink(
            TOURNAMENT_EVENTS_URL.format(id), self.session)

    def ParseEvents(self):
        for event in self.eventsData['tournaments'][0]['events']:
            # Should skip some matches
            self.events.append(Event(event))


class Event:
    def __init__(self, _dict):
        self.data = _dict
        self.teamHome = self.data['homeTeam']['name']
        self.teamAway = self.data['awayTeam']['name']
        if 'display' in self.data['homeScore']:
            self.goalHome = self.data['homeScore']['display']
            self.goalAway = self.data['awayScore']['display']
        else:
            self.goalHome = None
            self.goalAway = None
        if self.data['status']['type'] == "finished":
            self.status = STATUS_PLAYED
        elif self.data['status']['type'] == "inprogress":
            self.status = STATUS_INPROGRESS
        else:
            self.status = STATUS_NOTPLAYED
        self.Print()

    def Print(self):
        stringa = "Match: " + self.teamHome + " - " + self.teamAway
        if self.status == STATUS_NOTPLAYED:
            stringa += " | not played"
        else:
            stringa += " | " + str(self.goalHome) + " - " + str(self.goalAway)
        print(stringa)
