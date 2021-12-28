import pygame, sys, math, random
import numpy as np
from pygame.locals import *
from math import pi

class Frog(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.attack_animation = False
		self.sprites = []
		self.sprites.append(pygame.image.load('attack_1.png'))
		self.sprites.append(pygame.image.load('attack_2.png'))
		self.sprites.append(pygame.image.load('attack_3.png'))
		self.sprites.append(pygame.image.load('attack_4.png'))
		self.sprites.append(pygame.image.load('attack_5.png'))
		self.sprites.append(pygame.image.load('attack_6.png'))
		self.sprites.append(pygame.image.load('attack_7.png'))
		self.sprites.append(pygame.image.load('attack_8.png'))
		self.sprites.append(pygame.image.load('attack_9.png'))
		self.sprites.append(pygame.image.load('attack_10.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y]

	def attack(self):
		self.attack_animation = True

	def update(self,speed):
		if self.attack_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 0
				self.attack_animation = False

		self.image = self.sprites[int(self.current_sprite)]

class Fall(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('burger.png'))
        self.sprites.append(pygame.image.load('cheese.png'))
        self.sprites.append(pygame.image.load('doughnut_chocolate.png'))
        self.sprites.append(pygame.image.load('muffin_plain.png'))
        self.sprites.append(pygame.image.load('oyster.png'))
        self.sprites.append(pygame.image.load('peanut.png'))
        self.sprites.append(pygame.image.load('peppermint.png'))
        self.sprites.append(pygame.image.load('pizza_vegetable_slice.png'))
        self.sprites.append(pygame.image.load('popcorn.png'))
        self.sprites.append(pygame.image.load('cantaloupe_whole.png'))
        self.sprites.append(pygame.image.load('carrot.png'))
        self.sprites.append(pygame.image.load('chili_pepper_red.png'))
        self.sprites.append(pygame.image.load('chocolate.png'))
        self.sprites.append(pygame.image.load('egg_whole_white.png'))
        self.sprites.append(pygame.image.load('popcorn.png'))
        self.sprites.append(pygame.image.load('shrimp.png'))
        self.sprites.append(pygame.image.load('Battery.png'))
        self.current_sprite = random.randrange(0,len(self.sprites))
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def update(self,speed,height):
        self.rect.topleft = [self.rect.left,self.rect.top+speed]
        if self.rect.top>height:
            pygame.sprite.Sprite.kill(self)
        
# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
FPS = 60
BACKGROUNDCOLOR = (0, 0, 0)
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
frog_sprites = pygame.sprite.Group()
frog = Frog(50,600)
frog_sprites.add(frog)
food_sprites = pygame.sprite.Group()
while len(food_sprites) < 10:
    food = Fall(random.randrange(0,WINDOWWIDTH),0)
    food_sprites.add(food)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            frog.attack()
    
    if len(food_sprites)<15 and random.randrange(0,100)<25:
        food = Fall(random.randrange(0,WINDOWWIDTH),0)
        food_sprites.add(food)
    screen.fill((0,0,0))
    frog_sprites.draw(screen)
    frog_sprites.update(0.25)
    food_sprites.draw(screen)
    food_sprites.update(1,WINDOWHEIGHT)
    pygame.display.flip()
    clock.tick(60)



