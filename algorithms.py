import math
from board import Move,Board

def minMax(board:Board,alpha,beta,depth):

    if depth == 0:
        eval = evaluation(board.boardState)
        return (-1,-1,eval)

    moves = board.getAvailableMoves()

    move = Move(-1,-1)
    val = 0

    if (board.turn % 2) == 0:

        val = -math.inf

        if board.turn < 7:
            moves = list(filter(lambda x: x.col in (1,6),moves))

        moves.sort(key =lambda x: (x.col not in (1,6)))

        for temp in moves:

            board.playMove(temp)
            (_,_,n_eval) = minMax(board,alpha,beta,depth-1)
            board.undoLastMove()

            if(val == -math.inf):
                move = temp
                val = n_eval

            if(n_eval > val):
                move = temp
                val = n_eval

            alpha = max(alpha,val)

            if(alpha >= beta):
                return (move.row,move.col,val)
    else:

        val = math.inf

        if board.turn < 8:
            moves = list(filter(lambda x: x.row in (1,6),moves))

        moves.sort(key =lambda x: (x.row not in (1,6)))

        for temp in moves:
            board.playMove(temp)
            (_,_,n_eval) = minMax(board,alpha,beta,depth-1)
            board.undoLastMove()

            if(val == math.inf):
                move = temp
                val = n_eval

            if(n_eval < val):
                move = temp
                val = n_eval

            beta = min(beta,val)

            if(alpha >= beta):
                return (move.row,move.col,val)
        
    return (move.row,move.col,val)

def evaluation(boardState):
    brojac1 = 0
    brojac2 = 0
    safe1 = 0
    safe2 = 0

    for i in range(1,8):
        for j in range(0,8):
            if boardState[i][j] == ' ' and boardState[i-1][j] == ' ':
                brojac1+=1
                if j == 0 or (boardState[i][j - 1] != ' ' and boardState[i - 1][j - 1] != ' '):
                    if  (j == 7 or (boardState[i][j + 1] != ' ' and boardState[i - 1][j + 1] != ' ')):
                        safe1 += 1

    for i in range(0,8):
        for j in range(0,7):
            if(boardState[i][j]== ' ' and boardState[i][j+1] == ' '):
                brojac2+=1
                if i == 0 or (boardState[i-1][j] != ' ' and boardState[i - 1][j + 1] != ' '):
                    if  (i == 7 or (boardState[i+1][j] != ' ' and boardState[i + 1][j + 1] != ' ')):
                        safe2 += 1
    
    eval = brojac1 - brojac2 + safe1 - safe2
    if brojac2 == 0:
        return 1000
    elif brojac1 == 0:
        return -1000
    elif safe1 > brojac2:
        return  100+eval
    elif safe2 > brojac1:
        return -100-eval
    else:
        return eval