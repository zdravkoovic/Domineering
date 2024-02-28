#!/bin/python
#   ___   ___   ____ ___    _  __                                                                                           
#  / _ ) / _ \ /  _// _ |  / |/ /                                                                                           
# / _  |/ , _/_/ / / __ | /    /                                                                                            
#/____//_/|_|/___//_/ |_|/_/|_/                                                                                             

# ______ __           __        __   __                  __              _                      _                ___    ____
#/_  __// /  ___     / /  ___  / /_ / /_ ___  ____   ___/ /___   __ _   (_)___  ___  ___  ____ (_)___  ___ _    / _ |  /  _/
# / /  / _ \/ -_)   / _ \/ -_)/ __// __// -_)/ __/  / _  // _ \ /  ' \ / // _ \/ -_)/ -_)/ __// // _ \/ _ `/   / __ | _/ /  
#/_/  /_//_/\__/   /_.__/\__/ \__/ \__/ \__//_/     \_,_/ \___//_/_/_//_//_//_/\__/ \__//_/  /_//_//_/\_, /   /_/ |_|/___/  
#                                                                                                    /___/                  

import sys,argparse,logging,os
from tkinter import messagebox,Tk
from board import Board,GameState,Move
from algorithms import minMax
import math

VERSION = "1.1.0"

#BOJE
COLOR_RED = (164, 48, 63)
COLOR_BLUE = (8, 61, 119)
COLOR_WHITE = (254, 249, 255)
COLOR_GRAY = (180, 180, 180)
COLOR_GREEN = (0,255,0)

#Parametri igre prosledjeni kroz komandnu liniju
parser = argparse.ArgumentParser("BRIAN - the BetteR domIneering Ai N")
parser.add_argument('--depth','-d',metavar="",type=int,help="The depth of BRIAN's algorithm",default=3)
parser.add_argument('--cols','-c',metavar="",type=int,help="Number of columns in the playing field",default=8)
parser.add_argument('--rows','-r',metavar="",type=int,help="Number of rows in the playing field",default=8)
parser.add_argument('--first','-f',metavar="",type=str,help="Who plays first ? X or O ? Red or Blue ?",choices=["X","O"],default="X")
parser.add_argument('--gamemode','-g',metavar="",type=int,help="0:Human vs Human, 1:Human vs AI, 2:AI vs Human, 3:AI vs AI",choices=[0,1,2,3],default=1)
parser.add_argument('--version','-v',action="version",version=VERSION)
parser.add_argument('--log','-l',help="Log everything in the shell",action="count",default=0)

args = parser.parse_args()

DEPTH = args.depth
GAMEMODE = args.gamemode

if args.log == 1:
    logging.basicConfig(level = logging.INFO)

#Importing pygame with the hide flag
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

#Velicina ekrana
screen_size = (width, height) = 600,600
#Velicine jednog polja
(dx,dy) = (width/args.cols,height/args.rows)

#Incijalizacija engine-a
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.fill(COLOR_WHITE)

logging.info("Pygame initialised succesfully !")
logging.info("Brian is initialized and ready to play !")
logging.info("Stats : DEPTH={}, COLS={}, ROWS={}".format(DEPTH,args.cols,args.rows))

#Racuna poziciju kliknutu na tabli
def calculatePosition(x,y):
    row = int(y//dy)
    col = int(x//dx)
    return (row,col)

#Funkcija za crtanje table
def drawBoard(board:Board,bestMove:Move):
    for i in range(0,args.rows):
        for j in range(0,args.cols):
            if((i%2==0 and j%2==0) or (i%2==1 and j%2==1)):
                pygame.draw.rect(screen,COLOR_GRAY,rect = pygame.Rect(j*dx,i*dy,dx,dy))
            pygame.draw.rect(screen,COLOR_GRAY,rect = pygame.Rect(j*dx,i*dy,dx,dy),width=1)
            
            padding = 10
            radius = 10

            if(board.drawingBoard[i][j] == 'XL'):
                pygame.draw.rect(screen,COLOR_RED,rect = pygame.Rect(j*dx+padding,i*dy,dx-2*padding,dy-padding),border_bottom_left_radius=radius,border_bottom_right_radius=radius)
            if(board.drawingBoard[i][j] == 'OL'):
                pygame.draw.rect(screen,COLOR_BLUE,rect = pygame.Rect(j*dx + padding,i*dy+padding,dx,dy-2*padding),border_bottom_left_radius=radius,border_top_left_radius=radius)
            if(board.drawingBoard[i][j] == 'XH'):
                pygame.draw.rect(screen,COLOR_RED,rect = pygame.Rect(j*dx+padding,i*dy+padding,dx-2*padding,dy),border_top_left_radius=radius,border_top_right_radius=radius)
            if(board.drawingBoard[i][j] == 'OR'):
                pygame.draw.rect(screen,COLOR_BLUE,rect = pygame.Rect(j*dx,i*dy+padding,dx-padding,dy-2*padding),border_bottom_right_radius=radius,border_top_right_radius=radius)
    
    pygame.draw.rect(screen,COLOR_GREEN,rect = pygame.Rect(bestMove.col*dx,bestMove.row*dy,dx,dy))
    if board.turn % 2 == 0:
        pygame.draw.rect(screen,COLOR_GREEN,rect = pygame.Rect(bestMove.col*dx,(bestMove.row-1)*dy,dx,dy))
    else:
        pygame.draw.rect(screen,COLOR_GREEN,rect = pygame.Rect((bestMove.col + 1)*dx,bestMove.row*dy,dx,dy))

    pygame.display.flip()


#Inicijalizacija table i igre
board = Board(args.cols,args.rows,args.first)
bestMove = Move(-1,-1)

#AI vs AI varijanta
if GAMEMODE == 3 :
    end = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    end = False
                    board = Board(args.cols,args.rows,args.first)
                    screen.fill(COLOR_WHITE)

        while(board.getState() == GameState.PLAYING):
            if board.turn < 10:
                (row,col,eval) = minMax(board,-math.inf,math.inf,DEPTH-1)
            else:
                (row,col,eval) = minMax(board,-math.inf,math.inf,DEPTH)
            board.playMove(Move(row,col))
            logging.info(str(row) + " " + str(col) + " " + str(eval))

            screen.fill(COLOR_WHITE)
            drawBoard(board,bestMove)
        
        if(board.getState() == GameState.XWON and end == False):
            end = True
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Game won !","Player X won !")

        if(board.getState() == GameState.OWON and end == False):
            end = True  
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Game won !","Player O won !")

else:
    end = False
    if(GAMEMODE == 2):
        screen.fill(COLOR_WHITE)
        drawBoard(board,bestMove)
        (row,col,eval) = minMax(board,-math.inf,math.inf,DEPTH)
        board.playMove(Move(row,col))    
        logging.info(str(row) + " " + str(col) + " " + str(eval))

    #Glavna petlja
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    board = Board(args.cols,args.rows,args.first)
                    screen.fill(COLOR_WHITE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                (mx,my) = pygame.mouse.get_pos()
                (row,col) = calculatePosition(mx,my)

                if(board.getState() == GameState.PLAYING):
                    move = Move(row,col)
                    flag = board.playMove(move)
                    if flag is True and GAMEMODE != 0:
                        drawBoard(board,bestMove)
                        screen.fill(COLOR_WHITE)
                        (row,col,eval) = minMax(board,float(-math.inf),float(math.inf),DEPTH)
                        board.playMove(Move(row,col))
                        logging.info(str(row) + " " + str(col) + " " + str(eval))

                        if(board.getState() == GameState.XWON and end == False):
                            end = True
                            root = Tk()
                            root.withdraw()
                            messagebox.showinfo("Game won !","Player X won !")

                        if(board.getState() == GameState.OWON and end == False):
                            end = True  
                            root = Tk()
                            root.withdraw()
                            messagebox.showinfo("Game won !","Player O won !")

        drawBoard(board,bestMove)
