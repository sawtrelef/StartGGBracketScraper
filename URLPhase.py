import gc
import pygame, sys
import os
from pygame import font
from ClickableButton import ClickableOptionButton
from ItemListDisplay import ItemListDisplay, ItemCell
from FileStuff import FileWindow, FileBox, ColorBox
import pyperclip
from os import path

def loadclicked(self):
    return "./lists/"+self.text

def LoadButtonDoClicked(position,filewindow):
    if path.isdir('.\\lists\\'):
        itemlist = filewindow.UpdateSelf("./lists/",(position[0],position[1]))
        for item in itemlist:
            item.clickdummy = loadclicked

    return itemlist

def clickcheck(position, item):
    x = position[0]
    y = position[1]
    rect = item.rect
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y+rect.height:
        return True
    return False



def LoadFromFile(filepath,ListDisplay):
    file = open(filepath, 'r')
    lines = file.readlines()
    ListDisplay.setitemlist(lines)
    file.close()


def URLPhaseLoop(pygame,projectpath=False):
    font.init()
    FONT = font.Font('SuperMystery.ttf', 16)
    pygame.display.set_caption('Gather URL\'s')
    width = 800
    height = 700
    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    # display.blit(SourceImage,(X,Y))
    clock = pygame.time.Clock()
    filewindow = FileWindow()

    loadtext = FONT.render("Load From File", True, (90, 35, 35), (35, 35, 90))
    LoadListButton = ClickableOptionButton(5, 5, loadtext)

    LoadListButton.doclicked = LoadButtonDoClicked

    pastebuttonimage = FONT.render("Paste", True, (90, 35, 35), (35, 35, 90))
    PasteButton = ClickableOptionButton(LoadListButton.rect.x + LoadListButton.rect.width + 10, LoadListButton.rect.y,
                                        pastebuttonimage)

    enterbuttonimage = FONT.render("Enter", True, (90, 35, 35), (35, 35, 90))
    EnterButton = ClickableOptionButton(PasteButton.rect.x + PasteButton.rect.width + 10, PasteButton.rect.y,
                                        enterbuttonimage)

    AddLinkTextBar = ColorBox()
    AddLinkTextBar.background = (80, 25, 80)
    AddLinkTextBar.updatetext("Add Link Here")
    AddLinkTextBar.rect.x = EnterButton.rect.x + EnterButton.rect.width + 10
    AddLinkTextBar.rect.y = EnterButton.rect.y

    URLListDisplay = ItemListDisplay(20, 30, 300, 500)

    removeimage = FONT.render("REMOVE", True, (120, 50, 50), (35, 35, 90))
    RemoveButton = ClickableOptionButton(URLListDisplay.rect.x, URLListDisplay.rect.y + URLListDisplay.rect.height + 10,
                                         removeimage)

    doneimage = FONT.render("DONE", True, (90, 35, 35), (35, 35, 90))
    DoneButton = ClickableOptionButton(RemoveButton.rect.x + RemoveButton.rect.width + 10,
                                       URLListDisplay.rect.y + URLListDisplay.rect.height + 10, doneimage)

    clickableobjectlist = []
    clickableobjectlist.append(URLListDisplay.upButton)
    clickableobjectlist.append(URLListDisplay.downButton)
    clickableobjectlist.append(LoadListButton)
    clickableobjectlist.append(AddLinkTextBar)
    clickableobjectlist.append(PasteButton)
    clickableobjectlist.append(EnterButton)
    clickableobjectlist.append(DoneButton)
    clickableobjectlist.append(RemoveButton)
    backgroundrect = display.get_rect()
    width = backgroundrect.width
    height = backgroundrect.height
    done = False
    activecell = False
    urllist = []

    if projectpath != False:
        filelist = os.listdir(projectpath)
        if 'urllist.txt' in filelist:
            file = open (projectpath+'\\urllist.txt','r')
            urllist = file.readlines()
            file.close()
        URLListDisplay.setitemlist(urllist)
        for button in URLListDisplay.buttondict:
            clickableobjectlist.append(URLListDisplay.buttondict[button])

    eventlist = pygame.event.get()
    while not done:
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = False
                position = pygame.mouse.get_pos()
                check = False
                filewindow.state = False
                for clickable in clickableobjectlist:
                    if clickcheck(position,clickable):
                        clicked = clickable
                        if clickable == LoadListButton:
                            check = clickable.doclicked(position,filewindow)
                            if check.__class__ == dict:
                                for item in check:
                                    clickableobjectlist.append(item)
                        elif clickable.__class__ == FileBox:
                            check = clickable.doclicked()
                            LoadFromFile(check,URLListDisplay)

                        elif clickable == AddLinkTextBar:
                            if AddLinkTextBar.text == "Add Link Here":
                                AddLinkTextBar.updatetext(" ")
                            AddLinkTextBar.toggle()

                        elif clickable == PasteButton:
                            text = pyperclip.paste()
                            AddLinkTextBar.updatetext(text)
                            break
                        elif clickable == EnterButton:
                            if AddLinkTextBar.text != "Add Link Here":
                                for button in URLListDisplay.buttondict:
                                    if URLListDisplay.buttondict[button] in clickableobjectlist:
                                        clickableobjectlist.remove(URLListDisplay.buttondict[button])
                                URLListDisplay.additem(AddLinkTextBar.text)
                                AddLinkTextBar.updatetext("Add Link Here")
                                for button in URLListDisplay.buttondict:
                                    clickableobjectlist.append(URLListDisplay.buttondict[button])
                        elif clickable == DoneButton:
                            done = True
                        elif clickable == RemoveButton:
                            if activecell:
                                for button in URLListDisplay.buttondict:
                                    if URLListDisplay.buttondict[button] in clickableobjectlist:
                                        clickableobjectlist.remove(URLListDisplay.buttondict[button])
                                URLListDisplay.itemlist.remove(activecell.item)
                                URLListDisplay.setitemlist(URLListDisplay.itemlist)
                                for button in URLListDisplay.buttondict:
                                    clickableobjectlist.append(URLListDisplay.buttondict[button])
                        elif clickable.__class__ == ItemCell:
                            if activecell:
                                activecell.toggleclicked()
                                activecell.cutoff(URLListDisplay.downButton.rect.x)
                                for item in URLListDisplay.buttondict:
                                    if URLListDisplay.buttondict[item] == clickable:
                                        activecell = URLListDisplay.buttondict[item]
                                        activecell.toggleclicked()
                            else:
                                for item in URLListDisplay.buttondict:
                                    if URLListDisplay.buttondict[item] == clickable:
                                        activecell = URLListDisplay.buttondict[item]
                                        activecell.toggleclicked()

                        elif clickable.__class__ == ClickableOptionButton:
                            check = clickable.doclicked()

                        if clickable != AddLinkTextBar:
                            if AddLinkTextBar.status:
                                AddLinkTextBar.toggle()
                        break

                if clicked != PasteButton and clicked != AddLinkTextBar:
                    if AddLinkTextBar.status:
                        AddLinkTextBar.toggle()
                if check.__class__ != dict:
                    for item in filewindow.itemdict:
                        for thing in clickableobjectlist:
                            if thing == item:
                                clickableobjectlist.remove(item)
                    break
            if event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.dict['size']
                backgroundrect.width = newWidth
                backgroundrect.height = newHeight
                width = newWidth
                height = newHeight
                display = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

            if event.type == pygame.KEYUP:
                if AddLinkTextBar.status == True:
                    keypress = event.unicode
                    AddLinkTextBar.addtotext(keypress)
            if done:
                break
        #print("in gather url phase")
        pygame.draw.rect(display, (0, 0, 0), backgroundrect)
        URLListDisplay.draw(display)
        LoadListButton.draw(display)
        AddLinkTextBar.draw(display)
        PasteButton.draw(display)
        EnterButton.draw(display)
        DoneButton.draw(display)
        RemoveButton.draw(display)
        filewindow.draw(display)
        pygame.display.update()

    urllist = URLListDisplay.itemlist
    del AddLinkTextBar
    del DoneButton
    del EnterButton
    del FONT
    del LoadListButton
    del PasteButton
    del RemoveButton
    del URLListDisplay
    del activecell
    del backgroundrect
    del button
    del check
    del clickable
    del clickableobjectlist
    del clicked
    del clock
    del display
    del done
    del doneimage
    del enterbuttonimage
    del event
    del eventlist
    file.close()
    del file
    del filelist
    del height
    del loadtext
    del pastebuttonimage
    del position
    del removeimage
    del width
    del filewindow
    gc.collect()
    return urllist