import cv2
import numpy as np
from collections import defaultdict
import random

class BriksGame:
    def __init__(self, h=600, w=810, game_speed=60):
        #this one is for the whole image
        self.h = 600
        self.w = 810

        #the game speed => movement speed
        self.game_speed = game_speed

        #on a un rectangle du coup => w,h
        self.cell_h = 30
        self.cell_w = 150

        #colors
        self.grid_color = (1., 1., 1.)  
        self.racket_color = (0.7, 0.3, 0.7) 
        self.ball_color = (0., 0., 1.)
        self.brik_color = [ (0.8, 0.4, 0.5),(0.8, 0.5, 0.3), (0.8, 0.5, 0.4 ), (0.9, 0.5, 0.5), 
                            (0.9, 0.6, 0.7 ), (0.8, 0.6, 0.5), (1., 0.7, 0.6)]

        #creation de l'image
        self.img = np.ones((h, w, 3))*self.grid_color
        for y in range(0, h, self.cell_h):
            for x in range(0, w, self.cell_w):
                self.color_square((y, x), self.grid_color)

        #position initial de la raquette
        self.initial_pos = (self.h-self.cell_h*2, (self.w-self.cell_w)//2)
        self.racket = self.initial_pos
        #creation de la raquette 
        self.color_square(self.racket, self.racket_color)

        #creation des briques
        self.buildBriks()

        #position + creation de la ball 
        self.ball_position = (self.h//2, self.w//2)
        self.drawBall(self.ball_position, self.ball_color)
        
        #map pour sauvegarder les mouvements
        self.move_map = defaultdict(lambda: (0, 0))
        self.move_map.update({
            'left': (0, -self.cell_h),
            'right': (0, self.cell_h),
            'up': (-self.cell_h, 0),
            'down': (self.cell_h, 0)
        })

    #ceci est principalement pour colorier une matrice à partir de sa position
    def color_square(self, pos, color):
        y, x = pos
        self.img[y:y+self.cell_h, x:x+self.cell_w] = color

    #creation des briques
    def buildBriks(self, num_lines = 7, num_briks = 5):
        self.num_lines = num_lines
        self.num_briks = num_briks
        self.space = 35

        #ceci a ete fait apres plusieurs tests
        self.space_h=155
        #we we'll choose the width of the briks according to their num total
        w_brik = self.w//((self.cell_w//3)*self.num_briks)
        h_brik = self.cell_h
        brik_y = h_brik 
        #the space between 2 lines
        space = (w_brik + self.cell_h//2 + self.space_h)//(self.num_briks*2)

        for i in range(self.num_lines):
            brik_x = w_brik + space
            for j in range(self.num_briks):
                self.color_square((brik_y, brik_x), self.brik_color[i])
                brik_x = brik_x + self.space_h

            brik_y = brik_y + self.space

    #creation de la ball
    def drawBall(self, pos, color):
        b, a = pos
        r = 20
        R = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        R1 = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
        epsilon = np.sqrt(r)
        EPSILON = np.sqrt(R1)
        for y in range(self.h):
            for x, r in zip(range(self.w),R) :
                
                print(abs((x-a)**2 + (y-b)**2 - r**2))
                if (abs((x-a)**2 + (y-b)**2 - r**2) <= EPSILON.any()) :
                    self.img[y, x] = color
        
    #movement => ça bouge pas verticalement pour le moment
    def move(self):
        delta = self.move_map[self.direction]

        new_y, new_x = self.racket[0]+delta[0], self.racket[1]+delta[1]

        if new_y <(self.h - self.cell_h) and new_y >self.cell_h and  new_x <self.w-self.cell_w*9//10 and new_x >=0:
            self.color_square(self.racket, self.grid_color)
            self.color_square((self.racket[0], new_x), self.racket_color)
            self.racket = (self.racket[0], new_x)
        
    #le jeu !
    def play(self):
        UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 2490368, 2424832, 2621440, 2555904
        while(1):
            cv2.imshow('Break briks', self.img)
            k = cv2.waitKeyEx(self.game_speed)
            self.direction = ''
            if k == UP_KEY :
                self.direction = 'up'
            elif k == LEFT_KEY :
                self.direction = 'left'
            elif k == DOWN_KEY :
                self.direction = 'down'
            elif k == RIGHT_KEY :
                self.direction = 'right'
            if self.direction != '':
                self.move()
        cv2.destroyAllWindows()

#main ^^
briksGame = BriksGame()
briksGame.play()