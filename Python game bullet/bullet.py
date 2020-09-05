import pygame
import random
from variables import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
 
        super(Bullet,self).__init__()
        self.image = pygame.image.load(bullet_img)
        self.rect = self.image.get_rect()
        self.rect.y = y; self.starty = y
        self.rect.x = x; self.startx = x
        self.curr_dir = direction
        self.life = 200
        
    def update(self, walls ,enemy):
 
        if self.curr_dir == "RIGHT":
            self.rect.x += 10
        elif self.curr_dir == "LEFT":
            self.rect.x -=10
        elif self.curr_dir == "UP":
            self.rect.y -= 10
        elif self.curr_dir == "DOWN":
            self.rect.y +=10
 
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        if block_hit_list:
            self.kill()
        enemy_hit_list = pygame.sprite.spritecollide(self,enemy,False)
        for block in enemy_hit_list:
            block.kill()
            self.kill()
        if abs(self.rect.x - self.startx) > self.life: self.kill()
        if abs(self.rect.y - self.starty) > self.life: self.kill()
        

