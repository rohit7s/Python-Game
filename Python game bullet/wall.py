import pygame
from variables import *
class Wall(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        super(Wall,self).__init__()
        self.image = pygame.image.load(wall_img)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
