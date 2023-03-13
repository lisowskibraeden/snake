import pygame
import time
import threading
from random import randint, seed
from datetime import datetime
from copy import deepcopy

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

seed(datetime.now().timestamp())
SCREEN_X = 1013
SCREEN_Y = 1013
BOARD_X_COUNT = int((SCREEN_X  - 5)/16)
BOARD_Y_COUNT = int((SCREEN_Y - 5)/16)

tps = 1 / 8

class SnakeGame: 
    def __init__(self) -> None:
        self.board = [([0] * BOARD_X_COUNT) for _ in range(BOARD_Y_COUNT)]
        self.game_over = False
        self.score = 0
        self.character = [[randint(0, BOARD_X_COUNT - 1), randint(1, BOARD_Y_COUNT - 1)]]
        self.cherry = [randint(0, BOARD_X_COUNT - 1), randint(0, BOARD_Y_COUNT - 1)]
        self.ticking = False
        self.direction = 0
        self.runningGame = threading.Thread(target=self.tick)
        self.growing = False
        self.spawn_init()
    
    def tick(self):
        while self.ticking and not self.game_over:
            copy = [self.character[0][0], self.character[0][1]]
            self.character.insert(0, copy)
            match self.direction:
                case 0:
                    # Right
                    self.character[0][0] += 1
                case 1:
                    # Down
                    self.character[0][1] += 1
                case 2:
                    # Left
                    self.character[0][0] -= 1
                case 3:
                    # Up
                    self.character[0][1] -= 1
            if self.character[0][0] < 0 or self.character[0][0] >= len(self.board) or self.character[0][1] < 0 or self.character[0][1] >= len(self.board[0]):
                self.game_over = True
            elif self.board[self.character[0][0]][self.character[0][1]] == -1:
                self.score += 1
                self.spawn_cherry()
                pass
            elif self.board[self.character[0][0]][self.character[0][1]] == 1:
                self.game_over = True
            else:
                self.board[self.character[-1][0]][self.character[-1][1]] = 0
                del self.character[-1]
            if not self.game_over:
                self.board[self.character[0][0]][self.character[0][1]] = 1
                time.sleep(tps)

    def start_tick(self):
        if not self.ticking:
            self.ticking = True
            self.runningGame.start()

    def finish(self):
        self.ticking = False
        self.runningGame.join()

    def spawn_init(self):
        self.board[self.character[0][0]][self.character[0][1]] = 1
        self.spawn_cherry()

    def spawn_cherry(self):
        while self.board[self.cherry[0]][self.cherry[1]] > 0 or self.board[self.cherry[0]][self.cherry[1]] == -1:
            self.cherry = [randint(0, BOARD_X_COUNT - 1),randint(0, BOARD_Y_COUNT - 1)]
        self.board[self.cherry[0]][self.cherry[1]] = -1

    def printBoard(self):
        for i in range(0, len(self.board)):
            # print(i)
            for j in range(0, len(self.board)):
                # print(j, end="/")
                print (self.board[i][j], end = ' ')
            print ()
        print()

def graphics():
    pygame.init()
    # logo = pygame.image.load("logo.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
    pygame.font.init() 
    myfont = pygame.font.SysFont('Arial', 30)
    running = True
    screen.fill((0, 0, 0))
    borderSize = 4
    game = SnakeGame()
    square = pygame.Rect(0, 0, 12, 12)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.finish()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.start_tick()
            if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if game.direction != 2:
                            game.direction = 0
                    elif event.key == K_DOWN:
                        if game.direction != 3:
                            game.direction = 1
                    elif event.key == K_LEFT:
                        if game.direction != 0:
                            game.direction = 2
                    elif event.key == K_UP:
                        if game.direction != 1:
                            game.direction = 3
                    
        s = pygame.Surface((700,700))
        s.set_alpha(5)
        screen.fill((0, 0, 0))
        screen.blit(s, (0,0))
        for i_idx, i in enumerate(game.board):
            for x_idx, x in enumerate(game.board[i_idx]):
                if x > 0:
                    square.x = i_idx * borderSize + i_idx * square.width + borderSize
                    square.y = x_idx * borderSize + x_idx * square.height + borderSize
                    pygame.draw.rect(screen, [255, 255, 255], square)
                elif x == -1:
                    square.x = i_idx * borderSize + i_idx * square.width + borderSize
                    square.y = x_idx * borderSize + x_idx * square.height + borderSize
                    pygame.draw.rect(screen, [220, 20, 60], square)
                # else: 
                #     square.x = i_idx * borderSize + i_idx * square.width + borderSize
                #     square.y = x_idx * borderSize + x_idx * square.height + borderSize
                #     pygame.draw.rect(screen, [220, 20, 255], square)
        pygame.display.flip()
        running = not game.game_over
    game.finish()

graphics()