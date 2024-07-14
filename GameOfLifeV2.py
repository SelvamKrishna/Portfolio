import pygame as pg
import numpy as np
from scipy import signal
import os
from datetime import datetime

# rule1 - (over-population)  : If an ALIVE cell has more than 3 ALIVE NEIGHBOURS it will DIE.
# rule2 - (under-population) : If an ALIVE cell has less than 2 ALIVE NEIGHBOURS it will DIE.
# rule3 - (reproduction)     : If a DEAD cell has exactly 3 ALIVE NEIGHBOURS it will be BORN.

# CONTROLS: 
# --> SPACE = pause
# --> S     = screenshot

# WHEN PAUSED
# --> C     = clear / create empty
# --> N     = next generation 
# --> LMB   = toggle cell state

WIDTH, HEIGHT = 1280, 720
CELL_SZ = 10

gridW = WIDTH // CELL_SZ
gridH = HEIGHT // CELL_SZ

generation = 0

def create_grid():
    return np.random.choice([0, 1], size=(gridH, gridW), p=[0.8, 0.2])

def update(grid):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    
    neighbours = signal.convolve2d(grid, kernel, mode='same', boundary='wrap')
    new_grid = np.zeros((gridH, gridW), dtype=int)
    new_grid[np.logical_and(grid == 1, np.logical_or(neighbours == 2, neighbours == 3))] = 1
    new_grid[np.logical_and(grid == 0, neighbours == 3)] = 1
    return new_grid

def draw_grid(screen, grid):
    for y in range(gridH):
        for x in range(gridW):
            color = (0, 0, 0) if grid[y, x] else (255, 255, 255)
            pg.draw.rect(screen, color, 
                         (x * CELL_SZ + 1, y * CELL_SZ + 1, CELL_SZ - 2, CELL_SZ - 2))
            
def setup():
    global screen
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Game of Life")
    return create_grid()

def save_screen(screen):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    currentTime = datetime.now()
    timeStr = currentTime.strftime("%Y%m%d%H%M%S")
    fileName = f"screenshots/life_{timeStr}.png"
    pg.image.save(screen, fileName)

def main():
    global generation
    grid = setup()
    clock = pg.time.Clock()
    running = True
    paused = False
    font = pg.font.Font(None, 36)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: paused = not paused
                elif event.key == pg.K_c and paused:
                    grid = np.zeros((gridH, gridW), dtype=int)
                    generation = 0
                elif event.key == pg.K_r and paused:
                    grid = create_grid()
                    generation = 0
                elif event.key == pg.K_s: save_screen(screen)
                elif event.key == pg.K_n and paused:
                    grid = update(grid)
                    generation += 1
            elif event.type == pg.MOUSEBUTTONDOWN and paused:
                if event.button == 1:
                    x, y = event.pos
                    gridX, gridY = x // CELL_SZ, y // CELL_SZ
                    grid[gridY, gridX] = 1 - grid[gridY, gridX]

        if not paused:
            grid = update(grid)
            generation += 1

        screen.fill((200, 200, 200))
        draw_grid(screen, grid)

        genText = font.render(f"Generation: {generation}", True, (0, 0, 0))
        screen.blit(genText, (10, 10))

        pauseText = font.render("PAUSED" if paused else "RUNNING", True, (255, 100, 100) if paused else (20, 200, 20))
        screen.blit(pauseText, (WIDTH - 120, 10))

        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == "__main__": main()