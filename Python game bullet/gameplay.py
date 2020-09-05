import pygame
import random
import time

from player import Player
from treasure import Treasure
from enemy import Enemy
from wall import Wall
from bullet import Bullet
from level import *
from variables import *


def getPlayerName(screen):
    name = ""
    font = pygame.font.Font(None, 50)
    text = "Enter your name :"
    text_block = font.render(text, True, (255, 67, 100))
    text_rect = text_block.get_rect()
    text_rect.centerx=screen.get_rect().centerx
    text_rect.centery=screen.get_rect().centery - 50
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    return name
            elif event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        block = font.render(name, True, (255, 20, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(text_block, text_rect)
        screen.blit(block, rect)
        pygame.display.flip()
        


def game(screen, room, level, lvl):
    pygame.display.set_caption('Maze Runner')
    font = pygame.font.Font('./data/fonts/freesansbold.ttf', 20)
    gameoverfont = winfont = pygame.font.Font('./data/fonts/freesansbold.ttf', 72)
    gameovertext = gameoverfont.render('Game Over', 1, RED)
    gameoverrect = gameovertext.get_rect()
    gameoverrect.centerx = 320; gameoverrect.centery = 240
    wintext = winfont.render('Level Completed', 1,  RED)
    winrect = wintext.get_rect()
    winrect.centerx = 320; winrect.centery = 240
    startime = font.render('Time: 0', 1, WHITE)
    startrect = startime.get_rect()
    startrect.x = 0; startrect.y = 0
    gameovercount = 0; gameoverdelay = 90
    wincount = 0; windelay = 90
    
    
    invinciblecount = 0; invincibledelay = 20; invincibleon = False
    clock = pygame.time.Clock()
    gamePause = False
    #player=None
    walls=[]
    enemys=[]
    treasures=[]
    starttime = time.time()
    for x in range(len(level)):
        for y in range(len(level[x])):
            char = level[x][y]
            s_x=35+y*25
            s_y=35+x*25
            if char == "X":
                room.wall_list.add(Wall(s_x,s_y))
            elif char == "E":
                room.enemy_sprites.add(Enemy(s_x,s_y))
            elif char == "P":
                player = Player(s_x, s_y)
            elif char == "T":
                room.treasure_list.add(Treasure(s_x,s_y))       
         
    lives = int(player.lives); livestext = font.render('Lives: %s' % str(player.lives), 1, WHITE, BLACK)
    #enemy_c = len(room.enemy_sprites); enemy_text = font.render('Enemies: %s' % str(len(room.enemy_sprites)), 1, WHITE, (0,0,0))
    livesrect = livestext.get_rect()
    livesrect.x = screen.get_width()-livesrect.width
    livesrect.y = 0
    
    level_text = font.render('Level: %s' % str(lvl), 1, WHITE, (0,0,0))
    levelrect = level_text.get_rect()
    levelrect.centerx = screen.get_width()/2
    levelrect.y = 0
    
         
    
 
    # Create the player object
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    bullets = pygame.sprite.Group()
 
    rooms = []
 
    
    rooms.append(room)
 
    current_room_no = 0
    current_room = rooms[current_room_no]
 
    
 
    done = False
    pygame.mixer.music.load('./data/background_music.ogg') 
    #pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1,)
    screen.blit(startime, startrect)
    screen.blit(livestext, livesrect)
 
    while not done:
        screen.fill(BLACK)
        if not gamePause:
            tTime = int(round(abs(starttime-time.time())))
        else:
            if int(round(abs(starttime-time.time()))) > tTime:
                starttime += 1
        startime = font.render('Time: '+str(tTime), 1, WHITE, BLACK)
        #livestext = font.render('Lives: %s' % str(player.lives), 1, (255,255,255), (0,0,0))
        
 
        if invinciblecount > 0: invinciblecount -= 1
        if player.invincible: invincibleon = not invincibleon
        if invinciblecount == 0: player.invincible = False
 
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN and not gamePause:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0, "LEFT")
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0, "RIGHT")
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5, "UP")
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5, "DOWN")
                if event.key == pygame.K_SPACE:
                    bullets.add(Bullet(player.rect.x , player.rect.y + 10, player.prev_dir))
 
            if event.type == pygame.KEYUP and not gamePause:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0, "LEFT")
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0, "RIGHT")
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5, "UP")
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5, "DOWN")
 
        # --- Game Logic ---
        if not gamePause:
            player.move(current_room.wall_list,current_room.enemy_sprites,current_room.treasure_list )
            
            for group in current_room.enemy_sprites:
                group.changespeed(player)
                group.move(current_room.wall_list)
               
            for treasure in current_room.treasure_list:
                treasure.animate()
                
            for bull in bullets:
                bull.update(current_room.wall_list, current_room.enemy_sprites)
        
            if lives > player.lives and player.lives >= 0:
                lives = player.lives
                livestext = font.render('Lives: %s' % str(player.lives), 1, WHITE, BLACK)
                player.invincible = True
                invinciblecount = invincibledelay
            if player.lives == 0 and (not player.dead):
                gameovercount = gameoverdelay
                gamePause = True
                player.dead = True
            if not current_room.treasure_list and ( not player.won ):
                wincount = windelay
                gamePause = True
                player.won=True

            
        if gameovercount > 0: gameovercount -= 1
        if gameovercount == 0 and player.dead:
            done = True
        if wincount > 0: wincount -= 1
        if wincount == 0 and player.won:
            pygame.sprite.Group.empty(current_room.wall_list)
            pygame.sprite.Group.empty(current_room.enemy_sprites)
            pygame.sprite.Group.empty(current_room.treasure_list)
            return True
            
        
        
        
 
        # --- Drawing ---
        if not player.invincible and not player.dead and not player.won: movingsprites.draw(screen)
        if player.invincible and invincibleon and not player.dead: movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        current_room.enemy_sprites.draw(screen)
        current_room.treasure_list.draw(screen)
        bullets.draw(screen)
        screen.blit(startime, startrect)
        screen.blit(livestext, livesrect)
        screen.blit(level_text, levelrect)
        
        
        
        if player.won:
            screen.blit(wintext, winrect)
        if player.dead:
            screen.blit(gameovertext, gameoverrect)
        #print(current_room.enemy_sprites)

        pygame.display.flip()
 
        clock.tick(20)
    return False

def main():
    """ Main Program """
    # Initialising Pygame library 
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode([700, 700])
    done = False
    pName = getPlayerName(screen)
    print(pName)
    room = Room1()
    #clock.tick(20)
    i=1
    for level in room.level:
        if not game(screen,room,level,i):
            break
        i+=1

    pygame.quit()
 
if __name__ == "__main__":
    main()
