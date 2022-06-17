import os, json
import cv2 as cv
import numpy as np
import pygame as pg



class Track:
    def __init__(self, name: str):
        # Setters
        self.name = name
        
        self.level_dir = os.path.join(os.environ['GAME_DIR'], f'levels\{self.name}')
        
        # =============== Read level data ===============
        # Bounds map
        cap = cv.VideoCapture(os.path.join(self.level_dir, 'bounds.gif'))
        _, self.bounds = cap.read()
        cap.release()      
        self.bounds = np.asarray(self.bounds, dtype=np.uint8)[:,:,2]
        
        # Parameters
        with open(os.path.join(self.level_dir, 'parameters.json'), 'r') as f:
            tmp = json.load(f)
            self.h, self.w = tmp['height'], tmp['width']
            self.start_pos = tmp['start']
            self.checkpoints = tmp['checkpoints']
        
        # Track texture
        self.texture = pg.image.load(os.path.join(self.level_dir, 'texture.png'))
