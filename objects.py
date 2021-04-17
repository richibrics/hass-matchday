from requests import Request, Session
from .consts import *
import datetime


def GetFromLink(url, session):
    # return dict from request's json response
    req = Request('GET', url)
    prepped = session.prepare_request(req)
    response = session.send(prepped)
    if response.status_code == 200:
        return response.json()
    else:
        print("API error, exiting...")
        exit(1)


class Team:
    def __init__(self, id, session):
        # TODO: Add config for: Use alternative name
        self.events = []
        self.id = id
        self.session = session
        if(self.GetData() == -1):
            raise Exception("Can't initialize " + str(id) + " team")
        self.name = self.info['strTeam']
        self.alternativeName = self.info['strAlternate']
        #print(self.name)
        self.ParseEvents()

    def GetData(self):
        try:
            # Get Team info from INFO link
            self.info = self.GetFromLink(TEAM_DETAILS_URL)['teams'][0]
            self.lastEventsData = self.GetFromLink(TEAM_LASTEVENTS_URL)
            self.nextEventsData = self.GetFromLink(TEAM_NEXTEVENTS_URL)
            return 0
        except:
            print("Data not found for team id " + str(id))
            return -1

    def Update(self):
        self.events.clear()
        if(self.GetData() == -1):
            raise Exception("Can't get data for " + str(id) + " team")
        self.ParseEvents()

    def GetFromLink(self, notFormattedUrl):
        return GetFromLink(
            notFormattedUrl.format(self.id), self.session)

    def ParseEvents(self):
        for event in self.lastEventsData['results']:
            self.events.append(Event(event, PERIOD_LAST))
        self.events.reverse()
        for event in self.nextEventsData['events']:
            self.events.append(Event(event, PERIOD_NEXT))

    def ReturnData(self):  # [{Match,Datetime,Result}]
        fixtures = []
        for event in self.events:
            fixtures.append(event.ReturnInfo())
        return fixtures

class Tournament:
    def __init__(self, id, session):
        # TODO: Add config for: Use alternative name
        self.events = []
        self.id = id
        self.session = session
        if(self.GetData() == -1):
            raise Exception("Can't initialize " + str(id) + " tournament")
        self.name = self.info['strLeague']
        self.alternativeName = self.info['strLeagueAlternate']
        print(self.name)
        self.ParseEvents()

    def GetData(self):
        # Get Team info from INFO link
        try:
            self.info = self.GetFromLink(TOURNAMENT_DETAILS_URL)['leagues'][0]
            self.lastEventsData = self.GetFromLink(TOURNAMENT_LASTEVENTS_URL)
            self.nextEventsData = self.GetFromLink(TOURNAMENT_NEXTEVENTS_URL)
            return 0
        except:
            print("Data not found for league id " + str(id))
            return -1


    def Update(self):
        self.events.clear()
        if(self.GetData() == -1):
            raise Exception("Can't get data for " + str(id) + " tournament")
        self.ParseEvents()


    def ParseEvents(self):
        for event in self.lastEventsData['events']:
            self.events.append(Event(event, PERIOD_LAST))
        self.events.reverse()
        for event in self.nextEventsData['events']:
            self.events.append(Event(event, PERIOD_NEXT))

    def GetFromLink(self, notFormattedUrl):
        return GetFromLink(
            notFormattedUrl.format(self.id), self.session)


    def ReturnData(self):  # [{Match,Datetime,Result}]
        fixtures = []
        for event in self.events:
            fixtures.append(event.ReturnInfo())
        return fixtures


class Event:
    def __init__(self, _dict, period):
        self.data = _dict
        self.period = period
        self.id = self.data['idEvent']
        self.teamHome = self.data['strHomeTeam']
        self.teamAway = self.data['strAwayTeam']
        self.GetDatetime()
        if period == PERIOD_LAST:  # Take the result
            self.goalHome = self.data['intHomeScore']
            self.goalAway = self.data['intAwayScore']
        else:
            self.goalHome = None
            self.goalAway = None
        self.Print()

    def Print(self):
        stringa = "Match: " + self.teamHome + " - " + self.teamAway
        if self.period == PERIOD_NEXT:
            stringa += " | not played"
        else:
            stringa += " | " + str(self.goalHome) + " - " + str(self.goalAway)
        print(stringa)

    def GetDatetime(self):
        # Time is in GMT
        timestamp = self.data['dateEvent']+' '+self.data['strTime']
        self.datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:00")

    def ReturnInfo(self):
        fixture = {"match": None, "datetime": None, "result": None}
        fixture['match'] = self.teamHome+" - " + self.teamAway
        fixture['datetime'] = self.datetime
        if self.period==PERIOD_LAST:    
            try:
                fixture['result'] = self.goalHome+" - " + self.goalAway
            except:
                fixture['result'] = "  -  "
        else: 
            fixture['result'] = "  -  "
        return fixture