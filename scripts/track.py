import os, json
import cv2 as cv
import numpy as np
import pygame as pg



class Track:
    def __init__(self, name: str):
        # Setters
        self.name = name
        
        self.level_dir = os.path.join(os.environ['GAME_DIR'], f'bin\levels\{self.name}')
        
        # =============== Read level data ===============
        # Ream images
        self.texture = pg.image.load(os.path.join(self.level_dir, 'texture.png'))   
        self.bounds = np.asarray(cv.imread(os.path.join(self.level_dir, 'bounds.png')), dtype=np.uint8)
        
        # Parameters
        with open(os.path.join(self.level_dir, 'parameters.json'), 'r') as f:
            tmp = json.load(f)
            self.h, self.w = tmp['height'], tmp['width']
            self.start_pos = tmp['start']
            self.checkpoints = tmp['checkpoints']
