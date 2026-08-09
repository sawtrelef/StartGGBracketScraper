import gc

import requests
from bs4 import BeautifulSoup
from pysmashgg import SmashGG
from os.path import exists
from time import sleep


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
            self.opponents[game][name] = [0,0,0,0,0,0,0]

        if gamesplayed == 0:
            self.opponents[game][name] = [self.opponents[game][name][0], self.opponents[game][name][1], self.opponents[game][name][2], self.opponents[game][name][3], self.opponents[game][name][4],self.opponents[game][name][5],self.opponents[game][name][6]+1]
        elif gameswon > gameslost:
            self.opponents[game][name] = [self.opponents[game][name][0]+1, self.opponents[game][name][1]+1, self.opponents[game][name][2], self.opponents[game][name][3]+gamesplayed, self.opponents[game][name][4]+gameswon, self.opponents[game][name][5]+gameslost, self.opponents[game][name][6]]
        elif gameslost > gameswon:
            self.opponents[game][name] = [self.opponents[game][name][0]+1, self.opponents[game][name][1], self.opponents[game][name][2]+1, self.opponents[game][name][3]+gamesplayed, self.opponents[game][name][4]+gameswon, self.opponents[game][name][5]+gameslost, self.opponents[game][name][6]]

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
        winnerdata = match.find("div", class_="match-player entrant winner")
        loserdata = match.find("div", class_="match-player entrant loser")

        if winnerdata == None and loserdata == None:
            winnerdata = match.find("div", class_="match-section match-section-top")
            winnerdata = winnerdata.find("div", class_="match-player entrant loser missing dq")
            loserdata = match.find("div", class_="match-section match-section-bottom")
            loserdata = loserdata.find("div", class_="match-player entrant loser missing dq")

        if winnerdata == None:
            winnerdata = match.find("div", class_="match-player entrant winner missing")

        if loserdata == None:
            loserdata = match.find("div", class_="match-player entrant loser missing dq")

        if loserdata == None:
            loserdata = match.find("div", class_="match-player entrant loser missing")

        if loserdata == None:
            loserdata = match.find("div", class_="match-player entrant loser dq")

        if loserdata:
            losername = loserdata.find("span", class_="match-player-name-container")
            if losername == None:
                losername = loserdata.find("div", class_="match-player-name")
                losername = losername.find("span")
            losername = str(losername.contents[len(losername.contents) - 1])
            losergames = loserdata.contents[1].text

        if winnerdata:
            winnername = winnerdata.find("span", class_="match-player-name-container")
            if winnername == None:
                winnername = winnerdata.find("div", class_="match-player-name")
                winnername = winnername.find("span")
            winnername = str(winnername.contents[len(winnername.contents) - 1])
            winnergames = winnerdata.contents[1].text
            if winnergames == '' or winnergames == 'DQ':
                winnergames = 0
            winnergames = int(winnergames)

        if loserdata == None and winnerdata == None:
            continue

        if losergames == "DQ":
            losergames = 0
        if losergames == '':
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

        if winnername not in players:
            players[winnername] = Player()
        players[winnername].addOpponentData((losername, winnergames, losergames, game))

        if losername not in players:
            players[losername] = Player()
        players[losername].addOpponentData((winnername, losergames, winnergames, game))

    return names, players

def pullFromBracket(URL,smash):
    URLSPLITS = URL.split('/')
    bracketID = URLSPLITS[-1]
    EVENTNAME = URLSPLITS[URLSPLITS.index("tournament") + 1]
    #stuff = smash.tournament_phase_and_phasegroup(EVENTNAME)
    #game = stuff['data']['tournament']['events']['name']
    pagestuff = smash.bracket_show_sets_and_event(bracketID, 1)
    eventID = pagestuff['data']['phaseGroup']['phase']['event']['id']
    if pagestuff['data']['phaseGroup']['phase']['bracketType'] == 'RACE' or pagestuff['data']['phaseGroup']['phase']['bracketType'] == 'CIRCUIT' or pagestuff['data']['phaseGroup']['phase']['bracketType'] == 'ELIMINATION_ROUNDS':
        return {},{}
    #if pagestuff['data']['phaseGroup']['phase']['bracketType'] == 'ROUND_ROBIN':
        #return {}, {}

    pages = []
    game = URLSPLITS[URLSPLITS.index("event")+1]
    pagenum = 2
    while pagestuff['data']['phaseGroup']['sets']['nodes']!= []:
        pages.append(pagestuff)
        pagestuff = smash.bracket_show_sets_and_event(bracketID,pagenum)
        pagenum = pagenum+1

    pagenum = 1
    standingpages = []
    pagestuff = smash.event_show_lightweight_results_proper(eventID,pagenum)
    pagenum = 2
    while pagestuff['data']['event']['standings']['nodes'] != []:
        standingpages.append(pagestuff)
        pagestuff = smash.event_show_lightweight_results_proper(eventID,pagenum)
        pagenum = pagenum+1

    placementdict = {}
    for page in standingpages:
        for node in page['data']['event']['standings']['nodes']:
            if node['entrant']['name'] not in placementdict:
                placementdict[node['entrant']['name']] = node['placement']




    names = {}
    players = {}
    for page in pages:
        if page['data']['phaseGroup']['phase']['bracketType'] == 'DOUBLE_ELIMINATION' or page['data']['phaseGroup']['phase']['bracketType'] == 'SINGLE_ELIMINATION'or page['data']['phaseGroup']['phase']['bracketType'] == 'ROUND_ROBIN':
            for set in page['data']['phaseGroup']['sets']['nodes']:

                entrant1 = None
                entrant2 = None
                if set['slots'][0]['entrant']:
                    entrant1 = set['slots'][0]['entrant']['name']
                if set['slots'][1]['entrant']:
                    entrant2 = set['slots'][1]['entrant']['name']
                if entrant1 == None:
                    continue
                if entrant2 == None:
                    continue
                if set['slots'][0]['standing']:
                    entrant1score = set['slots'][0]['standing']['stats']['score']['value']
                else:
                    continue
                if set['slots'][1]['standing']:
                    entrant2score = set['slots'][1]['standing']['stats']['score']['value']
                else:
                    continue

                if not entrant1score:
                    entrant1score = 0

                if not entrant2score:
                    entrant2score = 0

                if entrant1score > entrant2score:
                    winner = entrant1
                    loser = entrant2
                    winnerscore = entrant1score
                    loserscore = entrant2score
                elif entrant2score > entrant1score:
                    winner = entrant2
                    loser = entrant1
                    winnerscore = entrant2score
                    loserscore = entrant1score
                elif entrant1score == entrant2score:
                    winner = entrant2
                    loser = entrant1
                    winnerscore = entrant2score
                    loserscore = entrant1score

                if winner not in names:
                    ## (Name:(sets played, sets won, games played, games won, dq's))
                    names[winner] = {}
                    names[winner][game] = 0,0,0,0,0
                if winnerscore == 0:
                    names[winner][game] = names[winner][game][0], names[winner][game][1], names[winner][game][2], names[winner][game][3], \
                    names[winner][game][4]
                else:
                    names[winner][game] = names[winner][game][0] + 1, names[winner][game][1] + 1, names[winner][game][
                        2] + winnerscore + loserscore, names[winner][game][3] + winnerscore, names[winner][game][4]

                if loser not in names:
                    ## (Name:(sets played, sets won, games played, games won, dq's))
                    names[loser] = {}
                    names[loser][game] = 0,0,0,0,0
                if winnerscore == 0:
                    names[loser][game] = names[loser][game][0], names[loser][game][1], names[loser][game][2], names[loser][game][3], \
                    names[loser][game][4]
                else:
                    names[loser][game] = names[loser][game][0] + 1, names[loser][game][1], names[loser][game][
                        2] + winnerscore + loserscore, names[loser][game][3], names[loser][game][4] + loserscore

                if winner not in players:
                    players[winner] = Player()
                players[winner].addOpponentData((loser, winnerscore, loserscore, game))
                players[winner].lastseen = set['completedAt']

                if loser not in players:
                    players[loser] = Player()
                players[loser].addOpponentData((winner, loserscore, winnerscore, game))
                players[loser].lastseen = set['completedAt']

    for player in players:
        players[player].lastplacement = placementdict[player]
    return names, players




def processURLs(BRACKETURLLIST, smash, projectpath,pygame):
    pygame.font.init()
    FONT = pygame.font.Font('SuperMystery.ttf', 16)
    pygame.display.set_caption('PROCESSING URL\'S')
    width = 800
    height = 700
    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    backgroundrect = display.get_rect()

    max = len(BRACKETURLLIST)
    masterplayers = {}
    masternames = {}
    tournamentlist = {}
    lastspotteddict = {}
    current = 0
    skipurls = []
    URLSPLITS = False
    countimage = False
    countstring = False
    game = False
    gamesplit = False
    index = False
    #max = False
    opponent = False
    player = False
    skipfile = False
    tmpdict = False
    tournamentname = False
    url = False

    if exists(projectpath+"\\ProcessedLinks.txt"):
        skipfile = open(projectpath+"\\ProcessedLinks.txt","r")
        skipurl = skipfile.readlines()
        for url in skipurl:
            url = url.removesuffix("\n")
            skipurls.append(url)
        skipfile.close()
        skipfile = open(projectpath+"\\ProcessedLinks.txt","w")

    else:
        skipfile = open(projectpath+"\\ProcessedLinks.txt","w")

    for URL in BRACKETURLLIST:
        if URL in skipurls:
            current = current + 1
            continue

        URLSPLITS = URL.split('/')
        gamesplit = URLSPLITS.index("brackets")
        game = URLSPLITS[gamesplit - 1]
        if "event" in URLSPLITS:
            index = URLSPLITS.index("event") - 1
        elif "events" in URLSPLITS:
            index = URLSPLITS.index("events") - 1
        tournamentname = URLSPLITS[index]

        if URLSPLITS[len(URLSPLITS) - 1] != "brackets":
            urlnames, urlplayers = pullFromBracket(URL,smash)
            if tournamentname not in tournamentlist:
                tournamentlist[tournamentname] = {}
            if game not in tournamentlist[tournamentname]:
                tournamentlist[tournamentname][game] = {}
            if game not in lastspotteddict:
                lastspotteddict[game] = {}

            for name in urlnames:
                if name not in masternames:
                    masternames[name] = {}
                    masternames[name][game] = [0, 0, 0, 0, 0]
                if game not in masternames[name]:
                    masternames[name][game] = [0, 0, 0, 0, 0]
                masternames[name][game] = [masternames[name][game][0] + urlnames[name][game][0], masternames[name][game][
                    1] + urlnames[name][game][1], masternames[name][game][2] + urlnames[name][game][2], \
                                          masternames[name][game][3] + urlnames[name][game][3], masternames[name][game][
                                              4] + urlnames[name][game][4]]
                if name not in tournamentlist[tournamentname][game]:
                    tournamentlist[tournamentname][game][name] = [0, 0, 0, 0, 0]
                tournamentlist[tournamentname][game][name] = [tournamentlist[tournamentname][game][name][0] + \
                                                             urlnames[name][game][0], \
                                                             tournamentlist[tournamentname][game][name][1] + \
                                                             urlnames[name][game][1], \
                                                             tournamentlist[tournamentname][game][name][2] + \
                                                             urlnames[name][game][2], \
                                                             tournamentlist[tournamentname][game][name][3] + \
                                                             urlnames[name][game][3], \
                                                             tournamentlist[tournamentname][game][name][4] + \
                                                             urlnames[name][game][4]]

            for player in urlplayers:
                if player not in masterplayers:
                    masterplayers[player] = urlplayers[player]
                else:
                    if game not in masterplayers[player].opponents:
                        masterplayers[player].opponents[game] = {}
                    for opponent in urlplayers[player].opponents[game]:
                        if opponent not in masterplayers[player].opponents[game]:
                            masterplayers[player].opponents[game][opponent] = [0, 0, 0, 0, 0, 0, 0]
                        masterplayers[player].opponents[game][opponent] = \
                        [masterplayers[player].opponents[game][opponent][0] + \
                        urlplayers[player].opponents[game][opponent][0], \
                        masterplayers[player].opponents[game][opponent][1] + \
                        urlplayers[player].opponents[game][opponent][1], \
                        masterplayers[player].opponents[game][opponent][2] + \
                        urlplayers[player].opponents[game][opponent][2], \
                        masterplayers[player].opponents[game][opponent][3] + \
                        urlplayers[player].opponents[game][opponent][3], \
                        masterplayers[player].opponents[game][opponent][4] + \
                        urlplayers[player].opponents[game][opponent][4], \
                        masterplayers[player].opponents[game][opponent][5] + \
                        urlplayers[player].opponents[game][opponent][5], \
                        masterplayers[player].opponents[game][opponent][6] + \
                        urlplayers[player].opponents[game][opponent][6]]
                if player not in lastspotteddict[game]:
                    tmpdict = urlplayers[player].opponents[game]
                    lastspotteddict[game][player] = tmpdict
                    lastspotteddict[game][player]['TOURNAMENT_NAME'] = tournamentname
                    lastspotteddict[game][player]['TIME_STAMP'] = urlplayers[player].lastseen
                    lastspotteddict[game][player]['PLACEMENT'] = urlplayers[player].lastplacement

                else:
                    if lastspotteddict[game][player]:
                        tmpdict = urlplayers[player].opponents[game]
                        if lastspotteddict[game][player]['TOURNAMENT_NAME'] != tournamentname:
                            if lastspotteddict[game][player]['TIME_STAMP'] < urlplayers[player].lastseen:
                                lastspotteddict[game][player] = tmpdict
                                lastspotteddict[game][player]['TOURNAMENT_NAME'] = tournamentname
                                lastspotteddict[game][player]['TIME_STAMP'] = urlplayers[player].lastseen
                                lastspotteddict[game][player]['PLACEMENT'] = urlplayers[player].lastplacement

        countstring = "Processing " + str(current) + " out of " + str(max)
        print(countstring)
        countimage = FONT.render(countstring, True, (40, 180, 40), (120, 120, 120))

        pygame.draw.rect(display, (0, 0, 0), backgroundrect)
        display.blit(countimage, (10, 10))

        pygame.display.update()
        sleep(10)
        current = current + 1

    for url in BRACKETURLLIST:
        if url in skipurls:
            continue
        else:
            skipurls.append(str(url))
    for url in skipurls:
        skipfile.write(str(url+'\n'))
    skipfile.close()
    del FONT
    del URL
    del URLSPLITS
    del backgroundrect
    del countimage
    del countstring
    del current
    del display
    del game
    del gamesplit
    del height
    del index
    del max
    del opponent
    del player
    del skipfile
    del skipurls
    del tmpdict
    del tournamentname
    del url
    del width
    gc.collect()
    return masternames,masterplayers,tournamentlist, lastspotteddict