import pygame, random, sys
from pygame.locals import *

BOXDIM = 10
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BACKGROUNDCOLOR = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 30
SPEED = 1
Length = 10
InitialPositon = (290,290)
MoveTo = (1,0)
score = 0

def terminate():
    pygame.quit()
    sys.exit()
    
def drawText(text, font, surface, x, y, TextColour = (255,255,255)):
    textobj = font.render(text, 1, TextColour)
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
                if event.key != K_LEFT and event.key != K_RIGHT and event.key != K_UP and event.key != K_DOWN:
                    return
            
def FoodPosition(snake):
    FoodInSnake = True
    while FoodInSnake:
        X_pos = random.randint(0,(WINDOWWIDTH/BOXDIM)-1)
        Y_pos = random.randint(0,(WINDOWHEIGHT/BOXDIM)-1)
        for i in snake:
            if i.left == X_pos*BOXDIM and i.top == Y_pos*BOXDIM:
                FoodInSnake = True
                break
            else:
                FoodInSnake = False
    return (X_pos,Y_pos)
    

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Snake')
pygame.mouse.set_visible(False)

# Setting up the snake
def start(InitialPositon):
    snake = []
    for i in range(Length):
        snake.append(pygame.Rect(InitialPositon[0],
                                 InitialPositon[1],BOXDIM,BOXDIM))
        InitialPositon = (InitialPositon[0]-BOXDIM,InitialPositon[1])
    return snake

snake = start(InitialPositon)

# Setting Food
food_pos = FoodPosition(snake)
food = pygame.Rect(food_pos[0]*BOXDIM,food_pos[1]*BOXDIM,BOXDIM,BOXDIM)

#Setting up the sounds
pygame.mixer.music.load('Juhani Junkala Ending.wav')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

windowSurface.fill(BACKGROUNDCOLOR)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Tag', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

while True:
    #Set up movement
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if snake[0].left-BOXDIM<0:
                    if WINDOWWIDTH != snake[1].left:
                        MoveTo = (-1,0)
                else:
                    if(snake[0].left-BOXDIM) != snake[1].left:
                        MoveTo = (-1,0)                        
            if event.key == K_RIGHT:
                if snake[0].left+BOXDIM>=WINDOWWIDTH:
                    if(0) != snake[1].left:
                        MoveTo = (1,0)
                else:
                    if(snake[0].left+BOXDIM) != snake[1].left:
                        MoveTo = (1,0)
            if event.key == K_UP:
                if snake[0].top-BOXDIM < 0:
                    if WINDOWHEIGHT != snake[1].top:
                        MoveTo = (0,-1)
                else:
                    if(snake[0].top-BOXDIM) != snake[1].top:
                        MoveTo = (0,-1)
            if event.key == K_DOWN:
                if snake[0].top+BOXDIM >= WINDOWHEIGHT:
                    if 0 != snake[1].top:
                        MoveTo = (0,1)
                else:
                    if(snake[0].top+BOXDIM) != snake[1].top:
                        MoveTo = (0,1)
                    
    #Movement
    lastBlock = (snake[-1].left,snake[-1].top)
    for i in range(len(snake)-1):
        snake[len(snake)-i-1].left = snake[len(snake)-i-2].left
        snake[len(snake)-i-1].top = snake[len(snake)-i-2].top
    if snake[0].left+MoveTo[0]<0:
        snake[0].left=WINDOWWIDTH-BOXDIM
    elif snake[0].left+MoveTo[0]>=WINDOWWIDTH:
        snake[0].left=0
    elif snake[0].top+MoveTo[1]<0:
        snake[0].top = WINDOWHEIGHT-BOXDIM
    elif snake[0].top+MoveTo[1]>=WINDOWHEIGHT:
        snake[0].top = 0
    else:
        snake[0].move_ip(MoveTo[0]*10,MoveTo[1]*10)
    
    #check if eaten
    if snake[0].colliderect(food):
        score+=1
        snake.append(pygame.Rect(lastBlock[0],
                                 lastBlock[1],BOXDIM,BOXDIM))
        food_pos = FoodPosition(snake)
        food = pygame.Rect(food_pos[0]*BOXDIM,food_pos[1]*BOXDIM,
                           BOXDIM,BOXDIM)
        
        
    #check death
    for i in range(1,len(snake)):
        if snake[i].colliderect(snake[0]):
            drawText('Game Over', font, windowSurface,
                     (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
            drawText('Score: %s' % (score), font, windowSurface,
                     (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+50,(0,0,255))
            pygame.display.update()
            waitForPlayerToPressKey()
            snake = start(InitialPositon)
            food_pos = FoodPosition(snake)
            food = pygame.Rect(food_pos[0]*BOXDIM,food_pos[1]*BOXDIM,BOXDIM,BOXDIM)
            MoveTo = (1,0)
            score = 0
            break
            
    
    # Draw the game world on the window.
    windowSurface.fill(BACKGROUNDCOLOR)
    for i in range(len(snake)):
        if(i//25)%2==0:
            pygame.draw.rect(windowSurface,(255-(i%25)*10, (i%25)*10, 0)
                             ,snake[i])
        else:
            pygame.draw.rect(windowSurface,((i%25)*10, 255-(i%25)*10, 0)
                             ,snake[i])
    pygame.draw.rect(windowSurface,(255, 255, 255),food)
    drawText('Score: %s' % (score), font, windowSurface, 10, 0,(0,0,255))
    pygame.display.update()
    mainClock.tick(FPS)