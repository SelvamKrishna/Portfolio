import pygame as pg
from pygame.locals import *
import random

{"CONSTANTS"}
WIDTH = 900
HEIGHT = 900
TILE = 10
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Food:
    def __init__(self) -> None:
        self.pos = self.RandomLoc()
        print(self.pos)

    def RandomLoc(self):
        xPos = random.randint(0, WIDTH // TILE) * TILE
        yPos = random.randint(0, WIDTH // TILE) * TILE

        return [xPos, yPos]

    def PlaceFood(self, screen):
        self.body = pg.Rect(self.pos[0], self.pos[1], TILE, TILE)
        pg.draw.rect(screen, WHITE, self.body)


class Snake:
    def __init__(self) -> None:
        self.length = 5
        self.body = []

        self.CreateSnake()
        self.head = self.body[0]

        self.up = [0, -1]
        self.down = [0, 1]
        self.left = [-1, 0]
        self.right = [1, 0]

        self.direction = self.right
        self.isMoving = True

    def CreateSnake(self):
        self.body.append(pg.Rect(WIDTH // 2, HEIGHT // 2, TILE, TILE))

        for i in range(self.length):
            if i != 0:
                segment = pg.Rect(self.body[i-1].x,
                                  self.body[i-1].y, TILE, TILE)
                self.body.append(segment)

    def DisplaySnake(self, screen):
        for segment in self.body:
            pg.draw.rect(screen, WHITE, segment)

    def Move(self):
        self.head.x += self.direction[0] * TILE
        self.head.y += self.direction[1] * TILE

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

            if i > 1 and self.head.colliderect(self.body[i]):
                print(True)
                self.isMoving = False

        self.IsPlaying()

    def AddBody(self):
        segment = pg.Rect(self.body[-1].x, self.body[-1].y, TILE, TILE)
        self.body.append(segment)

    def IsPlaying(self):
        if self.head.left <= 0:
            self.isMoving = False
        elif self.head.right >= WIDTH:
            self.isMoving = False
        elif self.head.top <= 0:
            self.isMoving = False
        elif self.head.bottom >= HEIGHT:
            self.isMoving = False


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("Snake Game")

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.Running = True

        self.snake = Snake()
        self.food = Food()

    def MainLoop(self):
        while self.Running:
            pg.display.update()

            for event in pg.event.get():
                if event.type == QUIT:
                    self.Running = False
                    break

            self.screen.fill(BLACK)
            self.snake.DisplaySnake(self.screen)
            self.food.PlaceFood(self.screen)

            if self.snake.isMoving:
                self.snake.Move()
            if self.snake.head.colliderect(self.food.body):
                self.food.pos = self.food.RandomLoc()
                self.snake.length += 1
                self.snake.AddBody()
            self.KeyHandler(pg.key.get_pressed())

            pg.display.flip()
            self.clock.tick(FPS)

        from sys import exit
        pg.quit()
        exit()

    def KeyHandler(self, key):
        if key[K_ESCAPE]:
            self.Running = False
        elif key[K_w] or key[K_UP] and self.snake.direction != self.snake.down:
            self.snake.direction = self.snake.up
        elif key[K_s] or key[K_DOWN] and self.snake.direction != self.snake.up:
            self.snake.direction = self.snake.down
        elif key[K_a] or key[K_LEFT] and self.snake.direction != self.snake.right:
            self.snake.direction = self.snake.left
        elif key[K_d] or key[K_RIGHT] and self.snake.direction != self.snake.left:
            self.snake.direction = self.snake.right


game = Game()
game.MainLoop()
