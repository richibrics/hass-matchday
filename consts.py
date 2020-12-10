TEAM_DETAILS_URL = "https://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id={}" # Needs ID
#TEAM_SEARCH_URL = "https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t={}" # Search not implemented yet
TEAM_LASTEVENTS_URL = "https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id={}" # 5 events
TEAM_NEXTEVENTS_URL = "https://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id={}" # 5 events

TOURNAMENT_DETAILS_URL = "https://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id={}" # Needs ID
TOURNAMENT_LASTEVENTS_URL = "https://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id={}" # 15 events
TOURNAMENT_NEXTEVENTS_URL = "https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id={}" # 15 events

# TEAM_EVENTS_DAYS_DISTANCE = 14
# TOURNAMENT_EVENTS_ROUND_NUMBER = 1

STATUS_NOTPLAYED = 0
# STATUS_INPROGRESS = 2 # DB without live results
STATUS_PLAYED = 1
