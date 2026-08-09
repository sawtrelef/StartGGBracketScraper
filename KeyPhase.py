import gc
import sys
import pygame
from os import listdir
from pygame import draw, font
from ClickableButton import ClickableOptionButton
from FileStuff import ColorBox
import pyperclip
'''font.init()

FONT = font.Font('SuperMystery.ttf', 14)

width = 800
height = 700

backgroundrect =  pygame.rect.Rect(0,0,width,height)

pygame.display.set_caption('Got yo keys?')
display = pygame.display.set_mode((width,height),pygame.RESIZABLE)
clock = pygame.time.Clock()


filelist = listdir('./')

infotext = FONT.render("PLEASE PROVIDE YOUR API KEY BELOW",True,(125, 85, 0),(75, 180, 75))
infotext2 = FONT.render("To obtain your *personal key*, check the developer settings tab on start.gg", True, (125, 85, 0),(75, 180, 75))


pastebuttonimage = FONT.render("Paste",True,(90,35,35),(35,35,90))
PasteButton = ClickableOptionButton(10,50,pastebuttonimage)

doneimage = FONT.render("DONE",True,(90,35,35),(35,35,90))
DoneButton = ClickableOptionButton(10,70, doneimage)

keybox = ColorBox()
keybox.background = (80,25,80)
keybox.rect.x = PasteButton.rect.width + 20
keybox.rect.y = 50
keybox.updatetext('    ')


if 'key' in filelist:
    file = open('key')
    lines = file.readlines()
    if lines != '':
        key = lines
        done = True

clickableobjectlist = []
clickableobjectlist.append(keybox)
clickableobjectlist.append(PasteButton)
clickableobjectlist.append(DoneButton)
'''

def clickcheck(position, item):
    x = position[0]
    y = position[1]
    rect = item.rect
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y+rect.height:
        return True
    return False

def getkeyloop(pygame):
    font.init()

    FONT = font.Font('SuperMystery.ttf', 14)

    width = 800
    height = 700

    backgroundrect = pygame.rect.Rect(0, 0, width, height)

    pygame.display.set_caption('Got yo keys?')
    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    filelist = listdir('./')

    infotext = FONT.render("PLEASE PROVIDE YOUR API KEY BELOW", True, (125, 85, 0), (75, 180, 75))
    infotext2 = FONT.render("To obtain your *personal key*, check the developer settings tab on start.gg", True,
                            (125, 85, 0), (75, 180, 75))

    pastebuttonimage = FONT.render("Paste", True, (90, 35, 35), (35, 35, 90))
    PasteButton = ClickableOptionButton(10, 50, pastebuttonimage)

    doneimage = FONT.render("DONE", True, (90, 35, 35), (35, 35, 90))
    DoneButton = ClickableOptionButton(10, 70, doneimage)

    keybox = ColorBox()
    keybox.background = (80, 25, 80)
    keybox.rect.x = PasteButton.rect.width + 20
    keybox.rect.y = 50
    keybox.updatetext('    ')

    if 'key' in filelist:
        file = open('key')
        lines = file.readlines()
        if lines != '':
            key = lines
            done = True

    clickableobjectlist = []
    clickableobjectlist.append(keybox)
    clickableobjectlist.append(PasteButton)
    clickableobjectlist.append(DoneButton)

    done = False
    if 'key' in filelist:
        file = open('key')
        lines = file.readlines()
        if lines != '':
            key = lines[0]
            done = True
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
                for item in clickableobjectlist:
                    if clickcheck(position, item):
                        clicked = item
                        if item == keybox:
                            if keybox.text == '    ':
                                keybox.updatetext(" ")
                            keybox.toggle()
                        elif item == PasteButton:
                            text = pyperclip.paste()
                            keybox.updatetext(text)
                            break
                        if item == DoneButton:
                            if keybox.text != '    ' and keybox.text != " ":
                                done = True
                                f = open('key', "w", encoding="utf-8")
                                key = keybox.text
                                f.write(str(key))
                                f.close()

                if clicked != PasteButton and clicked != keybox:
                    if keybox.status:
                        keybox.toggle()
            if event.type == pygame.KEYUP:
                if keybox.status:
                    keypress = event.unicode
                    if keybox.text == " " or keybox.text == '    ':
                        keybox.updatetext("")
                    keybox.addtotext(keypress)
            if done:
                break

        draw.rect(display,(0,0,0),backgroundrect)
        display.blit(infotext, (10, 10))
        display.blit(infotext2, (10, 30))
        keybox.draw(display)
        PasteButton.draw(display)
        DoneButton.draw(display)
        pygame.display.update()

    del DoneButton
    del FONT
    del PasteButton
    del backgroundrect
    del clickableobjectlist
    del clock
    del doneimage
    file.close()
    del file
    del height
    del infotext
    del infotext2
    del keybox
    del pastebuttonimage
    del width
    gc.collect()
    return key
#cleanup()