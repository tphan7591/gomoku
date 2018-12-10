import pygame
from pygame.locals import *
from sys import exit
from makeboard import *
from ai import *

#run in terminal
if __name__ == '__main__': 
    gomoku = MakeBoard()
    boardInfo = GetBoardInfo(gomoku)
    
    #initiate both AI
    ai = AI(gomoku, Board.black, 2)
    ai2 = AI(gomoku, Board.white, 2)
    result = Board.empty

    #set ai2 as true if play ai vs ai
    ai_On = True
    ai2_On = False

    ai.randomMove()
    result = gomoku.findResult()
    boardInfo.swap()

    while True:
        #vs AI
        if ai2_On:
            ai2.turn()
            result = gomoku.findResult()
            if result != Board.empty:
                print (result, "wins")
                break
            if ai_On:
                ai.turn()
                result = gomoku.findResult()
                if result != Board.empty:
                    print (result, "wins")
                    break
            else:
                boardInfo.swap()

        #vs player
        for control in pygame.event.get():
            if control.type == QUIT:
                exit()
            elif control.type == MOUSEBUTTONDOWN:
                if boardInfo.turn():
                    result = gomoku.findResult()
                else:
                    continue
                if result != Board.empty:
                    break
                if ai_On:
                    ai.turn()
                    result = gomoku.findResult()
                else:
                    boardInfo.swap()        
    
        boardInfo.applyResult()
        boardInfo.mouseClick()

        if result != Board.empty:
            boardInfo.printResult(result)

        pygame.display.update()