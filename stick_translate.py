# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 21:21:30 2022

@author: Adithya Raj Mishra
"""

import pygame
import os
import serial
import numpy as np


FPS = 60
WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Stick Translation")

WHITE = (255,255,255)

TT_RACKET = pygame.image.load(os.path.join('res','tt-racket-sqr.jpg'))


 
def getDT(ser,queue):
    
    t1 = ser.readline().decode().rstrip().split()
    t2 = ser.readline().decode().rstrip().split()
    while((len(t1)!= 3) or (len(t2)!= 3)):
        t1 = ser.readline().decode().rstrip().split()
        t2 = ser.readline().decode().rstrip().split()
    
    t1 = np.array(t1)
    t1 = t1.astype('float64')
    t2 = np.array(t2)
    t2 = t2.astype('float64')
    meanQ = np.mean(queue,axis = 0)
    queue = np.delete(queue,0,axis = 0)
    queue = np.delete(queue,0,axis = 0)
    
    queue = np.append(queue,[t1,],axis = 0)
    queue = np.append(queue,[t2,],axis = 0)
    
    print(np.shape(queue))
    
    
    meanQ = meanQ.astype('float64')
    
    return ((((queue[-2] + queue[-1])/2) - meanQ),queue)

def getVT(vD,queue,f):
    meanQ = np.mean(queue,axis = 0)
    queue = np.delete(queue,0,axis = 0)
    newVel = queue[-1] + vD*f
    queue = np.append(queue,[newVel,],axis = 0)
    return ((queue[-1] - meanQ),queue)
    
   
    
    
      
def getSample(ser,n):
    listA = []
    listB = []
    for i in range(n):
        listA_i = ser.readline().decode().rstrip().split()
        while(len(listA_i) !=3):
            listA_i = ser.readline().decode().rstrip().split()
        if(i == 0):
            listB.append([0,0,0])
        else:
            listB.append([listB[-1][0] + (float)(listA_i[0]),listB[-1][1] + (float)(listA_i[1]),listB[-1][2] + (float)(listA_i[2])])
        listA.append(listA_i)
            
    
    listA = np.array(listA)
    listA = listA.astype('float64')
    listB = np.array(listB)
    listB = listB.astype('float64')
    
    return (listA,listB)

def draw_game(r):
   
    WIN.fill(WHITE)
    WIN.blit(TT_RACKET,(WIDTH/2.5 - int(TT_RACKET.get_width()/2) + r[0], HEIGHT/2 - int(TT_RACKET.get_height()/2) - r[1]))
    pygame.display.update()


def main():
    ser = serial.Serial('COM3',9600)
    run = True
    clock = pygame.time.Clock()
    
    
    v = [0,0,0]
    v = np.array(v)
    v = v.astype('float64')
    r = [0,0,0]
    r = np.array(r)
    r = r.astype('float64')
    accList,velList = getSample(ser,50)
    
   
    
    
    while run:
        clock.tick(FPS)
        vD,accList = getDT(ser, accList)
        v,velList = getVT(vD,velList,1)
        v = np.around(v,decimals = 2)
        r = r + v
        r = np.around(r,decimals = 2)
        print(v[1])
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                ser.close()
        draw_game(r)
    pygame.quit()
    
    
    
if (__name__ =="__main__"):
    main()