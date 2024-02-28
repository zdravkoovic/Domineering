from algorithms import minMax
from board import Board,Move
import math

board = Board(8,8,'X')

def play():
    (row,col,eval) =minMax(board,-math.inf,math.inf,5)
    board.playMove(Move(row,col))

def test():
    for x in range(5):
        play()

play()