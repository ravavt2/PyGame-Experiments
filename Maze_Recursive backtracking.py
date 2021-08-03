# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 11:50:37 2021

@author: sun
"""
# Creating a maze using Recursive Backtracking algorithm
# Using deque to implement a stack for creating a maze

from collections import deque
import pygame, random, sys, enum
from pygame.locals import *

BOXDIM = 20
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
FPS = 60
BACKGROUNDCOLOR = (0, 0, 0)
CellColor = (155,100,100)
UnvisitedCellColor = (150,150,250)
WHITE = (255,255,255)
Wallcolor = (155,155,155)
WallWidth = 5

m_maze = [] #to keep track of visited cells
for i in range(((WINDOWWIDTH*WINDOWHEIGHT//BOXDIM)//BOXDIM)):
    m_maze.append([])

class connectedCell(enum.Enum):
    Cell_Path_N = 1
    Cell_Path_E = 2
    Cell_Path_S = 3
    Cell_Path_W = 4
    Cell_Visited = 5

mVisitedCells = 0 #how many cells visited

m_stack = deque()
m_stack.append((0,0))

m_maze[0].append(connectedCell.Cell_Visited)
mVisitedCells = 1

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
    
    neighbours = []
    #lambda function
    offset = lambda x,y: (m_stack[-1][1] + y) * WINDOWWIDTH//BOXDIM + (m_stack[-1][0] + x)
    
    #Maze creating
    if(mVisitedCells<((WINDOWWIDTH*WINDOWHEIGHT//BOXDIM)//BOXDIM)):
        #Create  set of unvisited neighbours
        #print('next')
        #North Neighbours
        if m_stack[-1][1]>0 and connectedCell.Cell_Visited not in m_maze[offset(0, -1)]:
            neighbours.append(0)
        
        #Eastern Neighbours
        if (m_stack[-1][0]<(WINDOWWIDTH//BOXDIM)-1) and connectedCell.Cell_Visited not in m_maze[offset(1, 0)]:
            neighbours.append(1)
            
        #South Neighbours
        if (m_stack[-1][1]<(WINDOWHEIGHT//BOXDIM)-1) and connectedCell.Cell_Visited not in m_maze[offset(0, 1)]:
            neighbours.append(2)
            
        #West Neighbours
        if m_stack[-1][0]>0 and connectedCell.Cell_Visited not in m_maze[offset(-1, 0)]:
            neighbours.append(3)
        
        #are neighbours available
        if len(neighbours) != 0:
            #choose a neighbour at random
            next_cell_dir = neighbours[random.randint(0,len(neighbours)-1)]
            #print("A ",m_stack[-1], m_maze[offset(0,0)],offset(0,0),next_cell_dir)
            
            #create a path to the neighbour
            if next_cell_dir == 0: #North direction
                m_maze[offset(0, -1)].append(connectedCell.Cell_Visited)
                m_maze[offset(0, -1)].append(connectedCell.Cell_Path_S)
                m_maze[offset(0, 0)].append(connectedCell.Cell_Path_N)
                #print("B ",offset(0, -1),m_maze[offset(0, -1)])
                m_stack.append(((m_stack[-1][0] + 0), (m_stack[-1][1] - 1)));
            elif next_cell_dir == 1: #Eastern direction
                m_maze[offset(1, 0)].append(connectedCell.Cell_Visited)
                m_maze[offset(1,0)].append(connectedCell.Cell_Path_W)
                m_maze[offset(0, 0)].append(connectedCell.Cell_Path_E)
                #print("B ",offset(1,0),m_maze[offset(1,0)])
                m_stack.append(((m_stack[-1][0] + 1), (m_stack[-1][1] + 0)));
            elif next_cell_dir == 2: #South directiom
                m_maze[offset(0, 1)].append(connectedCell.Cell_Visited)
                m_maze[offset(0, 1)].append(connectedCell.Cell_Path_N)
                m_maze[offset(0, 0)].append(connectedCell.Cell_Path_S)
                #print("B ",offset(0, 1),m_maze[offset(0, 1)])
                m_stack.append(((m_stack[-1][0] + 0), (m_stack[-1][1] + 1)));
            elif next_cell_dir == 3: #West direction
                m_maze[offset(-1, 0)].append(connectedCell.Cell_Visited)
                m_maze[offset(-1, 0)].append(connectedCell.Cell_Path_E)
                m_maze[offset(0, 0)].append(connectedCell.Cell_Path_W)
                #print("B ",offset(-1, 0),m_maze[offset(-1, 0)])
                m_stack.append(((m_stack[-1][0] - 1), (m_stack[-1][1] + 0)));
            mVisitedCells +=1
            #print("C ", m_stack[-1], m_maze[offset(0,0)],offset(0,0), 
                  #"len stack = ", len(m_stack), "mVisitedCells ", mVisitedCells)
            
        else:
            m_stack.pop()
            
    
    #Draws the maze blocks
    for j in range(WINDOWHEIGHT//BOXDIM):
        for i in range(WINDOWWIDTH//BOXDIM):
            #Draws visited cells
            if (connectedCell.Cell_Visited in m_maze[(j*WINDOWWIDTH//BOXDIM)+i]):
                pygame.draw.rect(windowSurface, CellColor, 
                                 (i*BOXDIM,j*BOXDIM,
                                  BOXDIM-WallWidth,BOXDIM-WallWidth))
            else:#Draws unvisited cells
                pygame.draw.rect(windowSurface, UnvisitedCellColor, 
                                 (i*BOXDIM,j*BOXDIM,
                                  BOXDIM-WallWidth,BOXDIM-WallWidth))
            #Draws walls to south
            if(connectedCell.Cell_Path_S in m_maze[(j*WINDOWWIDTH//BOXDIM)+i]):
                pygame.draw.rect(windowSurface, CellColor,
                                 ((i)*BOXDIM,(j+1)*BOXDIM-WallWidth,
                                  BOXDIM-WallWidth,WallWidth))
            #Draws walls to east
            if(connectedCell.Cell_Path_E in m_maze[(j*WINDOWWIDTH//BOXDIM)+i]):
                pygame.draw.rect(windowSurface, CellColor,
                                 ((i+1)*BOXDIM-WallWidth,(j)*BOXDIM,
                                  WallWidth,BOXDIM-WallWidth))
    if(mVisitedCells<((WINDOWWIDTH*WINDOWHEIGHT//BOXDIM)//BOXDIM)):
        pygame.draw.rect(windowSurface, WHITE, 
                     (m_stack[-1][0]*BOXDIM,m_stack[-1][1]*BOXDIM,
                      BOXDIM-WallWidth,BOXDIM-WallWidth))
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
    pygame.display.update()
    mainClock.tick(FPS)
    