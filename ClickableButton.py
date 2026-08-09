class ClickableOptionButton():
    def __init__(self, x, y, image = False):
        if image:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def draw(self, WINDOW, rect=False, transform=False):
        WINDOW.blit(self.image, self.rect)

    def doclicked(self):
        return False

    def setImage(self, image):
        self.image = image
        x,y = self.rect.x,self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y