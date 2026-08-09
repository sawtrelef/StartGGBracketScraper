import gc
import sys
import pygame
import json
import jsonpickle
import pathlib
from pygame import font
from pysmashgg import SmashGG

from ItemListDisplay import ItemListDisplay,ItemCell
from URLGathering import gatherURLs
from URLProcessing import processURLs
from ClickableButton import ClickableOptionButton
from xlsxExporter import exportToxlsx
from URLGathering import gatherURLs

class MergeButton(ClickableOptionButton):
    def __init__(self,FONT):
        self.textbox = FONT.render("MERGE NOW",True,(255,0,0),(0,140,140))
        super().__init__(300, 500,self.textbox)
        self.activestate = False

    def activecheck(self,stringstocheck):
        self.activestate = True
        for item in stringstocheck:
            if item == "":
                self.activestate = False

    def draw(self,WINDOW):
        if self.activestate:
            super().draw(WINDOW)

    def doclicked(self):
        if self.activestate:
            print("I Was Here")
        return self
def Merge(GametoRemove, GameInto, namedict, playerdict, tourneydict,mostrecentlist):
    changelist = []
    for tourney in tourneydict:
        for game in tourneydict[tourney]:
            if game == GametoRemove:
                tmpdict = tourneydict[tourney][game]
                changelist.append((tourney,tmpdict))

    for item in changelist:
        del tourneydict[item[0]][GametoRemove]
        tourneydict[item[0]][GameInto] = item[1]

    for player in playerdict:
        if GametoRemove in playerdict[player]['opponents']:
            if GameInto not in playerdict[player]['opponents']:
                playerdict[player]['opponents'][GameInto] = {}
            for opponent in playerdict[player]['opponents'][GametoRemove]:
                if opponent not in playerdict[player]['opponents'][GameInto]:
                    playerdict[player]['opponents'][GameInto][opponent] = playerdict[player]['opponents'][GametoRemove][opponent]
                else:
                    playerdict[player]['opponents'][GameInto][opponent] = [playerdict[player]['opponents'][GameInto][opponent][0]+playerdict[player]['opponents'][GametoRemove][opponent][0],
                                                                            playerdict[player]['opponents'][
                                                                               GameInto][opponent][1] +
                                                                            playerdict[player]['opponents'][
                                                                                GametoRemove][opponent][1],
                                                                            playerdict[player]['opponents'][
                                                                               GameInto][opponent][2] +
                                                                            playerdict[player]['opponents'][
                                                                                GametoRemove][opponent][2],
                                                                            playerdict[player]['opponents'][
                                                                                GameInto][opponent][3] +
                                                                            playerdict[player]['opponents'][
                                                                               GametoRemove][opponent][3],
                                                                            playerdict[player]['opponents'][
                                                                               GameInto][opponent][4] +
                                                                            playerdict[player]['opponents'][
                                                                               GametoRemove][opponent][4],
                                                                            playerdict[player]['opponents'][
                                                                               GameInto][opponent][5] +
                                                                            playerdict[player]['opponents'][
                                                                               GametoRemove][opponent][5],
                                                                            playerdict[player]['opponents'][
                                                                               GameInto][opponent][6] +
                                                                            playerdict[player]['opponents'][
                                                                               GametoRemove][opponent][6]
                                                                            ]
            del playerdict[player]['opponents'][GametoRemove]

    for player in namedict:
        if GametoRemove in namedict[player]:
            if GameInto not in namedict[player]:
                namedict[player][GameInto] = namedict[player][GametoRemove]
            else:
                namedict[player][GameInto] = [namedict[player][GameInto][0]+namedict[player][GametoRemove][0],
                    namedict[player][GameInto][1]+namedict[player][GametoRemove][1],
                    namedict[player][GameInto][2]+namedict[player][GametoRemove][2],
                    namedict[player][GameInto][3]+namedict[player][GametoRemove][3],
                    namedict[player][GameInto][4] + namedict[player][GametoRemove][4]
                ]
            del namedict[player][GametoRemove]

    if GametoRemove in mostrecentlist:
        if GameInto in mostrecentlist:
            for player in mostrecentlist[GametoRemove]:
                if player in mostrecentlist[GameInto]:
                    if mostrecentlist[GameInto][player]['TIME_STAMP'] < mostrecentlist[GametoRemove][player]['TIME_STAMP']:
                        mostrecentlist[GameInto][player] = mostrecentlist[GametoRemove][player]
                else:
                    mostrecentlist[GameInto][player] = mostrecentlist[GametoRemove][player]
        else:
            mostrecentlist[GameInto] = mostrecentlist[GametoRemove]

    del mostrecentlist[GametoRemove]

    return namedict, playerdict, tourneydict, mostrecentlist


##GATHERURLS
#smash = SmashGG("6224ab77ef2169b2e55b6c5621e9bb3b")
#URLLIST = gatherURLs(smash=smash)
#masternames,masterplayers,tournamentlist = processURLs(URLLIST,smash)

#namespickle = jsonpickle.encode(masternames)
#playerspickle = jsonpickle.encode(masterplayers)
#tournamentpickle = jsonpickle.encode(tournamentlist)

#namesfile = open("namesfile.json","w")
#json.dump(namespickle,namesfile)
#namesfile.close()
#playersfile = open('playersfile.json','w')
#json.dump(playerspickle,playersfile)
#playersfile.close()
#tourneyfile = open('tourneyfile.json','w')
#json.dump(tournamentpickle,tourneyfile)

#namesfile.close()
#playersfile.close()
#tourneyfile.close()

#masternames = json.loads(json.load(open('namesfile.json')))
#masterplayers = json.loads(json.load(open('playersfile.json')))
#tournamentlist = json.loads(json.load(open('tourneyfile.json')))

#gamenamelist = ['melee-singles','ultimate-singles','melee-dubz','ultimate-dubz','sf6-1v1', 'melee-singles-1v1','ultimate-singles-1v1', 'mario-kart','godzilla','bingo','blackjack','Slay The Spire', 'Spyro', 'Jak and Daxter', 'rugrats', 'skul', 'counter-strike', 'Marvel', 'Tetris', 'Puyo', 'golf', 'Basketball', 'Downhill Standing']

#for tournament in tournamentlist:
#    for game in tournamentlist[tournament]:
#        if game not in gamenamelist:
#            gamenamelist.append(game)



def clickcheck(position, item):
    x = position[0]
    y = position[1]
    rect = item.rect
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y+rect.height:
        return True
    return False
def GameDataPhase(pygame, masternames, masterplayers,tournamentlist, mostrecentlist):
    font.init()
    FONT = font.Font('SuperMystery.ttf', 16)

    mergeButton = MergeButton(FONT)
    mergeButton.doclicked = Merge

    exportbuttonimage = FONT.render("BEGIN EXPORT",True,(0,0,0),(200,50,50))
    ExportButton = ClickableOptionButton(20,600,exportbuttonimage)

    ITEMTOCHANGE = ""
    ITEMTOBECOME = ""

    pygame.display.set_caption('Bracket to Excel compiler')
    width = 800
    height = 700
    display = pygame.display.set_mode((width,height),pygame.RESIZABLE)
    #display.blit(SourceImage,(X,Y))
    clock = pygame.time.Clock()

    backgroundrect = pygame.rect.Rect(0,0,width,height)

    GameNameDisplay = ItemListDisplay(25,25,200,400)

    gamenamelist = []
    for tournament in tournamentlist:
        for item in tournamentlist[tournament]:
            if item not in gamenamelist:
                gamenamelist.append(item)
    for game in mostrecentlist:
        if game not in gamenamelist:
            gamenamelist.append(game)

    GameNameDisplay.setitemlist(gamenamelist)
    MergeNameDisplay = ItemListDisplay(500,25,200,400)
    OutPutButtonList = []
    secondtablebuttonlist = []
    for item in GameNameDisplay.buttondict:
        OutPutButtonList.append(GameNameDisplay.buttondict[item])

    clickableobjectlist = []
    clickableobjectlist.append(GameNameDisplay.upButton)
    clickableobjectlist.append(GameNameDisplay.downButton)
    clickableobjectlist.append(MergeNameDisplay.upButton)
    clickableobjectlist.append(MergeNameDisplay.downButton)
    clickableobjectlist.append(mergeButton)
    clickableobjectlist.append(ExportButton)
    for item in GameNameDisplay.buttondict:
        clickableobjectlist.append(GameNameDisplay.buttondict[item])

    done = False
    tmplist = False
    button = False
    gameName = False
    while not done:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.dict['size']
                backgroundrect.width = newWidth
                backgroundrect.height = newHeight
                width = newWidth
                height = newHeight
                display = pygame.display.set_mode((newWidth,newHeight),pygame.RESIZABLE)
            #HANDLES WHEN MOUSE IS CLICKED
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for item in clickableobjectlist:
                    if clickcheck(position,item):
                        if item in OutPutButtonList:
                            gameName = item.doclicked()
                            tmplist = GameNameDisplay.itemlist.copy()
                            tmplist.remove(gameName)
                            ITEMTOCHANGE = str(gameName)
                            ITEMTOBECOME = ""
                            for item in MergeNameDisplay.buttondict:
                                clickableobjectlist.remove(MergeNameDisplay.buttondict[item])
                                secondtablebuttonlist.remove(MergeNameDisplay.buttondict[item])
                            MergeNameDisplay.setitemlist(tmplist)
                            for item in MergeNameDisplay.buttondict:
                                clickableobjectlist.append(MergeNameDisplay.buttondict[item])
                                secondtablebuttonlist.append(MergeNameDisplay.buttondict[item])
                        elif item in secondtablebuttonlist:
                            gameName = item.doclicked()
                            ITEMTOBECOME = str(gameName)
                        elif item == mergeButton:
                            if item.activestate:
                                masternames,masterplayers,tournamentlist,mostrecentlist = item.doclicked(ITEMTOCHANGE,ITEMTOBECOME,masternames,masterplayers,tournamentlist,mostrecentlist)
                                for button in GameNameDisplay.buttondict:
                                    if GameNameDisplay.buttondict[button] in clickableobjectlist:
                                        clickableobjectlist.remove(GameNameDisplay.buttondict[button])
                                    if GameNameDisplay.buttondict[button] in OutPutButtonList:
                                        OutPutButtonList.remove(GameNameDisplay.buttondict[button])
                                gamenamelist.remove(ITEMTOCHANGE)
                                GameNameDisplay.setitemlist(gamenamelist)
                                for button in OutPutButtonList:
                                    if button.item == ITEMTOCHANGE:
                                        OutPutButtonList.remove(button)
                                for button in GameNameDisplay.buttondict:
                                    clickableobjectlist.append(GameNameDisplay.buttondict[button])
                                    OutPutButtonList.append(GameNameDisplay.buttondict[button])
                                ITEMTOCHANGE = ""
                                ITEMTOBECOME = ""
                                item.activestate == False
                        elif item == ExportButton:
                            done = True


        if done:
            break

        ##THIS SHOULD ALWAYS BE THE FINAL BEFORE DRAWING

        itemtochangetextbox = FONT.render(ITEMTOCHANGE,True, (0,0,140))
        changetotextbox = FONT.render(ITEMTOBECOME, True, (140,0,0))
        middletextbox = FONT.render("-- WILL MERGE INTO ->", True, (0,140,0))

        pygame.draw.rect(display, (0, 0, 0), backgroundrect)

        mergeButton.activecheck([ITEMTOBECOME,ITEMTOCHANGE])
        mergeButton.draw(display)
        GameNameDisplay.draw(display)
        MergeNameDisplay.draw(display)
        ExportButton.draw(display)
        display.blit(itemtochangetextbox,(25,450))
        display.blit(middletextbox,(250, 475))
        display.blit(changetotextbox,(475,450))
        pygame.display.update()

    del ExportButton
    del FONT
    del GameNameDisplay
    del ITEMTOBECOME
    del ITEMTOCHANGE
    del MergeNameDisplay
    del OutPutButtonList
    del backgroundrect
    del button
    del changetotextbox
    del clickableobjectlist
    del clock
    del display
    del done
    del event
    del eventlist
    del exportbuttonimage
    del game
    del gameName
    del gamenamelist
    del height
    del item
    del itemtochangetextbox
    del mergeButton
    del middletextbox
    del position
    del secondtablebuttonlist
    del tmplist
    del tournament
    del width
    gc.collect()
    return masternames, masterplayers, tournamentlist, mostrecentlist


#exportToxlsx(masternames,masterplayers,tournamentlist)
#font.quit()
#pygame.quit()
#cleanup()
