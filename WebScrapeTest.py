import requests
from xlsxExporter import exportToxlsx
from bs4 import BeautifulSoup

URL1 = "https://www.start.gg/tournament/arcade-time-knockout-smash-brothers-tournament-with-hungrybox-2/event/melee-singles/brackets/2177508/3167981"
URL2 = "https://www.start.gg/tournament/arcade-time-knockout-smash-brothers-tournament-with-hungrybox-2/event/ultimate-singles/brackets/2175874/3165749"

URL = URL2

URLLIST = []
URLLIST.append(URL1)
URLLIST.append(URL2)

class Player():
    def __init__(self):
        self.opponents = {} # name: (Setsplayed, setswon, setslost, gamesplayed, gameswon, gameslost, nocontest)

    def addOpponentData(self,matchdata): #matchdata as (,OpponentName, GamesIWon, GamesILost, Game)
        name = matchdata[0]
        gameswon = matchdata[1]
        gameslost = matchdata[2]
        game = matchdata[3]

        gamesplayed = gameswon+gameslost
        if game not in self.opponents:
            self.opponents[game] = {}
        if name not in self.opponents[game]:
            self.opponents[game][name] = (0,0,0,0,0,0,0)

        if gamesplayed == 0:
            self.opponents[game][name] = (self.opponents[game][name][0], self.opponents[game][name][1], self.opponents[game][name][2], self.opponents[game][name][3], self.opponents[game][name][4],self.opponents[game][name][5],self.opponents[game][name][6]+1)
        elif gameswon > gameslost:
            self.opponents[game][name] = (self.opponents[game][name][0]+1, self.opponents[game][name][1]+1, self.opponents[game][name][2], self.opponents[game][name][3]+gamesplayed, self.opponents[game][name][4]+gameswon, self.opponents[game][name][5]+gameslost, self.opponents[game][name][6])
        elif gameslost > gameswon:
            self.opponents[game][name] = (self.opponents[game][name][0]+1, self.opponents[game][name][1], self.opponents[game][name][2]+1, self.opponents[game][name][3]+gamesplayed, self.opponents[game][name][4]+gameswon, self.opponents[game][name][5]+gameslost, self.opponents[game][name][6])




def gatherData(URL):
    URLSPLITS = URL.split('/')
    gamesplit = URLSPLITS.index("brackets")
    game = URLSPLITS[gamesplit - 1]

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    matches = soup.find_all("div", class_="match has-identifier reportable")
    winnername = ""
    losername = ""
    names = {}
    players = {}

    for match in matches:
        if losername == "CCgrabs":
            print("beep")

        winnerdata = match.find("div", class_="match-player entrant winner")
        loserdata = match.find("div", class_="match-player entrant loser")

        if winnerdata == None:
            winnerdata = match.find("div", class_="match-player entrant winner missing")

        if loserdata == None:
            loserdata = match.find("div", class_="match-player entrant loser missing dq")

        if loserdata == None:
            loserdata = match.find("div", class_="match-player entrant loser missing")

        if loserdata:
            losername = loserdata.find("span", class_="match-player-name-container")
            losername = str(losername.contents[len(losername.contents) - 1])
            losergames = loserdata.contents[1].text

        if winnerdata:
            winnername = winnerdata.find("span", class_="match-player-name-container")
            winnername = str(winnername.contents[len(winnername.contents) - 1])
            winnergames = winnerdata.contents[1].text
            if winnergames == '':
                winnergames = 0
            winnergames = int(winnergames)

        if losergames == "DQ":
            losergames = 0
        losergames = int(losergames)

        if winnername not in names:
            ## (Name:(sets played, sets won, games played, games won, dq's))
            names[winnername] = {}
            names[winnername][game] = 0,0,0,0,0
        if winnergames == 0:
            names[winnername][game] = names[winnername][game][0], names[winnername][game][1], names[winnername][game][2], names[winnername][game][3], \
            names[winnername][game][4]
        else:
            names[winnername][game] = names[winnername][game][0] + 1, names[winnername][game][1] + 1, names[winnername][game][
                2] + winnergames + losergames, names[winnername][game][3] + winnergames, names[winnername][game][4]

        losergames = int(losergames)
        if losername not in names:
            names[losername] = {}
            names[losername][game] = 0, 0, 0, 0, 0
        if winnergames == 0:
            names[losername][game] = names[losername][game][0], names[losername][game][1], names[losername][game][2], names[losername][game][3], \
            names[losername][game][4] + 1
        else:
            names[losername][game] = names[losername][game][0] + 1, names[losername][game][1], names[losername][game][
                2] + winnergames + losergames, names[losername][game][3] + losergames, names[losername][game][4]

        # matchdata as (OpponentName, GamesIWon, GamesILost)
        if winnername == "Hungrybox":
            print("beep")

        if winnername not in players:
            players[winnername] = Player()
        players[winnername].addOpponentData((losername, winnergames, losergames, game))

        if losername == "Yho!":
            print("teehee")
        if losername not in players:
            players[losername] = Player()
        players[losername].addOpponentData((winnername, losergames, winnergames, game))

    return names, players

def fetchURLS(URL):
    listofURL = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    return listofURL


masternames = {}
masterplayers = {}

for URL in URLLIST:


    URLSPLITS = URL.split('/')
    gamesplit = URLSPLITS.index("brackets")
    game = URLSPLITS[gamesplit-1]

    if URLSPLITS[len(URLSPLITS)-1] != "brackets":
        urlnames, urlplayers = gatherData(URL)


        for name in urlnames:
            if name not in masternames:
                masternames[name] = {}
                masternames[name][game] = 0,0,0,0,0
            if game not in masternames[name]:
                masternames[name][game] = 0,0,0,0,0
            masternames[name][game] = masternames[name][game][0] + urlnames[name][game][0],masternames[name][game][1]+urlnames[name][game][1],masternames[name][game][2]+urlnames[name][game][2],masternames[name][game][3]+urlnames[name][game][3],masternames[name][game][4]+urlnames[name][game][4]

        for player in urlplayers:
            if player not in masterplayers:
                masterplayers[player] = urlplayers[player]
            else:
                if game not in masterplayers[player].opponents:
                    masterplayers[player].opponents[game] = {}
                for opponent in urlplayers[player].opponents[game]:
                    if opponent not in masterplayers[player].opponents[game]:
                        masterplayers[player].opponents[game][opponent] = 0, 0, 0, 0, 0, 0, 0
                    masterplayers[player].opponents[game][opponent] = masterplayers[player].opponents[game][opponent][0] + urlplayers[player].opponents[game][opponent][0], \
                                                        masterplayers[player].opponents[game][opponent][1] + urlplayers[player].opponents[game][opponent][1], \
                                                        masterplayers[player].opponents[game][opponent][2] + urlplayers[player].opponents[game][opponent][2], \
                                                        masterplayers[player].opponents[game][opponent][3] + urlplayers[player].opponents[game][opponent][3], \
                                                        masterplayers[player].opponents[game][opponent][4] + urlplayers[player].opponents[game][opponent][4], \
                                                        masterplayers[player].opponents[game][opponent][5] + urlplayers[player].opponents[game][opponent][5], \
                                                        masterplayers[player].opponents[game][opponent][6] + urlplayers[player].opponents[game][opponent][6]
    else:
        urllist = fetchURLS(URL)

    #for player in players:
        #print(player.text)
        #if len(player.contents) urlnames[name]> 1:
            #name = player.contents[1]
        #else: name = player.text
        #if name not in names:
            #names.append(str(name))




print("goodbye")
exportToxlsx(masternames, masterplayers)
quit()