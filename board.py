from enum import Enum
import logging
from copy import deepcopy

#GAME STATE ENUM
class GameState(Enum):
    PLAYING = 1
    XWON = 2
    OWON = 3

class Move():
    row = -1
    col = -1

    def __init__(self,row,col):
        self.row = row
        self.col = col

class Board():
    
    boardState = []
    drawingBoard = []
    turn = 0
    lastMove:list[Move] = []

    #Inicira tablu
    def __init__(self,cols,rows,firstPlayer):
        self.cols = cols
        self.rows = rows
        self.turn = 0 if firstPlayer == "X" else 1
        self.lastMove = []
        self.boardState = [[str(' ') for _ in range(cols)] for _ in range(rows)]
        self.drawingBoard = [[str(' ') for _ in range(cols)] for _ in range(rows)]
    
    #Racuna broj slobodnih poteza za oba igraca
    def countAvailableMoves(self):
        brojac1 = 0
        brojac2 = 0

        for i in range(1,self.rows):
            for j in range(0,self.cols):
                if(self.boardState[i][j] == ' ' and self.boardState[i-1][j] == ' '):
                    brojac1 = brojac1 + 1
                
        for i in range(0,self.rows):
            for j in range(0,self.cols-1):
                if(self.boardState[i][j]== ' ' and self.boardState[i][j+1] == ' '):
                    brojac2 = brojac2 + 1
                
        return {"X":brojac1,"O":brojac2}

    #Vraca poteze moguce za igraca koji naredni igra
    def getAvailableMoves(self) -> list[Move]:
        moves = []
        if self.turn % 2 == 0:
            for i in range(1,self.rows):
                for j in range(0,self.cols):
                    if(self.boardState[i][j] == ' ' and self.boardState[i-1][j] == ' '):
                        moves.append(Move(i,j))
        else:
            for i in range(0,self.rows):
                for j in range(0,self.cols-1):
                    if(self.boardState[i][j]== ' ' and self.boardState[i][j+1] == ' '):
                        moves.append(Move(i,j))
                
        return moves
        
    def childStates(self):
        boards = []
        
        for move in self.getAvailableMoves():
            temp = self.playGhostMove(move)
            boards.append(temp)
        return boards

    #Vraca stanje table tj. ko je pobedio !
    def getState(self):
        state = self.countAvailableMoves()

        if(state["X"] == 0 and state["O"] != 0):
            return GameState.OWON
        elif(state["X"] != 0 and state["O"] == 0):
            return GameState.XWON
        else:
            return GameState.PLAYING

    def getBoard(self):
        return self.boardState

    def getDrawingBoard(self):
        return self.drawingBoard

    def playGhostMove(self,move):
        temp = deepcopy(self.boardState)

        row = move.row
        col = move.col

        if row == -1 or col == -1:
            return None

        if self.turn % 2 == 0 and row > 0:
            if temp[row][col] == ' ' and temp[row-1][col] == ' ':
                temp[row][col] = 'X'
                temp[row-1][col] = 'X'
                return temp
        elif self.turn % 2 == 1 and col < self.cols -1:
            if temp[row][col] == ' ' and temp[row][col+1] == ' ':
                temp[row][col] = 'O'
                temp[row][col+1] = 'O'
                return temp

        return None

    def undoLastMove(self):
        if len(self.lastMove) == 0:
            return False

        move = self.lastMove.pop()
        
        if self.turn % 2 == 1:
            (self.boardState)[move.row][move.col] = ' '
            (self.drawingBoard)[move.row][move.col] = ' '
            (self.boardState)[move.row-1][move.col] = ' '
            (self.drawingBoard)[move.row-1][move.col] = ' '
            self.turn -= 1
        else:
            (self.boardState)[move.row][move.col] = ' '
            (self.drawingBoard)[move.row][move.col] = ' '
            (self.boardState)[move.row][move.col+1] = ' '
            (self.drawingBoard)[move.row][move.col+1] = ' '
            self.turn -= 1

        return True

    def playMove(self,move:Move):
        row = move.row
        col = move.col

        if row == -1 or col == -1:
            return False

        if self.turn % 2 == 0 and row > 0:
            if self.boardState[row][col] == ' ' and self.boardState[row-1][col] == ' ':
                self.lastMove.append(Move(move.row,move.col))
                self.boardState[row][col] = 'X'
                self.drawingBoard[row][col] = 'XL'
                self.boardState[row-1][col] = 'X'
                self.drawingBoard[row-1][col] = 'XH'
                self.turn = self.turn + 1
                return True
        elif self.turn % 2 == 1 and col < self.cols -1:
            if self.boardState[row][col] == ' ' and self.boardState[row][col+1] == ' ':
                self.lastMove.append(Move(move.row,move.col))
                self.boardState[row][col] = 'O'
                self.boardState[row][col+1] = 'O'
                self.drawingBoard[row][col] = 'OL'
                self.drawingBoard[row][col+1] = 'OR'
                self.turn = self.turn + 1
                return True

        return False