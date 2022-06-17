import pygame as pg
from scripts import ComputerCar, PlayerCar, Track


class Engine:
    def __init__(self, level: str, n_cars: int = 1):
        super().__init__()
        pg.init()
        
        # Setters
        self.track = Track(level)
        self.w, self.h = self.track.w, self.track.h
        pg.display.set_caption(f"Gene Racer - {self.track.name}")
        # self.logo = pg.image.load(os.path.join(os.environ['GAME_DIR'], f'engine\images\logo32x32.png'))
        # pg.display.set_icon(self.logo)
        self.screen = pg.display.set_mode((self.w, self.h))
        self.running = False
        self.background = pg.Surface(self.screen.get_size())
        self.background.blit(self.track.texture.convert(), (0, 0))
        self.screen.blit(self.background, (0, 0))
        self.clock = pg.time.Clock()
        
        self.cars = [PlayerCar(self.screen, self.track.start_pos, self.w, self.h) for _ in range(n_cars)]
        
        # Sprites
        self.sprites = pg.sprite.RenderUpdates(self.cars)
    
    def mainloop(self):
        self.running = True
        pg.display.flip()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        self.cleanup()
            
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]  and not keys[pg.K_RIGHT]:   self.cars[0].left()
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:    self.cars[0].right()
        if keys[pg.K_UP]    and not keys[pg.K_DOWN]:    self.cars[0].forward()
        if keys[pg.K_DOWN]  and not keys[pg.K_UP]:      self.cars[0].backward()
        
        self.sprites.update()
        self.clock.tick(60)
    
    def draw(self):
        self.sprites.clear(self.screen, self.background)
        dirty = self.sprites.draw(self.screen)
        
        pg.display.update(dirty)

    def cleanup(self):
        pg.quit()