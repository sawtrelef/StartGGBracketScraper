from pygame import Rect, draw, image, font, transform, Surface
from ClickableButton import ClickableOptionButton


font.init()

FONT = font.Font('SuperMystery.ttf', 14)

#test = FONT.render("Sometext", True, (125,125,45))
#height = test.get_height()
#width = test.get_width()

class ItemCell(ClickableOptionButton):
    colors = colors = {False: (75, 12, 75), True: (75, 180, 75), "Text":(125, 85, 0)}
    def __init__(self,x,y,item,image):
        super().__init__(x, y, image)
        self.item = item
        self.doclicked = self.returnItem
        self.activestate = False
        self.clicked = False

    def returnItem(self):
        if self.activestate:
            return self.item

    def toggle(self):
        self.activestate = not self.activestate

    def toggleclicked(self):
        self.clicked = not self.clicked
        textimage = FONT.render(self.item,True,self.colors["Text"],self.colors[self.clicked])
        self.image = textimage

    def cutoff(self, stopx):
        textrect = self.image.get_rect()
        x = self.rect.x

        if x + textrect.width > stopx:
            newwidth = stopx - self.rect.x
            tmpsurface = Surface((newwidth, textrect.height))
            textrect.update(textrect.x, textrect.y, newwidth, textrect.height)
            tmpsurface.blit(self.image, (textrect.x, textrect.y), textrect)
            self.image = tmpsurface


    def draw(self,WINDOW):
        if self.activestate:
            super().draw(WINDOW)



class ItemListDisplay():
    def __init__(self,x,y,width,height):
        self.itemlist = []
        self.buttondict = {}
        self.rect = Rect(x,y,width,height)
        self.color = (75,75,75)
        self.upimage = image.load("UpArrow.png")
        self.downimage = image.load("DownArrow.png")
        self.upButton = ClickableOptionButton(self.rect.x+self.rect.width-self.upimage.get_width(), self.rect.y,self.upimage)
        self.downButton = ClickableOptionButton(self.rect.x + self.rect.width - self.downimage.get_width(), self.rect.y+self.rect.height-self.downimage.get_height(), self.downimage)
        self.upButton.doclicked = self.tabUp
        self.downButton.doclicked = self.tabDown
        self.minimum = 0
        self.maximum = 0
        test = FONT.render('W',True,(1,1,1),(60,60,60))
        testheight = test.get_height()
        self.range = int((self.rect.height-24)/20)

    def tabUp(self):
        if self.minimum > 0:
            self.minimum = self.minimum - 1
            self.updateDisplayList()
    def tabDown(self):
        if self.minimum + self.range + 1 < self.maximum:
            self.minimum = self.minimum + 1
            self.updateDisplayList()

    ##ITEMLIST IS A LIST OF STRINGS
    def setitemlist(self,itemlist):
        del self.itemlist
        del self.buttondict
        self.itemlist = itemlist
        self.buttondict = {}
        self.maximum = len(self.itemlist)-1
        ID = 0
        for item in self.itemlist:
            x = self.rect.x + 5
            y = -1
            textbox = FONT.render(str(item), True, (125, 85, 0), (75, 12, 75))
            textrect = textbox.get_rect()
            stopx = self.downButton.rect.x
            if x + textrect.width > stopx:
                newwidth = stopx - x
                tmpsurface = Surface((newwidth,textrect.height))
                textrect.update(textrect.x,textrect.y,newwidth,textrect.height)
                tmpsurface.blit(textbox,(0,0),textrect)
                textbox = tmpsurface
            button = ItemCell(x,y,str(item),textbox)
            self.buttondict[ID] = button
            ID = ID+1
        self.updateDisplayList()

    def additem(self,item):
        self.itemlist.append(item)
        self.setitemlist(self.itemlist)

    def updateDisplayList(self):
        for item in self.buttondict:
            self.buttondict[item].activestate = False

        x = self.rect.x + 5
        y = self.rect.y + 12
        for item in range(self.minimum,self.minimum+self.range+1):
            if item in self.buttondict:
                self.buttondict[item].activestate = True
                self.buttondict[item].rect.y = y
                self.buttondict[item].rect.x = x
                y = y+20
            else:
                break


    def draw(self,WINDOW):
        draw.rect(WINDOW, (75, 75, 75), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        WINDOW.blit(self.upimage,(self.upButton.rect.x,self.upButton.rect.y))
        WINDOW.blit(self.downimage, (self.downButton.rect.x, self.downButton.rect.y))
        for item in self.buttondict:
            self.buttondict[item].draw(WINDOW)



