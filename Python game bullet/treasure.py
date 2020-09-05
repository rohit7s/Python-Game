import pygame
from variables import *

class Treasure(pygame.sprite.Sprite):
    img=treasure_img
    curr=0
    def __init__(self, x, y):
 
        super(Treasure,self).__init__()
 
        self.image = pygame.image.load(self.img[self.curr])
         
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def getPos(self):
        return (self.rect.x,self.rect.y)
     
    def animate(self):
        self.curr+=1
        if self.curr == 9:
            self.curr=0
        self.image = pygame.image.load(self.img[self.curr])
