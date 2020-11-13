import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    K_SPACE,
    K_w,
    K_a,
    K_s,
    K_d,
    KEYDOWN,
    QUIT,
)

pygame.init()
clock = pygame.time.Clock()
screenWidth = 1250
screenHeight = 750

win = pygame.display.set_mode((screenWidth, screenHeight))

#for a certain time after, attack remains, else, erase it
#attack cant be used - cooldown(done)

playerSprites = [pygame.image.load("images/p1-up.png"), pygame.image.load("images/p1-down.png"), pygame.image.load("images/p1-right.png"), pygame.image.load("images/p1-left.png")]

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)#x, width, height
        self.facing = 0

        self.aRect = (0, 0, 0, 0)
        #part of the attack
        self.cooldown = 500
        self.lastFire = 0
        self.now = 0
        
    def move(self, keys):    
        if keys[K_w] or keys[K_UP]:
            self.y -= 1
            self.facing = 0
            attacks.clear()
            
        if keys[K_s] or keys[K_DOWN]:    
            self.y += 1
            self.facing = 1
            attacks.clear()
            
        if keys[K_d] or keys[K_RIGHT]:
            self.x += 1
            self.facing = 2
            attacks.clear()
            
        if keys[K_a] or keys[K_LEFT]:
            self.x -= 1
            self.facing = 3
            attacks.clear()

        #attack
        if keys[K_SPACE]:
            self.now = pygame.time.get_ticks()
            if self.now - self.lastFire > self.cooldown or self.lastFire == 0:
                self.lastFire = self.now
                if self.facing == 0:
                    self.aRect = (self.x, self.y -self.height, self.width, self.height)
                if self.facing == 1:
                    self.aRect = (self.x, self.y + self.height, self.width, self.height)
                if self.facing == 2:
                    self.aRect = (self.x + self.width, self.y, self.width, self.height)
                if self.facing == 3:
                    self.aRect = (self.x - self.width, self.y, self.width, self.height)
                attacks.append(self.aRect)


        self.hitbox = (self.x, self.y, self.width, self.height)


    def attackClear(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.lastFire > 1000:
            attacks.clear()

#    def draw(self, win):
#            win.blit(pygame.image.load("images/p1-down.png"), (self.x, self.y))
        


                

        
    
"""
attack
create a projectile that is launched from a side. disapears after a while

add projecticle to a list, if its not in the list, it doesnt check for hitboxes
"""




class Enemy(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    #def start(self):
        self.moveDec = random.randint(1, 2)
        if self.moveDec == 1:
            OoX = random.randint(1, 2)
            if OoX == 1:
                self.x = 0
            else:
                self.x = screenWidth
            self.y = random.randint(0, screenHeight)
            
        else:
            OoY = random.randint(1, 2)
            if OoY == 1:
                self.y = 0
            else:
                self.y = screenHeight
            self.x = random.randint(0, screenWidth)
        self.hitbox = (self.x, self.y, self.width, self.height)


    def move(self, playerX, playerY):
        if self.x < playerX:
            self.x += 1
            
        elif self.x > playerX:
            self.x -= 1
            
        if self.y < playerY:
            self.y += 1
            
        elif self.y > playerY:
            self.y -= 1
        self.hitbox = (self.x, self.y, self.width, self.height)

            
        

p1 = Player(int(screenWidth/2), int(screenHeight/2), 20, 30)   #defining player   19, 29


#defining an enemy
#newEnemy = Enemy(10, 10)
#newEnemy.start()


def redrawWindow():
    win.fill((25, 25, 25))
    #if len(attacks) > 0:
    for rectangles in attacks:
        pygame.draw.rect(win, [0, 100, 0], p1.aRect)
        
    pygame.draw.rect(win, [255, 0, 0], p1.hitbox)
    win.blit(playerSprites[p1.facing], (p1.x, p1.y))    
    for enemy in enemies:
        pygame.draw.rect(win, [100, 100, 100], enemy.hitbox)
    pygame.display.flip()


#pre loop variables
attacks = []
enemies = []

game = True

#game start
while game:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game = False
        elif event.type == QUIT:
            game = False

    #creating enemies
    if len(enemies) < 2:
        newEnemy = Enemy(10, 10)
        enemies.append(newEnemy)
    
    #attack hitbox
    for attack in attacks:
        for enemy in enemies:
            if enemy.hitbox[0] < attack[0] + attack[2] and enemy.hitbox[0] + enemy.hitbox[2] > attack[0]:
                if enemy.hitbox[1] < attack[1] + attack[3] and enemy.hitbox[1] + enemy.hitbox[3] > attack[1]:
                    enemies.pop(enemies.index(enemy))
            
    #player hitbox
    for enemy in enemies:
        if p1.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2] and p1.hitbox[0] + p1.hitbox[2] > enemy.hitbox[0]:
            if p1.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and p1.hitbox[1] + p1.hitbox[3] > enemy.hitbox[1]:
                game = False        



    #moves/redraw
    for enemy in enemies:
        enemy.move(p1.x, p1.y)
    keys = pygame.key.get_pressed()
    p1.move(keys)
    p1.attackClear()
    redrawWindow()

    clock.tick(100)

    
