import pygame as pg
import sys, random

pg.init()

X_CELLS = 200
Y_CELLS = 200
CELL_SIZE = 4
DEAD_COLOR = (0, 0, 0)
LIVE_COLOR = (255, 255, 255)
FPS = 30

class World:
    def __init__(self) -> None:
        self.world = self.create(isRandom = True)

    def display(self, screen: pg.Surface) -> None:
        for row in range(Y_CELLS):
            for col in range(X_CELLS):
                if self.world[(row, col)] == True:
                    cell = pg.Rect(row * CELL_SIZE + 1, col * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1)
                    pg.draw.rect(screen, LIVE_COLOR, cell)

    def update(self) -> None:
        nextGen = {}
        for row in range(Y_CELLS):
            for col in range(X_CELLS):

                relative = 0
                for xShift in range(3):
                    for yShift in range(3):
                        if self.world[((row + xShift - 1) % X_CELLS, (col + yShift - 1) % Y_CELLS)] == True: 
                            relative += 1

                if self.world[(row, col)] == True:
                    relative -= 1
                    nextGen[(row, col)] = not(relative < 2 or relative > 3)
                else: nextGen[(row, col)] = relative == 3

        self.world = nextGen

    def create(self, isRandom = True) -> dict:
        world = {}
        for x in range(Y_CELLS):
            for y in range(X_CELLS):
                if isRandom: world[(x, y)] = random.choice((True, False))
                else: world[(x, y)] = False  
                
        return world

class Game:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode((X_CELLS * CELL_SIZE, Y_CELLS * CELL_SIZE))
        pg.display.set_caption("Convoy's Game of Life")

        self.world = World()
        self.running = True
        self.clock = pg.time.Clock()

    def update(self) -> None:
        self.world.update()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT: self.kill()
            
            self.world.update()
                
            self.screen.fill(DEAD_COLOR)
            self.world.display(self.screen)
            
            pg.display.update()
            self.clock.tick(FPS)

    def kill(self) -> None:
        self.running = False
        pg.quit()
        sys.exit()

Game().update()