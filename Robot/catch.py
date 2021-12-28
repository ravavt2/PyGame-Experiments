import pygame, sys, math, random
import numpy as np
from pygame.locals import *
from math import pi

WINDOWWIDTH = 1000
WINDOWHEIGHT = 700
FPS = 60
BACKGROUNDCOLOR = (0, 0, 0)
XPosition = WINDOWWIDTH/2
YPosition = 550
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

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

#food sprite
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
        self.current_sprite = random.randrange(0,len(self.sprites))
        self.image = self.sprites[self.current_sprite]
        self.gripped = False
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        
    def update(self,speed,height,p,Gstatus):
        if self.gripped == False:
            self.rect.topleft = [self.rect.left,self.rect.top+speed]
        else:
            self.rect.center = p
        if self.rect.top>height and self.gripped == False:
            pygame.sprite.Sprite.kill(self)
        if self.rect.collidepoint(p[0], p[1]) and Gstatus == False:
            self.gripped = True
            robotStatus.collided(0)
        if self.rect.collidepoint([100,650]):
            pygame.sprite.Sprite.kill(self)
            robotStatus.reached()
            frog.attack()
            
            
#battery sprite
class Battery(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.sprites = pygame.image.load('Battery.png')
        self.image = self.sprites
        self.gripped = False
        
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        
    def update(self,speed,height,p,Gstatus):
        if self.gripped == False:
            self.rect.topleft = [self.rect.left,self.rect.top+speed]
        else:
            self.rect.topleft = p
        if self.rect.top>height and self.gripped == False:
            pygame.sprite.Sprite.kill(self)
        if self.rect.collidepoint(p[0], p[1]) and Gstatus == False:
            self.gripped = True
            robotStatus.collided(1)
        if self.rect.collidepoint([XPosition,YPosition]):
            pygame.sprite.Sprite.kill(self)
            robotStatus.reached()
        
class RoboCollision():
    def __init__(self):
        self.grip = False
        self.goal = 0
        
    def collided(self,num):
        self.grip = True
        self.goal = num
    def reached(self):
        self.grip = False

        
#creating a lambda function for transfer matrix
T = lambda theta, l: np.array([[math.cos(theta), -math.sin(theta), 0, l],
                               [math.sin(theta), math.cos(theta), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

def terminate():
    pygame.quit()
    sys.exit()
    
def origin3(r,l,theta):
    '''returns the position of link 3. 
    r = co-ordinate position of end effector
    l = array of link lengths from base to end effector
    theta = orientation of the end effector'''
    return np.array([r[0]-l[2]*math.cos(theta), r[1]-l[2]*math.sin(theta)])

def tran(phi,x):
    '''returs a transformation matrix from frame end effector to ground frame (T_0_H)
    input an array of joint angles and link lengths'''
    T = lambda theta, l: np.array([[math.cos(theta), -math.sin(theta), 0, l],
                                   [math.sin(theta), math.cos(theta), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])                                   
    T_0_N = T(phi[0],0)
    for i in range(1,len(phi)):
        T_0_N = np.matmul(T_0_N,T(phi[i],x[i-1]))
    T_0_N = np.matmul(T_0_N,T(0,x[-1]))
    return T_0_N

def joint2cart(angles,lengths):
    '''returns a list of coordinates of the joints'''
    linkpos = []
    for i in range(1,len(angles)+1):
        p = np.matmul(tran(angles[0:i],lengths[:i]),np.array([[0],[0],[0],[1]]))
        linkpos = linkpos + [[p[0,0],p[1,0]]]
    return linkpos

def Base2winOrg (cor, trans):
    '''returns an array of of corordinate positions with respect to window origin.
    cor should be an array of cordinate frames.
    trans is an numpy array of the transfer matrix with respect to window origin'''
    cor_win = []
    for i in cor:
        p_win = np.matmul(trans,np.array([[i[0]],[i[1]],[0],[1]]))
        cor_win = cor_win + [[p_win[0,0],p_win[1,0]]]
    return cor_win

def trajectory_cubic(p_i,p_f,t):
    '''returns coeficients of cubic polynomial moving for movement from initial
    position to final position in time t sec'''
    a = []
    for i in range(len(p_i)):
        a = a + [[p_i[i], 0, 3*(p_f[i]-p_i[i])/t**2, -2*(p_f[i]-p_i[i])/t**3]]
    return a

def cart2joint(endeffector,lengths,theta123):
    '''returns both sets of possible joint angles as 2*3 numpy matrix.'''
    link3 = origin3(endeffector, lengths, theta123)
    cos2 = (link3[0]**2+link3[1]**2-lengths[0]**2-lengths[1]**2)/(2*lengths[0]*lengths[1])
    if cos2 > 1:
        if np.linalg.norm(endeffector) > np.sum(lengths):
            theta = np.array([[math.atan2(endeffector[1],endeffector[0]),
                                 0.0,0.0],[math.atan2(endeffector[1],endeffector[0]),0.0,0.0]])
            return theta
        else:
            theta123 = math.atan2(endeffector[1],endeffector[0])
            theta = cart2joint(endeffector,lengths, theta123)
            return theta
    else:
        theta = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0]])
        theta[0,1] = math.atan2(math.sqrt(1-cos2**2),cos2)
        theta[1,1] = math.atan2(-math.sqrt(1-cos2**2),cos2)
        k01 = lengths[0]+lengths[1]*math.cos(theta[0,1])
        k02 = lengths[1]*math.sin(theta[0,1])
        k11 = lengths[0]+lengths[1]*math.cos(theta[1,1])
        k12 = lengths[1]*math.sin(theta[1,1])
        theta[0,0] = math.atan2(link3[1],link3[0])-math.atan2(k02,k01)
        theta[1,0] = math.atan2(link3[1],link3[0])-math.atan2(k12,k11)
        theta[0,2]=theta123-theta[0,0]-theta[0,1]
        theta[1,2]=theta123-theta[1,0]-theta[1,1]
        return theta
    
def updategoal(pos,theta0,T,lengths,XPosition,YPosition,T_pyOrg_o):
    '''updates the goal of the mouse'''
    endpoint = np.array([pos[0],pos[1]])
    endpoint = Base2winOrg ([endpoint], np.linalg.inv(T_pyOrg_o))
    endpoint = endpoint[0]
    pos_i = joint2cart(theta0, lengths)
    pos_i = pos_i[2]
    theta123 = math.atan2(endpoint[1]-pos_i[1],endpoint[0]-pos_i[0])
    theta_f = cart2joint(endpoint,lengths, theta123)
                
    #chosing theta with least rotation in link 0
    if abs(theta_f[0,0]-theta0[0]) < abs(theta_f[1,0]-theta0[0]):
        theta_f = theta_f[0,:]
    else:
        theta_f = theta_f[1,:]
    coeff = trajectory_cubic(theta0, theta_f, T)
    return coeff    

#Transfer matrix of base of the origin with respect to origin of the window
T_pyOrg_o = np.array([[1, 0, 0, XPosition],
                      [0, -1, 0, YPosition],
                      [0, 0, -1, 0],
                      [0, 0, 0, 1]])

lengths =np.array([165,165,165,]) #link lengts
theta0 = np.array([0.0, 0.0, 0.0]) #initial joint angles
thetat = theta0[:] #theta at time t
dt = 1/FPS #step
T = 1
t = 0
theta123 = 0 #orientation of endeffector
robotStatus = RoboCollision() #I have no clue what I am doing

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("Catching")

# Creating the sprites and groups
frog_sprites = pygame.sprite.Group()
frog = Frog(50,600)
frog_sprites.add(frog)
food_sprites = pygame.sprite.Group()
while len(food_sprites) < 5:
    food = Fall(random.randrange(150,WINDOWWIDTH-150),0)
    food_sprites.add(food)

endpoint = np.array([food_sprites.sprites()[0].rect.left,food_sprites.sprites()[0].rect.top])
endpoint = Base2winOrg ([endpoint], np.linalg.inv(T_pyOrg_o))
endpoint = endpoint[0]
theta_f = cart2joint(endpoint,lengths, theta123)
#chosing theta with least rotation in link 0
if abs(theta_f[0,0]-theta0[0]) < abs(theta_f[1,0]-theta0[0]):
    theta_f = theta_f[0,:]
else:
    theta_f = theta_f[1,:]

coeff = trajectory_cubic(theta0, theta_f, T)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            frog.attack()
    #adding food
    if len(food_sprites)<3 and random.randrange(0,100)<25:
        if random.randrange(0,100)<5:
            food = Battery(random.randrange(150,WINDOWWIDTH-150),0)
        else:
            food = Fall(random.randrange(150,WINDOWWIDTH-150),0)
        food_sprites.add(food)
        
    #joints in global space
    p = joint2cart(thetat, lengths)
    p = Base2winOrg(p, T_pyOrg_o)
    p = [[XPosition,YPosition]]+p
    
    screen.fill((0,0,0))
    frog_sprites.draw(screen)
    for i in range(len(p)-1):
        if(i%3 == 0):
            pygame.draw.line(screen, BLUE, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
        elif(i%3==1):
            pygame.draw.line(screen, RED, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
        else:
            pygame.draw.line(screen, GREEN, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
    t = t+dt
    if t < T:
        #updating thetat
        for i in range(len(thetat)):
            thetat[i] = coeff[i][0] + coeff[i][1]*t+coeff[i][2]*t**2+coeff[i][3]*t**3
    if t > T and robotStatus.grip == False:
        pos = [food_sprites.sprites()[0].rect.left,food_sprites.sprites()[0].rect.top+FPS+5]
        coeff = updategoal(pos,thetat,T,lengths,XPosition,YPosition,T_pyOrg_o)
        t = 0
    if robotStatus.grip == True and t>T:
        if robotStatus.goal == 0:
            pos = [100,650]
            coeff = updategoal(pos,thetat,T,lengths,XPosition,YPosition,T_pyOrg_o)
            t = 0
        else:
            pos = [XPosition,YPosition]
            coeff = updategoal(pos,thetat,T,lengths,XPosition,YPosition,T_pyOrg_o)
            t = 0
    # Draw the window onto the screen.
    
    frog_sprites.update(0.25)
    food_sprites.draw(screen)
    food_sprites.update(1,WINDOWHEIGHT,p[len(p)-1],robotStatus.grip)
    pygame.display.flip()
    clock.tick(60)



