import os
import numpy as np
from numpy import pi
import pygame as pg
from .brain import Brain
from random import randrange


LIDAR_ANGLES = (
    pi/2,     # Front
    pi/3,     # Front-right 1
    pi/4,     # Front-right 2
    2*pi/3,   # Front-left 1
    3*pi/4,   # Front-left 2
    0,        # Right
    pi,       # Left
    5*pi/3,   # Back-right 1
    4*pi/3,   # Back-left 1
)

abs = lambda x: x if x >= 0 else -x

sgn = lambda x: x / abs(x)

def bound(x, min_val, max_val):
    return max(min(x, max_val), min_val)

def hex_colour(x):
    return f'{hex(x[0])[2:]:0<2}{hex(x[1])[2:]:0<2}{hex(x[2])[2:]:0<2}'

cyl2cart = lambda cyl: np.array([cyl[0] * np.cos(cyl[1]), cyl[0] * np.sin(cyl[1]), cyl[2]])


class Car(pg.sprite.Sprite):
    def __init__(self, parent, lidars: tuple = LIDAR_ANGLES):
        super().__init__()
        
        # Setters
        self.parent = parent
        self.screen = parent.screen
        self.x, self.y, self.a = parent.track.start_pos.values()
        self.vx, self.va = 0, 0
        self.w, self.h = parent.w, parent.h
        self.lidars = lidars
        self.measurement = np.zeros(len(lidars))
        self.name = hex(randrange(1048576, 16777215))[2:]
        self.cycles = int(os.environ['EPOCH_CYCLES'])
        
        # Reset
        self.rot = False
        self.lin = False
        self.alive = True
        self.score = 0
        self.checkpoints = []
        self.finish_flag = False
        
        # Get image
        self.img = pg.image.load(os.path.join(os.environ['GAME_DIR'], f'bin\images\car.png'))
        self.image = self.img.convert()
        self.rect = self.image.get_rect()
        
        self.image = pg.transform.rotate(self.img.convert(), self.a)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def lose(self, msg: str = None):
        self.alive = False
        
        if msg is None:
            self.info(f'LOSE {self.score:.2f}')
        else:
            self.info(f'LOSE ({msg}) {self.score:.2f}')
    
    def info(self, msg):
        print(f'[{self.name}] - {msg}')
        
    def update(self):
        if not self.alive: return
        
        self.score = max(0, self.score - float(os.environ['POINT_DEC']))
        self.cycles -= 1
        if self.cycles <= 0:
            self.lose("GLOBAL TIMEOUT")
            return
        
        # Update velocity
        if not self.lin:
            if self.vx > 0:
                self.vx = max(0, self.vx - float(os.environ['LIN_DEC']))
            elif self.vx < 0:
                self.vx = min(0, self.vx + float(os.environ['LIN_DEC']))
        # Update position
        self.y -= self.vx * np.sin(self.a * pi / 180)
        self.y = bound(self.y, 0, self.h)
        self.x += self.vx * np.cos(self.a * pi / 180)
        self.x = bound(self.x, 0, self.w)
        self.lin = False
        
        # Update omega
        if not self.rot:
            if self.va > 0:
                self.va = max(0, self.va - float(os.environ['ANG_DEC']))
            elif self.va < 0:
                self.va = min(0, self.va + float(os.environ['ANG_DEC']))
        # Update angle
        self.a = (self.a + self.va) % 360
        self.rot = False
        
        # Update sprite
        self.image = pg.transform.rotate(self.img.convert(), self.a)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Handle bound-map
        px = hex_colour(self.parent.track.bounds[int(self.y), int(self.x)])
        if px == '000000':
            self.handle_out_of_bounds()
        elif px == '00ff00':
            self.handle_finish_line()
        elif px == 'ffffff':
            self.handle_road()
        else:
            self.handle_checkpoint(px)
            
        self.measure_lidar()
    
    def handle_finish_line(self):
        if self.finish_flag:
            return
        
        if len(self.checkpoints) >= self.parent.track.checkpoints:
            self.score += 20
            self.checkpoints = []
            # self.alive = False
            self.info(f'Finish Line {self.score:.2f}')
        else:
            self.score = max(0, self.score - 5)
            self.lose(f'FINISHED W/ NOT ENOUGH CHECKPOINTS {len(self.checkpoints)}/{self.parent.track.checkpoints}')
        
        self.finish_flag = True
    
    def handle_out_of_bounds(self):
        self.lose("OUT OF BOUNDS")
    
    def handle_road(self):
        self.finish_flag = False
    
    def handle_checkpoint(self, checkpoint):
        if checkpoint not in self.checkpoints:
            self.checkpoints.append(checkpoint)
            self.score += 1
    
    def left(self):
        self.rot = True
        self.va += float(os.environ['ANG_ACC'])
        self.va = min(self.va, float(os.environ['ANG_VEL']))
        
    def right(self):
        self.rot = True
        self.va -= float(os.environ['ANG_ACC'])
        self.va = max(self.va, -float(os.environ['ANG_VEL']))
        
    def forward(self):
        self.lin = True
        self.vx += float(os.environ['LIN_ACC'])
        self.vx = min(self.vx, float(os.environ['LIN_VEL']))
        
    def backward(self):
        self.lin = True
        self.vx -= float(os.environ['LIN_ACC'])
        self.vx = max(self.vx, -float(os.environ['LIN_VEL']))

    def measure_lidar(self):
        res = []
        for l in self.lidars:
            l = (l + pi * self.a / 180) % (2 * pi)
            r = 0
            
            while hex_colour(self.parent.track.bounds[int(r * np.cos(l) + self.y), int(r * np.sin(l) + self.x)]) != '000000':
                r += 1
            res.append(r)
        
        self.measurement = np.array(res)
        return
    
    def __lt__(self, other):
        return self.score < other.score
    
    def __le__(self, other): 
        return self.score <= other.score
        
    def __gt__(self, other):
        return self.score > other.score
    
    def __ge__(self, other):
        return self.score >= other.score
        
    def __str__(self):
        return self.brain.name

    def __float__(self):
        return self.score


class ComputerCar(Car):
    def __init__(self, parent, brain: Brain = None, deadline: int = 150):    
        super().__init__(parent)
        
        self.deadline = deadline
        self.life = deadline
        
        if brain is None:
            self.brain = Brain(self.name, len(self.lidars), 3, [12, 6, 4], 4)
        else:
            self.brain = brain
    
    def handle_checkpoint(self, checkpoint):
        super().handle_checkpoint(checkpoint)
        self.life = self.deadline
    
    def update(self):
        if not self.alive: return
        
        self.life -= 1
        
        resp = self.brain.calculate(self.measurement)
        if resp[0] > resp[1] > 0.2:
            self.forward()
        elif resp[1] > resp[0] > 0.2:
            self.backward()
        
        if resp[2] > resp[3] > 0.2:
            self.left()
        elif resp[3] > resp[2] > 0.2:
            self.right()
            
        super().update()
            
        if self.life <= 0: 
            self.lose(f'TIMEOUT')
            return
    
    def copy(self):
        return ComputerCar(self.parent, self.brain.copy(), self.deadline)
    
    def copy_mutated(self, mutation_rate: float):
        return ComputerCar(self.parent, self.brain.copy_mutated(mutation_rate), self.deadline)
    
    
class PlayerCar(Car):
    def update(self):
        super().update()
