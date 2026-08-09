import gc
import sys
import pygame
from pygame import draw, font
from BracketLinkPuller import fetchBracketURLS
from ClickableButton import ClickableOptionButton
from ItemListDisplay import ItemListDisplay, ItemCell
from URLGathering import gatherURLs

def clickcheck(position, item):
    x = position[0]
    y = position[1]
    rect = item.rect
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y+rect.height:
        return True
    return False

def EventChoiceLoop(pygame, INPUTURLLIST, projectpath=False, smash=False):
    pygame.display.set_caption("Pick Which Games You're Keeping")
    font.init()
    FONT = font.Font('SuperMystery.ttf', 14)

    width = 800
    height = 700

    backgroundrect = pygame.rect.Rect(0, 0, width, height)
    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    doneimage = FONT.render("DONE", True, (90, 35, 35), (35, 35, 90))
    DoneButton = ClickableOptionButton(10, 480, doneimage)

    nextimage = FONT.render("NEXT LINK", True, (90, 35, 35), (35, 35, 90))
    NextButton = ClickableOptionButton(DoneButton.rect.x + DoneButton.rect.width + 10, 480, nextimage)

    removeimage = FONT.render("REMOVE", True, (90, 35, 35), (35, 35, 90))
    RemoveButton = ClickableOptionButton(313 - (removeimage.get_rect().width / 2), 265, removeimage)
    RemoveButton.status = False

    keepimage = FONT.render("KEEP", True, (90, 35, 35), (35, 35, 90))
    KeepButton = ClickableOptionButton(313 - (keepimage.get_rect().width / 2), 265, keepimage)
    KeepButton.status = False

    GamesToKeep = ItemListDisplay(25, 70, 200, 400)
    GamesToDrop = ItemListDisplay(425, 70, 200, 400)

    clickableobjectlist = []
    clickableobjectlist.append(GamesToKeep.upButton)
    clickableobjectlist.append(GamesToDrop.upButton)
    clickableobjectlist.append(GamesToKeep.downButton)
    clickableobjectlist.append(GamesToDrop.downButton)
    clickableobjectlist.append(DoneButton)
    clickableobjectlist.append(NextButton)
    clickableobjectlist.append(RemoveButton)
    clickableobjectlist.append(KeepButton)

    done = False
    cutoff = len(INPUTURLLIST)
    listpos = 0

    progresstracker = FONT.render(str(listpos+1)+" out of " + str(cutoff),True,(125, 85, 0),(75, 180, 75))
    activeURL = INPUTURLLIST[listpos]
    activeURLinfo = FONT.render(activeURL,True,(125, 85, 0),(75, 180, 75))
    URLHoldingList = gatherURLs([activeURL],smash)
    OUTPUTURLLIST = []

    EventNameList = []
    for item in URLHoldingList:
        splits = item.split('/')
        seek = splits.index('event')
        name = splits[seek+1]
        if name not in EventNameList:
            EventNameList.append(name)

    GamesToKeep.setitemlist(EventNameList)
    for item in GamesToKeep.buttondict:
        if GamesToKeep.buttondict[item] in clickableobjectlist:
            clickableobjectlist.remove(GamesToKeep.buttondict[item])
    for item in GamesToKeep.buttondict:
        clickableobjectlist.append(GamesToKeep.buttondict[item])



    NametoHold = ""
    activecell = False
    clicked = False
    tmplist = False
    while not done:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                width, height = event.dict['size']
                backgroundrect.width = width
                backgroundrect.height = height
                display = pygame.display.set_mode((width,height),pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                clicked = False
                for clickable in clickableobjectlist:
                    if clickcheck(position, clickable):
                        clicked = clickable
                        if clickable == NextButton:
                            if listpos < cutoff:
                                for item in GamesToKeep.buttondict:
                                    if GamesToKeep.buttondict[item] in clickableobjectlist:
                                        clickableobjectlist.remove(GamesToKeep.buttondict[item])
                                for item in GamesToDrop.buttondict:
                                    if GamesToDrop.buttondict[item] in clickableobjectlist:
                                        clickableobjectlist.remove(GamesToDrop.buttondict[item])

                                tempremovelist = []
                                for item in GamesToDrop.itemlist:
                                    for link in URLHoldingList:
                                        splits = link.split('/')
                                        seek = splits.index('event')
                                        if splits[seek+1] == item:
                                            tempremovelist.append(link)
                                GamesToDrop.setitemlist([])
                                for link in tempremovelist:
                                    URLHoldingList.remove(link)
                                del tempremovelist
                                for item in URLHoldingList:
                                    OUTPUTURLLIST.append(item)
                                listpos = listpos + 1
                                if listpos < cutoff:
                                    activeURL = INPUTURLLIST[listpos]
                                    activeURLinfo = FONT.render(activeURL, True, (125, 85, 0), (75, 180, 75))
                                    progresstracker = FONT.render(str(listpos+1) + " out of " + str(cutoff), True,
                                                                  (125, 85, 0), (75, 180, 75))
                                    URLHoldingList = gatherURLs([activeURL],smash)
                                    EventNameList = []
                                    for item in URLHoldingList:
                                        splits = item.split('/')
                                        seek = splits.index('event')
                                        name = splits[seek + 1]
                                        if name not in EventNameList:
                                            EventNameList.append(name)
                                    GamesToKeep.setitemlist(EventNameList)
                                    for item in GamesToKeep.buttondict:
                                        clickableobjectlist.append(GamesToKeep.buttondict[item])
                                else:
                                    done = True

                        if clickable.__class__ == ItemCell:
                            if activecell:
                                activecell.toggleclicked()
                                for item in GamesToKeep.buttondict:
                                    if GamesToKeep.buttondict[item] == activecell:
                                        activecell.cutoff(GamesToKeep.downButton.rect.x)
                                for item in GamesToDrop.buttondict:
                                    if GamesToDrop.buttondict[item] == activecell:
                                        activecell.cutoff(GamesToDrop.downButton.rect.x)

                            for item in GamesToKeep.buttondict:
                                if GamesToKeep.buttondict[item] == clickable:
                                    RemoveButton.status = True
                                    KeepButton.status = False
                                    activecell = GamesToKeep.buttondict[item]
                                    activecell.toggleclicked()
                            for item in GamesToDrop.buttondict:
                                if GamesToDrop.buttondict[item] == clickable:
                                    RemoveButton.status = False
                                    KeepButton.status = True
                                    activecell = GamesToDrop.buttondict[item]
                                    activecell.toggleclicked()
                            NametoHold = clickable.doclicked()
                        if clickable == RemoveButton:
                            if RemoveButton.status:
                                activecell.toggleclicked()
                                for item in GamesToKeep.buttondict:
                                    if GamesToKeep.buttondict[item] in clickableobjectlist:
                                        clickableobjectlist.remove(GamesToKeep.buttondict[item])
                                for item in GamesToDrop.buttondict:
                                    if GamesToDrop.buttondict[item] in clickableobjectlist:
                                        clickableobjectlist.remove(GamesToDrop.buttondict[item])
                                tmplist = GamesToKeep.itemlist
                                tmplist.remove(NametoHold)
                                GamesToKeep.setitemlist(tmplist)
                                GamesToDrop.additem(NametoHold)
                                for item in GamesToKeep.buttondict:
                                    clickableobjectlist.append(GamesToKeep.buttondict[item])
                                for item in GamesToDrop.buttondict:
                                    clickableobjectlist.append(GamesToDrop.buttondict[item])
                                RemoveButton.status = False
                        if clickable == KeepButton:
                            if KeepButton.status == False:
                                continue
                            activecell.toggleclicked()
                            for item in GamesToKeep.buttondict:
                                if GamesToKeep.buttondict[item] in clickableobjectlist:
                                    clickableobjectlist.remove(GamesToKeep.buttondict[item])
                            for item in GamesToDrop.buttondict:
                                if GamesToDrop.buttondict[item] in clickableobjectlist:
                                    clickableobjectlist.remove(GamesToDrop.buttondict[item])
                            tmplist = GamesToDrop.itemlist
                            tmplist.remove(NametoHold)
                            GamesToDrop.setitemlist(tmplist)
                            GamesToKeep.additem(NametoHold)
                            for item in GamesToKeep.buttondict:
                                clickableobjectlist.append(GamesToKeep.buttondict[item])
                            for item in GamesToDrop.buttondict:
                                clickableobjectlist.append(GamesToDrop.buttondict[item])
                            KeepButton.status = False
                        if clickable == ClickableOptionButton:
                            clickable.doclicked()
                        if clickable == DoneButton:
                            for item in GamesToKeep.buttondict:
                                if GamesToKeep.buttondict[item] in clickableobjectlist:
                                    clickableobjectlist.remove(GamesToKeep.buttondict[item])
                            for item in GamesToDrop.buttondict:
                                if GamesToDrop.buttondict[item] in clickableobjectlist:
                                    clickableobjectlist.remove(GamesToDrop.buttondict[item])

                            tempremovelist = []
                            for item in GamesToDrop.itemlist:
                                for link in URLHoldingList:
                                    splits = link.split('/')
                                    seek = splits.index('event')
                                    if splits[seek + 1] == item:
                                        tempremovelist.append(link)
                            GamesToDrop.setitemlist([])
                            for link in tempremovelist:
                                URLHoldingList.remove(link)
                            del tempremovelist
                            for item in URLHoldingList:
                                OUTPUTURLLIST.append(item)
                            listpos = listpos+1
                            if listpos<cutoff:
                                activeURL = INPUTURLLIST[listpos]
                            done = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                break

        if done:
            break

        draw.rect(display,(0,0,0),backgroundrect)
        display.blit(activeURLinfo,(10,10))
        display.blit(progresstracker,(10,30))
        if RemoveButton.status:
            RemoveButton.draw(display)
        if KeepButton.status:
            KeepButton.draw(display)
        DoneButton.draw(display)
        NextButton.draw(display)
        GamesToKeep.draw(display)
        GamesToDrop.draw(display)
        pygame.display.update()
    linkstoadd = False
    link = False
    while listpos < cutoff:
        linkstoadd = gatherURLs([activeURL],smash)
        for link in linkstoadd:
            OUTPUTURLLIST.append(link)
        listpos = listpos+1
        if listpos < cutoff:
            activeURL = INPUTURLLIST[listpos]
    del DoneButton
    del EventNameList
    del FONT
    del GamesToDrop
    del GamesToKeep
    del INPUTURLLIST
    del KeepButton
    del NametoHold
    del NextButton
    #del OUTPUTURLLIST
    del RemoveButton
    del URLHoldingList
    del activeURL
    del activeURLinfo
    del activecell
    del backgroundrect
    del clickable
    del clickableobjectlist
    del clicked
    del clock
    del cutoff
    del display
    del done
    del doneimage
    del event
    del eventlist
    del height
    del item
    del keepimage
    del link
    del linkstoadd
    del listpos
    del name
    del nextimage
    del position
    del progresstracker
    del projectpath
    del removeimage
    del seek
    del splits
    del tmplist
    del width
    gc.collect()
    return OUTPUTURLLIST





#EventChoiceLoop(pygame,urllist)
