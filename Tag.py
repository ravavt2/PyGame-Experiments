import pygame, random, sys
import math
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BACKGROUNDCOLOR = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
SPEED = 5
AISPEED = 8
BOXDIM = 30
x = y =0
PI = 3.1415
botEscaping = False

def distance (x,y):
    return math.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

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

def pol_cord(x,SPEED):
    return (round(math.cos(x),2)*SPEED,round(math.sin(x),2)*SPEED)

#x is player and y is ai
def calcangle(x,y):
    tanInv = math.atan2(x[1]-y[1],x[0]-y[0])
    return (random.uniform(tanInv+PI/3,tanInv+2*PI-PI/3))
    


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tag')
pygame.mouse.set_visible(False)

#Set up player and ai
playerRect = pygame.Rect(random.randint(0,(WINDOWWIDTH/2)-BOXDIM),
                         random.randint(0,(WINDOWHEIGHT/2)-BOXDIM),
                         BOXDIM, BOXDIM)
aiRect = pygame.Rect(random.randint((WINDOWWIDTH/2),WINDOWWIDTH-BOXDIM),
                         random.randint((WINDOWHEIGHT/2),WINDOWHEIGHT-BOXDIM),
                         BOXDIM, BOXDIM)

#Setting up the sounds
pygame.mixer.music.load('Juhani Junkala Ending.wav')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Tag', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

#Setting initial AI direction
angle = random.uniform(-PI,PI)

while True:
    #Set up the start of the game.
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                x = -1
            if event.key == K_RIGHT:
                x = 1
            if event.key == K_UP:
                y = -1
            if event.key == K_DOWN:
                y = 1
                
        if event.type == KEYUP:
            if event.key == K_LEFT and x<0:
                x = 0
            if event.key == K_RIGHT and x>0:
                x = 0
            if event.key == K_UP and y<0:
                y = 0
            if event.key == K_DOWN and y>0:
                y = 0

    # Move the player around.

    if (playerRect.left > 0 and x< 0):
        playerRect.move_ip(x * SPEED, 0)
    if (playerRect.right < WINDOWWIDTH and x> 0):
        playerRect.move_ip(x * SPEED, 0)
    if (playerRect.top>0 and y<0):
        playerRect.move_ip(0,y * SPEED)
    if (playerRect.bottom<WINDOWHEIGHT and y>0):
        playerRect.move_ip(0,y * SPEED)

    # Move AI around
    if (aiRect.top<=0):
        angle = random.uniform(0,PI)
    if (aiRect.left<=0):
        angle = random.uniform(-PI/2,PI/2)
    if (aiRect.right>=WINDOWWIDTH):
        angle = random.uniform(PI/2,3*PI/2)
    if (aiRect.bottom>=WINDOWHEIGHT):
        angle = random.uniform(-PI,0)
    if (distance((playerRect.centerx,playerRect.centery),
                 (aiRect.centerx,aiRect.centery))<60) and botEscaping==False:
        angle = calcangle((playerRect.centerx,playerRect.centery),
                                (aiRect.centerx,aiRect.centery))
        botEscaping = True
    if (distance((playerRect.centerx,playerRect.centery),
                 (aiRect.centerx,aiRect.centery))>60) and botEscaping==True:
        botEscaping = False
        
    aiRect.move_ip(pol_cord(angle,AISPEED))
    if playerRect.colliderect(aiRect):
        drawText('You Hit the Green Box!!!', font, windowSurface,
                 (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Are you happy now?', font, windowSurface,
                 (WINDOWWIDTH / 3)-150, (WINDOWHEIGHT / 3)+30)
        pygame.display.update()
        waitForPlayerToPressKey()
        playerRect = pygame.Rect(random.randint(0,(WINDOWWIDTH/2)-BOXDIM),
                                 random.randint(0,(WINDOWHEIGHT/2)-BOXDIM),
                                 BOXDIM, BOXDIM)
        aiRect = pygame.Rect(random.randint((WINDOWWIDTH/2),WINDOWWIDTH-BOXDIM),
                             random.randint((WINDOWHEIGHT/2),WINDOWHEIGHT-BOXDIM),
                             BOXDIM, BOXDIM)
        x=y=0
        
            

    # Draw the game world on the window.
    windowSurface.fill(BACKGROUNDCOLOR)
    pygame.draw.rect(windowSurface,RED,playerRect)
    pygame.draw.rect(windowSurface,GREEN,aiRect)
    pygame.display.update()
    mainClock.tick(FPS)
    


