# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:20:55 2021

@author: tejas
"""

#Graphical simulation of 3R manipulator

import pygame, sys, math
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

#creating a lambda function for transfer matrix
T = lambda theta, l: np.array([[math.cos(theta), -math.sin(theta), 0, l],
                               [math.sin(theta), math.cos(theta), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

def terminate():
    pygame.quit()
    sys.exit()
    
def drawText(text, font, surface, x, y, TextColour = (255,255,255)):
    textobj = font.render(text, 1, TextColour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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
            return 'Out of Workspace'
        else:
            return 'Orientation not possible'
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
    if isinstance(theta_f, str):
        if theta_f == 'Out of Workspace':
            theta_f = np.array([[math.atan2(endpoint[1],endpoint[0]),
                                 0.0,0.0],[math.atan2(endpoint[1],endpoint[0]),0.0,0.0]])
        elif theta_f == 'Orientation not possible':
            c = np.linalg.norm(endpoint)/2
            theta123 = math.atan2(endpoint[1],endpoint[0])
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
endpoint = np.array([0.0,0.0]) #position of the end effector with respect to base frame
thetat = theta0[:] #theta at time t
dt = 1/FPS #step
T = 1
t = 0
theta123 = 0 #orientation of endeffector
theta_f = cart2joint(endpoint,lengths, theta123)
#chosing theta with least rotation in link 0
if abs(theta_f[0,0]-theta0[0]) < abs(theta_f[1,0]-theta0[0]):
    theta_f = theta_f[0,:]
else:
    theta_f = theta_f[1,:]

coeff = trajectory_cubic(theta0, theta_f, T)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Trajectory')

while True:
    #joints in global space
    p = joint2cart(thetat, lengths)
    p = Base2winOrg(p, T_pyOrg_o)
    p = [[XPosition,YPosition]]+p
    windowSurface.fill(BACKGROUNDCOLOR)
    for i in range(len(p)-1):
        if(i%3 == 0):
            pygame.draw.line(windowSurface, BLUE, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
        elif(i%3==1):
            pygame.draw.line(windowSurface, RED, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
        else:
            pygame.draw.line(windowSurface, GREEN, (p[i][0], p[i][1]),
                             (p[i+1][0], p[i+1][1]), 4)
    t = t+dt
    if t < T:
        #updating thetat
        for i in range(len(thetat)):
            thetat[i] = coeff[i][0] + coeff[i][1]*t+coeff[i][2]*t**2+coeff[i][3]*t**3
    # Draw the window onto the screen.
    pygame.display.update()
    mainClock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            coeff = updategoal(pos,thetat,T,lengths,XPosition,YPosition,T_pyOrg_o)
            t = 0
