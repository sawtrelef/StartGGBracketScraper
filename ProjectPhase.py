import sys, gc
import pygame
from pygame import draw
import os
from ClickableButton import ClickableOptionButton
from FileStuff import ColorBox
from ItemListDisplay import ItemListDisplay,ItemCell


#def cleanup():
    #del display
    #del clock
    #del done
    #del eventlist
    #del width
    #del height

def clickcheck(position, item):
    x = position[0]
    y = position[1]
    rect = item.rect
    if x >= rect.x and x <= rect.x + rect.width and y >= rect.y and y <= rect.y+rect.height:
        return True
    return False
def ProjectPhase(pygame):
    FONT = pygame.font.Font('SuperMystery.ttf', 14)
    PATH = os.path

    if not PATH.exists('Projects'):
        os.mkdir('Projects')

    width = 800
    height = 700

    backgroundrect = pygame.rect.Rect(0,0,width,height)

    pygame.display.set_caption('Select or Create Project Folder')
    display = pygame.display.set_mode((width,height),pygame.RESIZABLE)
    clock = pygame.time.Clock()

    newimage = FONT.render("NEW PROJECT",True,(90,35,35),(35,35,90))
    NewButton = ClickableOptionButton(10,10, newimage)

    loadimage = FONT.render("LOAD PROJECT",True,(90,35,35),(35,35,90))
    LoadButton = ClickableOptionButton(NewButton.rect.x + NewButton.rect.width +10,10, loadimage)

    ProjectList = ItemListDisplay(10,30, 300, 400)
    projectlist = os.listdir('.\\Projects')
    ProjectList.setitemlist(projectlist)

    projectnamebox = ColorBox()
    projectnamebox.background = (80,25,80)
    projectnamebox.rect.x = LoadButton.rect.width + 20 + LoadButton.rect.x
    projectnamebox.rect.y = LoadButton.rect.y
    projectnamebox.updatetext('')

    createprojectimage = FONT.render("CREATE PROJECT", True, (35,95,35),(200,35,90))
    CreateProjectButton = ClickableOptionButton(projectnamebox.rect.x + projectnamebox.rect.width + 10,10,createprojectimage)
    CreateProjectButton.status = False

    clickableobjectlist = []
    drawlist = []
    clickableobjectlist.append(NewButton)
    clickableobjectlist.append(LoadButton)
    clickableobjectlist.append(projectnamebox)
    clickableobjectlist.append(CreateProjectButton)
    ID = False
    for ID in ProjectList.buttondict:
        clickableobjectlist.append(ProjectList.buttondict[ID])
    drawlist.append(NewButton)
    drawlist.append(LoadButton)
    drawlist.append(ProjectList)
    drawlist.append(projectnamebox)
    #drawlist.append(CreateProjectButton)


    done = False
    ActiveCell = False
    projectpath = ""
    clicked = False
    position = False
    clickable = False
    while not done:

        eventlist = pygame.event.get()

        for event in eventlist:
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                width, height = event.dict['size']
                backgroundrect.width = width
                backgroundrect.height = height
                display = pygame.display.set_mode((width,height),pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = False
                for clickable in clickableobjectlist:
                    if clickcheck(position, clickable):
                        clicked = clickable
                        if clicked.__class__ == ItemCell:
                            if projectnamebox.status == True:
                                projectnamebox.toggle()
                                CreateProjectButton.status = False
                            if ActiveCell:
                                ActiveCell.toggleclicked()
                            ActiveCell = clicked
                            ActiveCell.toggleclicked()
                        elif clicked == LoadButton:
                            if ActiveCell.__class__ == ItemCell:
                                projectpath = '.\\Projects\\' + str(ActiveCell.item)
                                done = True
                        elif clicked == NewButton:
                            if ActiveCell:
                                ActiveCell.toggleclicked()
                                ActiveCell = False
                            projectnamebox.updatetext(" ")
                            CreateProjectButton.rect.x = projectnamebox.rect.x + projectnamebox.rect.width + 10
                            projectnamebox.toggle()
                            CreateProjectButton.status = True
                        elif clicked == CreateProjectButton:
                            if CreateProjectButton.status == True:
                                projectname = projectnamebox.text
                                if projectname != " ":
                                    projectpath = '.\\Projects\\'+str(projectname)
                                    if projectname not in projectlist:
                                        os.mkdir(projectpath)
                                    done = True
                        elif clicked == projectnamebox:
                            if ActiveCell:
                                ActiveCell.toggleclicked()
                                ActiveCell = False
                            CreateProjectButton.status = True
                            projectnamebox.toggle()
                        elif clickable == ClickableOptionButton:
                            clickable.doclicked()
                break
            if event.type == pygame.KEYUP:
                if projectnamebox.status:
                    keypress = event.unicode
                    if keypress != '\x08':
                        if projectnamebox.text == " " or projectnamebox.text == '    ':
                            projectnamebox.updatetext("")
                        projectnamebox.updatetext(projectnamebox.text + str(keypress))
                        CreateProjectButton.rect.x = projectnamebox.rect.x + projectnamebox.rect.width + 10
                    if keypress == '\x08':
                        newtext = projectnamebox.text[:-1]
                        if newtext == '':
                            newtext = " "
                        projectnamebox.updatetext(newtext)
                        CreateProjectButton.rect.x = projectnamebox.rect.x + projectnamebox.rect.width + 10
        if done:
            break

        draw.rect(display,(0,0,0),backgroundrect)
        for drawitem in drawlist:
            drawitem.draw(display)
        if CreateProjectButton.status:
            CreateProjectButton.draw(display)
        pygame.display.update()
    del ActiveCell
    del CreateProjectButton
    del FONT
    del ID
    del LoadButton
    del NewButton
    del ProjectList
    del backgroundrect
    del clickableobjectlist
    del clicked
    del clock
    del createprojectimage
    del display
    del done
    del drawitem
    del drawlist
    del event
    del eventlist
    del height
    del loadimage
    del newimage
    del position
    del projectlist
    del projectnamebox
    del width
    del clickable
    gc.collect()
    return projectpath