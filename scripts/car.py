import os
import numpy as np
import pygame as pg


def bound(x, min_val, max_val):
    return max(min(x, max_val), min_val)


class Car(pg.sprite.Sprite):
    def __init__(self, screen, start_pos: dict, w, h):
        super().__init__()
        
        # Setters
        self.screen = screen
        self.x, self.y, self.a = start_pos.values()
        self.w, self.h = w, h
        
        # Commands
        self.rot = 0
        self.lin = 0
        
        # Get image
        self.img = pg.image.load(os.path.join(os.environ['GAME_DIR'], f'scripts\engine\images\car.png'))
        self.image = self.img.convert()
        self.rect = self.image.get_rect()
        
        self.update()
        
    def update(self):
        # print(self.x, self.y, self.a)
        
        if self.rot != 0:
            self.a += self.rot * float(os.environ['ANG_VEL'])
            self.a %= 360
            self.rot = 0
        
        self.image = pg.transform.rotate(self.img.convert(), self.a)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def left(self):
        self.rot = 1
        
    def right(self):
        self.rot = -1
        
    def forward(self):
        self.lin = 1
        
    def backward(self):
        self.lin = -1
    
    def draw(self):
        pass

class ComputerCar(Car):
    def update(self):
        self.y -= float(os.environ['LIN_VEL']) * np.sin(self.a * np.pi / 180)
        self.y = bound(self.y, 0, self.h)
        self.x += float(os.environ['LIN_VEL']) * np.cos(self.a * np.pi / 180)
        self.x = bound(self.x, 0, self.w)
        self.lin = 0
    
class PlayerCar(Car):
    def update(self):
        if self.lin != 0:
            self.y -= float(os.environ['LIN_VEL']) * np.sin(self.a * np.pi / 180) * self.lin
            self.y = bound(self.y, 0, self.h)
            self.x += float(os.environ['LIN_VEL']) * np.cos(self.a * np.pi / 180) * self.lin
            self.x = bound(self.x, 0, self.w)
            self.lin = 0
            
        super().update()
