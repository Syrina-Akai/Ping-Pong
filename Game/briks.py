import cv2
import numpy as np
from collections import defaultdict
from queue import Queue

class BriksGame:
    def __init__(self, h=600, w=810, game_speed=60):
        self.game_speed = game_speed
        self.cell_h = 30
        self.cell_w = 150
        self.cell_Move_x = 30
        self.h = 600
        self.w = 810
        self.grid_color = (1., 1., 1.)  # white
        self.racket_color = (1., 0., 0.)
        self.img = np.ones((h, w, 3))*self.grid_color
        for y in range(0, h, self.cell_h):
            for x in range(0, w, self.cell_w):
                self.color_square((y, x), self.grid_color)
        self.initial_pos = (self.h-self.cell_h*2, self.w-self.cell_w*2)
        self.racket = self.initial_pos
        self.color_square(self.racket, self.racket_color)
        
        self.move_map = defaultdict(lambda: (0, 0))
        self.move_map.update({
            'left': (0, -self.cell_h),
            'right': (0, self.cell_h),
            'up': (-self.cell_h, 0),
            'down': (self.cell_h, 0)
        })

    def color_square(self, pos, color):
        y, x = pos
        self.img[y:y+self.cell_h, x:x+self.cell_w] = color

    def move(self):
        delta = self.move_map[self.direction]
        
        new_y, new_x = self.racket[0]+delta[0], self.racket[1]+delta[1]
        if new_y <self.h-self.cell_h and new_y >self.cell_h and  new_x <self.w-self.cell_w*9//10 and new_x >=0:
            self.color_square(self.racket, self.grid_color)
            self.color_square((new_y, new_x), self.racket_color)
            self.racket = (new_y, new_x)
        
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

briksGame = BriksGame()
briksGame.play()