import pygame as pg
from pygame.locals import *
from random import choice

pg.init()

WIDTH: int = 1000
HEIGHT: int = 600
TITLE: str = "Pong"
FPS: int = 60
COLORS: dict = {"white": (255, 255, 255),
                "black": (20, 20, 20)}

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

PADDLE_WIDTH: int = 10
PADDLE_HEIGHT: int = 100

BALL_SIZE: int = 20
SPEED: int = 5


class Game():

    def __init__(self) -> None:
        self.ball = pg.Rect(WIDTH // 2 - BALL_SIZE // 2,
                            HEIGHT // 2 - BALL_SIZE // 2,
                            BALL_SIZE, BALL_SIZE)

        self.ball_speed: list = [
            choice((SPEED, -SPEED)), choice((SPEED, -SPEED))]

        self.player = pg.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT)

        self.opponent = pg.Rect(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                PADDLE_WIDTH, PADDLE_HEIGHT)

        self.findPos: bool = False
        self.clock = pg.time.Clock()
        self.running: bool = True

    def Mainloop(self):
        while self.running == True:

            for event in pg.event.get():
                if event.type == QUIT:
                    self.running: bool = False

            key = pg.key.get_pressed()

            self.PlayerLogic(key)
            self.KeyHandler(key)
            self.BallLogic()
            self.AILogic()
            self.DrawObj()

            self.clock.tick(FPS)
            pg.display.flip()

        self.ExitGame()

    def KeyHandler(self, key):
        if key[K_r]:
            self.Restart()
        if key[K_ESCAPE]:
            self.running: bool = False

    def BallLogic(self):
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.ball_speed[1] *= -1

        if self.ball.colliderect(self.opponent):
            self.ball_speed[0] *= -1

        if self.ball.colliderect(self.player):
            if (self.player.right - self.ball.left) < 10:
                self.ball_speed[0] *= -1

        if self.ball.right < -10 or self.ball.left > WIDTH + 10:
            self.Restart()

    def PlayerLogic(self, key):
        if (key[K_UP] or key[K_w]) and self.player.top > 0:
            self.player.y -= SPEED
        if (key[K_DOWN] or key[K_s]) and self.player.bottom < HEIGHT:
            self.player.y += SPEED

    def AILogic(self):
        if self.findPos == False:
            if self.opponent.centery > self.ball.centery and self.opponent.top > 0:
                self.opponent.y -= SPEED

            if self.opponent.centery < self.ball.centery and self.opponent.bottom < HEIGHT:
                self.opponent.y += SPEED

        if self.ball.colliderect(self.player):
            self.findPos: bool = True
            self.aiPredict: list = self.PredictAI()

        if self.findPos == True:
            if self.opponent.centery > self.aiPredict[1] and self.opponent.top > 0:
                self.opponent.y -= SPEED

            if self.opponent.centery < self.aiPredict[1] and self.opponent.bottom < HEIGHT:
                self.opponent.y += SPEED

    def PredictAI(self):
        betaPos: list = [self.ball.x, self.ball.y]
        betaDir: list = [self.ball_speed[0], self.ball_speed[1]]

        predicted: bool = False
        while predicted == False:
            betaPos[0] += betaDir[0]
            betaPos[1] += betaDir[1]

            if betaPos[1] <= 0 or betaPos[1] >= HEIGHT:
                betaDir[1] *= -1

            if betaPos[0] <= self.player.x:
                betaDir[0] *= -1

            if betaPos[0] == WIDTH - 55:
                predicted: bool = True

            if betaPos[0] < 50:
                self.findPos: bool = False
                break

        return betaPos

    def Restart(self):
        self.ball = pg.Rect(WIDTH // 2 - BALL_SIZE // 2,
                            HEIGHT // 2 - BALL_SIZE // 2,
                            BALL_SIZE, BALL_SIZE)

        self.ball_speed: list = [
            choice((SPEED, -SPEED)), choice((SPEED, -SPEED))]
        self.findPos: bool = False

    def DrawObj(self):
        screen.fill(COLORS["black"])
        pg.draw.ellipse(screen, COLORS["white"], self.ball)
        pg.draw.rect(screen, COLORS["white"], self.player)
        pg.draw.rect(screen, COLORS["white"], self.opponent)
        pg.draw.aaline(screen, COLORS["white"],
                       (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    def ExitGame(self):
        from sys import exit
        pg.quit()
        exit()


Game().Mainloop()