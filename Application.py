import jsonpickle
import json
from ChooseEventsPhase import EventChoiceLoop
from GameDataPhase import GameDataPhase
from KeyPhase import getkeyloop
from ProjectPhase import ProjectPhase
from URLPhase import URLPhaseLoop
from pysmashgg import SmashGG
import pygame,sys, gc
from URLProcessing import processURLs
from os import listdir, remove, path, mkdir

from xlsxExporter import exportToxlsx


if getattr(sys, 'frozen', False):
    import pyi_splash

def CombineData(startnames,startplayers,starttournament,addnames,addplayer,addtournament):
    names,players,tournaments = {},{},{}

    for name in addnames:
        if name not in startnames:
            startnames[name] = addnames[name]
        elif name in startnames:
            for game in addnames[name]:
                if game not in startnames[name]:
                    startnames[name][game] = addnames[name][game]
                elif game in startnames[name][game]:
                    startnames[name][game] = [startnames[name][game][0] + addnames[name][game][0],
                                            startnames[name][game][1] + addnames[name][game][1],
                                            startnames[name][game][2] + addnames[name][game][2],
                                            startnames[name][game][3] + addnames[name][game][3],
                                            startnames[name][game][4] + addnames[name][game][4]
                                            ]

    for player in addplayer:
        if player not in startplayers:
            startplayers[player] = addplayer[player]
        elif player in startplayers:
            for game in addplayer[player]['opponents']:
                if game not in startplayers[player]['opponents']:
                    startplayers[player]['opponents'][game] = addplayers[player]['opponents'][game]
                elif game in startplayers[player]['opponents']:
                    for opponent in addplayers[player]['opponents'][game]:
                        if opponent not in startplayers[player]['opponents'][game]:
                            startplayers[player]['opponents'][game][opponent] = addplayers[player]['opponents'][game][opponent]
                        elif opponent in startplayers[player]['opponents'][game]:
                            startplayers[player]['opponents'][game][opponent] = [startplayers[player]['opponents'][game][opponent][0] + startplayers[player]['opponents'][game][opponent][0],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][1] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][1],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][2] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][2],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][3] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][3],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][4] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][4],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][5] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][5],
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][6] +
                                                                                 startplayers[player]['opponents'][
                                                                                     game][opponent][6]
                                                                                 ]

    for tournament in addtournament:
        if tournament not in starttournament:
            starttournament[tournament] = addtournament[tournament]
        elif tournament in starttournament:
            for game in addtournament[tournament]:
                if game not in starttournament[tournament]:
                    starttournament[tournament][game] = addtournament[tournament][game]
                elif game in starttournament[tournament]:
                    for player in addtournament[tournament][game]:
                        if player not in starttournament[tournament][game]:
                            starttournament[tournament][game][player] = addtournament[tournament][game][player]
                        elif player in starttournament[tournament][game]:
                            starttournament[tournament][game][player] = [starttournament[tournament][game][player][0] + addtournament[tournament][game][player][0],
                                                                         starttournament[tournament][game][player][1] +
                                                                         addtournament[tournament][game][player][1],
                                                                         starttournament[tournament][game][player][2] +
                                                                         addtournament[tournament][game][player][2],
                                                                         starttournament[tournament][game][player][3] +
                                                                         addtournament[tournament][game][player][3],
                                                                         starttournament[tournament][game][player][4] +
                                                                         addtournament[tournament][game][player][4]
                                                                         ]

    names = startnames
    players = startplayers
    tournaments = starttournament
    return names,players,tournaments

def MergeRecentLists(OGdict, Adddict):
    mergedict = {}
    for game in Adddict:
        if game in OGdict:
            for player in Adddict[game]:
                if player not in OGdict[game]:
                    OGdict[game][player] = Adddict[game][player]
                elif player in OGdict[game]:
                    if OGdict[game][player]['TIME_STAMP'] < Adddict[game][player]['TIME_STAMP']:
                        OGdict[game][player] = Adddict[game][player]
        else:
            OGdict[game] = Adddict[game]
    mergedict = OGdict
    return mergedict

pygame.init()
if  not path.isdir('.\\lists\\'):
    mkdir('.\\lists\\')
if  not path.isdir('.\\Projects\\'):
    mkdir('.\\Projects\\')
if getattr(sys, 'frozen', False):
    pyi_splash.close()
key = getkeyloop(pygame)
smash = SmashGG(str(key))
projectpath = ProjectPhase(pygame)
filelist = listdir(projectpath)
BaseURLList = URLPhaseLoop(pygame,projectpath)
WorkingURLList = EventChoiceLoop(pygame,BaseURLList,projectpath,smash)
writefile = open(projectpath+"\\urllist.txt","w")
for item in BaseURLList:
    if '\n' not in item:
        item = item +'\n'
    writefile.write(item)
writefile.close()

if 'namesfile.json' in filelist:
    masternames = json.loads(json.load(open(projectpath+ '\\namesfile.json')))
else:
    masternames = {}
if 'playersfile.json' in filelist:
    masterplayers = json.loads(json.load(open(projectpath+'\\playersfile.json')))
else:
    masterplayers = {}
if 'tourneyfile.json' in filelist:
    tournamentlist = json.loads(json.load(open(projectpath+'\\tourneyfile.json')))
else:
    tournamentlist = {}
if 'recentfile.json' in filelist:
    mostrecentlist = json.loads(json.load(open(projectpath+'\\recentfile.json')))
else:
    mostrecentlist = {}

addnames,addplayers,addtournamentlist,addrecent = processURLs(WorkingURLList,smash,projectpath,pygame)

Newnamespickle = jsonpickle.encode(addnames)
Newplayerspickle = jsonpickle.encode(addplayers)
Newtournamentpickle = jsonpickle.encode(addtournamentlist)
Newrecentpickle = jsonpickle.encode(addrecent)
Newnamesfile = open(projectpath +"\\Newnamesfile.json","w")
json.dump(Newnamespickle,Newnamesfile)
Newplayersfile = open(projectpath + '\\Newplayersfile.json','w')
json.dump(Newplayerspickle,Newplayersfile)
Newtourneyfile = open(projectpath +'\\Newtourneyfile.json','w')
json.dump(Newtournamentpickle,Newtourneyfile)
Newrecentfile = open(projectpath+'\\Newrecentfile.json','w')
json.dump(Newrecentpickle,Newrecentfile)
Newnamesfile.close()
Newplayersfile.close()
Newtourneyfile.close()
Newrecentfile.close()

addnames = json.loads(json.load(open(projectpath+ '\\Newnamesfile.json')))
addplayers = json.loads(json.load(open(projectpath+'\\Newplayersfile.json')))
addtournamentlist = json.loads(json.load(open(projectpath+'\\Newtourneyfile.json')))
addrecent = json.loads(json.load(open(projectpath+'\\Newrecentfile.json')))

##Need to implement combining of newly processed recently seen data with previously marked recently seen data
##New recent data *replaces* old recent data

mostrecentlist = MergeRecentLists(mostrecentlist,addrecent)

masternames,masterplayers, tournamentlist = CombineData(masternames,masterplayers,tournamentlist,addnames,addplayers,addtournamentlist)

masternames,masterplayers,tournamentlist,mostrecentlist = GameDataPhase(pygame, masternames, masterplayers,tournamentlist,mostrecentlist)

Newnamespickle = jsonpickle.encode(masternames)
Newplayerspickle = jsonpickle.encode(masterplayers)
Newtournamentpickle = jsonpickle.encode(tournamentlist)
Newrecentpickle = jsonpickle.encode(mostrecentlist)
Newnamesfile = open(projectpath +"\\namesfile.json","w")
json.dump(Newnamespickle,Newnamesfile)
Newplayersfile = open(projectpath + '\\playersfile.json','w')
json.dump(Newplayerspickle,Newplayersfile)
Newtourneyfile = open(projectpath +'\\tourneyfile.json','w')
json.dump(Newtournamentpickle,Newtourneyfile)
Newrecentfile = open(projectpath+'\\recentfile.json','w')
json.dump(Newrecentpickle,Newrecentfile)
Newnamesfile.close()
Newplayersfile.close()
Newtourneyfile.close()
Newrecentfile.close()

addnames = json.loads(json.load(open(projectpath+ '\\Newnamesfile.json')))
addplayers = json.loads(json.load(open(projectpath+'\\Newplayersfile.json')))
addtournamentlist = json.loads(json.load(open(projectpath+'\\Newtourneyfile.json')))
addrecent = json.loads(json.load(open(projectpath+'\\Newrecentfile.json')))

exportToxlsx(masternames,masterplayers,tournamentlist,mostrecentlist,projectpath)

pygame.quit()
del smash
del tournamentlist
writefile.close()
del writefile
del BaseURLList
Newnamesfile.close()
del Newnamesfile
del Newnamespickle
Newplayersfile.close()
del Newplayersfile
del Newplayerspickle
Newrecentfile.close()
del Newrecentfile
del Newrecentpickle
del Newtournamentpickle
Newtourneyfile.close()
del Newtourneyfile
del WorkingURLList
del addnames
del addplayers
del addrecent
del addtournamentlist
del filelist
del item
del key
del listdir
del masternames
del masterplayers
del mostrecentlist
del projectpath
gc.collect()

try:
    sys.exit()
except:
    print('Catch all exceptions')
