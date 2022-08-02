# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 17:38:24 2022

@author: Adithya Raj Mishra
"""

import pygame
import os
import serial



FPS = 60
WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Stick Rotation")

WHITE = (255,255,255)

TT_RACKET = pygame.image.load(os.path.join('res','tt-racket-sqr.jpg'))
theta = 0
dTheta = 2

def getDT(ser):
    
    t1 = ser.readline().decode().rstrip().split()
    t2 = ser.readline().decode().rstrip().split()
    while((len(t1)!= 3) or (len(t2)!= 3)):
        t1 = ser.readline().decode().rstrip().split()
        t2 = ser.readline().decode().rstrip().split()
        
    return -(float(t1[2]) + float(t2[2]))/120
        

def draw_game(theta):
    TT_RACKET_ROT = pygame.transform.rotate(TT_RACKET, theta)
    WIN.fill(WHITE)
    WIN.blit(TT_RACKET_ROT,(WIDTH/2.5 - int(TT_RACKET_ROT.get_width()/2) , HEIGHT/2 - int(TT_RACKET_ROT.get_height()/2) ))
    pygame.display.update()


def main():
    ser = serial.Serial('COM3',9600)
    run = True
    clock = pygame.time.Clock()
    theta = 0
    
    while run:
        clock.tick(FPS)
        theta = theta + getDT(ser)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                ser.close()
        draw_game(theta)
    pygame.quit()
    
    
    
if (__name__ =="__main__"):
    main()