import pygame as pg
import numpy as np
from pygame import draw
from BackEnd import *
import time
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)
pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

GRIDCOLOR = (255,255,255)
BACKGROUND = (0,0,0)

XCOLOR = GRIDCOLOR
OCOLOR = GRIDCOLOR

XRATIO = 0.8
ORATIO = 0.8

GRIDSIZE = 150
BOARDSIZE = GRIDSIZE * 3

running = True

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
framerate = 240
screen.fill(BACKGROUND)

WIDTH_OFFSET, HEIGHT_OFFSET = (SCREEN_WIDTH - BOARDSIZE)/2, (SCREEN_HEIGHT - BOARDSIZE)/2

def render_symbols():
    X = pg.Surface((GRIDSIZE*XRATIO,GRIDSIZE*XRATIO))
    O = pg.Surface((GRIDSIZE*ORATIO,GRIDSIZE*ORATIO))
    X_rect = X.get_rect()
    pg.draw.circle(O,OCOLOR,O.get_rect().center,GRIDSIZE*ORATIO/2,width=5)
    pg.draw.line(X,XCOLOR,np.array(X_rect.bottomleft),np.array(X_rect.topright),width =5)
    pg.draw.line(X,XCOLOR,np.array(X_rect.bottomright),np.array(X_rect.topleft),width =5)
    return X,O

def render_board():
    background = pg.Surface((BOARDSIZE,BOARDSIZE))
    board_rect = []
    for i in range(0,BOARDSIZE,GRIDSIZE):
        rank = []
        for j in range(0,BOARDSIZE,GRIDSIZE):
            rect = pg.Rect(j,i,GRIDSIZE,GRIDSIZE)
            pg.draw.rect(background,GRIDCOLOR,rect,width=1)
            rank.append(pg.Rect(WIDTH_OFFSET+j,HEIGHT_OFFSET+i,GRIDSIZE,GRIDSIZE))
        board_rect.append(rank)
    return background,board_rect

def mouseOver(mouse_pos,board_rect): #returns the grid number over which the mouse currently is.
    for i, rank in enumerate(board_rect):
        for j,grid in enumerate(rank): 
            if grid.collidepoint(mouse_pos):
                return (i,j)
    return False

def draw_symbol(screen,curr_player,pos,board_rect):
    symbol = X if curr_player else O
    screen.blit(symbol,symbol.get_rect(center=board_rect[pos[0]][pos[1]].center))

backboard,board_rect = render_board()
X,O = render_symbols()

current_player = False #True for X, False for O

pg.Surface.blit(screen,backboard,(WIDTH_OFFSET,HEIGHT_OFFSET))
while running:
    if not current_player: #AI's move
        AI_move = bestMove(table,current_player)[0]
        table[AI_move[0]][AI_move[1]] = 'O'
        draw_symbol(screen,current_player,AI_move,board_rect)
        if scorePosition(table)==-10:##check if AI has won
            print('O has won')
            running = False
        elif scorePosition(table)==0: ##check draw
            print("It's a draw")
            running = False
        current_player = not current_player
    for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                
                square = mouseOver(event.pos,board_rect)
                if not square:
                    continue

                if not table[square[0]][square[1]]: ##Square is empty
                    draw_symbol(screen,current_player,square,board_rect)
                    curr_symbol = 'X' #if current_player else 'O'
                    table[square[0]][square[1]] = curr_symbol
                    current_player = not current_player

                    if scorePosition(table)==10: ##check if player has won
                        print(curr_symbol,'X won!')
                        running=False

                    elif scorePosition(table)==0: ##check draw
                        print("It's a draw")
                        running = False
    pg.display.flip()   