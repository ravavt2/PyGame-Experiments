# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 09:36:35 2022

@author: tejas
"""

Floor = True
Wall = False

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
WHITE = (255,255,255)
Wallcolor = (155,155,155)
BACKGROUNDCOLOR = (0, 0, 0)
CellColor = (155,100,100)
FPS = 60

import random, copy
import pygame, sys
from pygame.locals import *
#SEED = 10
#random.seed(SEED)

def make_noise_grid(density,height,width):
    '''function returns a noise grid with random True or False values'''
    noise_grid = []
    for i in range(height):
        noise_grid = noise_grid + [[]]
    for i in range(height):
        for j in range(width):
            rand = random.randint(1,100)
            if rand > density:
                noise_grid[i] = noise_grid[i] + [Floor]
            else:
                noise_grid[i] = noise_grid[i] + [Wall]
    return noise_grid


def firstIteration(grid,height,width):
    '''counts the number of walls in the neighbourhoud 
    and changes to wall if neighbouring walls are greated than 4'''
    tempGrid = copy.deepcopy(grid)
    for i in range(height):
        for j in range(width):
            neigh_wall_count = 0
            for y in range(i-1,i+2):
                for x in range(j-1,j+2):
                    if (y>=0 and y<height) and (x>=0 and x<width): #is within map bound
                        if (y!=i) or (x!=j):
                            if (grid[y][x]==Wall):
                                neigh_wall_count+=1
                    else:
                        neigh_wall_count+=1
            if neigh_wall_count>4:
                tempGrid[i][j]=Wall
            else:
                tempGrid[i][j]=Floor
    return tempGrid

def terminate():
    pygame.quit()
    sys.exit()
    
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

density = 60
map_height = 120
map_width = 120
boxHeight = WINDOWHEIGHT//map_height
boxWidth = WINDOWWIDTH//map_width

noise_grid = make_noise_grid(density,map_height,map_width)
                    
firstGrid = firstIteration(noise_grid,map_height,map_width)
grids = [noise_grid] + [firstGrid]
current_grid = firstGrid
grid_iter = 0

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

pygame.display.set_caption('Maze')
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Press any key to generate a Maze', font, windowSurface, 
         (15), (WINDOWHEIGHT / 3))
pygame.display.update()
waitForPlayerToPressKey()


while True:
    windowSurface.fill(BACKGROUNDCOLOR)
    
    if grid_iter < len(grids):
        current_grid = grids[grid_iter]
        
    else:
        while grid_iter >= len(grids):
            current_grid = firstIteration(grids[-1],map_height,map_width)
            grids.append(current_grid)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if grid_iter>0:
                    grid_iter -=1
            if event.key == K_RIGHT:
                grid_iter +=1
        
        for i in range(map_height):
            for j in range(map_width):
                if current_grid[i][j]==True:
                    pygame.draw.rect(windowSurface, CellColor,
                                     (j*boxWidth,i*boxHeight,boxWidth,boxHeight))
        
        pygame.display.update()
        mainClock.tick(FPS)