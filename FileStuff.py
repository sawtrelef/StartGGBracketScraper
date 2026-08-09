from os import listdir
from pygame import draw, font




font.init()
FONT = font.Font('SuperMystery.ttf', 14)

class ColorBox():
    rect = False
    textitem = False
    text = ""
    colors = {False: (80,25,80), True: (70,110,70), "Text":(240,120,80)}

    def __init__(self):

        self.text = "#rrggbb"
        self.background = (0,0,0)
        self.textitem = FONT.render(self.text, True,self.colors["Text"], self.background)
        self.rect = self.textitem.get_rect()
        self.status = False
        self.spacecheck = False


    ##THIS IS ABSOLUTELY GENIUS RIGHT HERE
    ##I DON'T KNOW THE OFFICIAL NAME OF THIS PATTERN
    ##I'M CALLING IT THE DOUBLE DUMMY PATTERN

    def doclicked(self):
        return self

    def toggle(self):
        self.status = not self.status
        self.background = self.colors[self.status]
        self.updatetext(self.text)


    def updatetext(self, new):
        self.text = new
        self.textitem = FONT.render(self.text,True,self.colors["Text"], self.background)
        rect = self.textitem.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect

    def addtotext(self, new):
        if new == '\x08':
            self.text = self.text[0:-1]
            if self.text == '':
                self.text = ' '
                self.spacecheck = False
        elif new =='\r':
            print("ok")
        else:
            if self.text == ' ':
                if new == ' ':
                    if self.spacecheck == True:
                        self.text = self.text + str(new)
                        self.spacecheck = True
                    else:
                        self.spacecheck = True
                else:
                    if self.spacecheck == True:
                        self.text = self.text + str(new)
                    else:
                        self.text = str(new)
            else:
                self.text = self.text + str(new)


        self.updatetext(self.text)

    def draw(self,WINDOW):
        WINDOW.blit(self.textitem,self.rect)

class FileBox():
    rect = False
    textitem = False
    text = ""


    def __init__(self, textitem,rect,text):

        self.rect = rect
        self.textitem = textitem
        self.text = text



    ##THIS IS ABSOLUTELY GENIUS RIGHT HERE
    ##I DON'T KNOW THE OFFICIAL NAME OF THIS PATTERN
    ##I'M CALLING IT THE DOUBLE DUMMY PATTERN
    def clickdummy(self,item):
        return

    def doclicked(self):
        dummy = self.clickdummy(self)
        return dummy

    def updatetext(self, new):
        self.text = new
        self.textitem = FONT.render(self.text,True,(75,200,200))
        rect = self.textitem.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect

class FileWindow():
    xpos = 0
    ypos = 0
    height = 0
    width = 0
    state = False
    itemdict = {}

    mode = False
    def __init__(self):
        return

    def update(self):
        biggest = 0
        for item in self.itemdict:
            if item.rect.width > biggest:
               biggest = item.rect.width
        self.width = biggest+4



    def UpdateSelf(self, directory = False, coords = (), mode = False):
        self.height = 0
        self.width = 0
        self.x, self.y = coords[0], coords[1]
        self.itemdict = {}
        self.mode = mode
        if directory:
            filelist = listdir(directory)
            buffer = 2
            for item in filelist:
                textbox = FONT.render(str(item),True,(75,200,200))
                rect = textbox.get_rect()
                addheight = rect.height
                rect.x = self.x + 2
                rect.y = self.y + buffer

                box = FileBox(textbox,rect,str(item))
                buffer = buffer + addheight + 1
                width = rect.width
                if width > self.width:
                    self.width = width
                self.itemdict[box] = rect

            if self.mode == "save":
                textbox = FONT.render("NEW", True, (75,200,200))
                rect = textbox.get_rect()
                addheight = rect.height
                rect.x = self.x + 2
                rect.y = self.y - addheight - buffer
                box = FileBox(textbox, rect, "NEW")
                buffer = buffer+addheight+1
                width = rect.width
                if width > self.width:
                    self.width = width
                self.itemdict[box] = rect

            buffer = buffer + 2
            self.height = buffer
            self.width = self.width+4
            self.state = True

        return self.itemdict

    def draw(self, WINDOW):
        if self.state == True:
            draw.rect(WINDOW,(75,75,175),(self.x,self.y,self.width,self.height))
            for item in self.itemdict:
                WINDOW.blit(item.textitem, item.rect)

    def setDoClicked(self, function, function2 = False):
        for item in self.itemdict:
            if item.text != "NEW":
                item.doclicked = function
            else:
                item.doclicked = function2
