from pysmashgg import SmashGG
import requests

def fetchBracketURLS(seedURL,smash):
    URLSPLITS = seedURL.split('/')

    EVENTNAME = URLSPLITS[URLSPLITS.index("tournament")+1]

    bracketlinklist = []

    stuff = smash.tournament_phase_and_phasegroup(EVENTNAME)
    gamelist = stuff['data']['tournament']['events']
    for game in gamelist:
        gamename = game['name']
        phases = game['phases']
        slug = game['slug']
        gamenameclean = gamename.lower()
        gamenameclean = gamenameclean.replace(' ','-')
        for item in ['[', ']', ':', '*', '?', '/', '\\','(',')',',','!','.']:
            if item in gamenameclean:

                if item == ':':
                    itemindex = gamenameclean.index(':')
                    index2 = -1
                    index3 = -1
                    if itemindex - 1 >= 0:
                        index2 = itemindex-1
                    if itemindex + 1 < len(gamenameclean):
                        index3 = itemindex+1
                    if index2 > -1 and index3 > -1:
                        if (gamenameclean[index2] != ' ' and gamenameclean[index2] != '-') and (gamenameclean[index3] != ' ' and gamenameclean[index3] != '-'):
                            gamenameclean = gamenameclean.replace(item,'-')

                gamenameclean = gamenameclean.replace(item, '')


        for phase in phases:
            phaseID = str(phase['id'])
            phaseGroups = phase['phaseGroups']
            for node in phaseGroups['nodes']:
                bracketID = str(node['id'])
                linktoadd = 'https://www.start.gg/'+slug+'/'+'brackets'+'/'+phaseID+'/'+bracketID
                bracketlinklist.append(linktoadd)



    return bracketlinklist