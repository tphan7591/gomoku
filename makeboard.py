import pygame
from pygame.locals import *
from enum import Enum

N = 15
directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
boardLoc = 'graph/'
boardWidth = 540
boardHeight = 540
edge = 22
frame = (boardWidth - 2 * edge) / (N - 1)
totalPiece = 32

class Board(Enum):
    empty = 0
    black = 1
    white = 2

class MakeBoard(object):
    #initialize 15x15 chessboard
    def __init__(self):
        self.chessBoard = [[Board.empty for j in range(N)] for i in range(N)]
        self.locI = -1
        self.locJ = -1
        self.currentBoard = Board.empty

    def getPos(self):
        return self.chessBoard

    def boardState(self, i, j):
        return self.chessBoard[i][j]

    def applyBoard(self, i, j, state):
        self.chessBoard[i][j] = state
        self.locI = i
        self.locJ = j
        self.currentBoard = state

    def findResult(self):
        if self.straightFive(self.locI, self.locJ, self.currentBoard):
            return self.currentBoard
        else:
            return Board.empty

    def countPos(self, i, j, xAxis, yAxis, player):
        count = 0
        for move in range(1, 5):
            if xAxis != 0 and (j + xAxis * move < 0 or j + xAxis * move >= N):
                break
            if yAxis != 0 and (i + yAxis * move < 0 or i + yAxis * move >= N):
                break
            if self.chessBoard[i + yAxis * move][j + xAxis * move] == player:
                count += 1
            else:
                break
        return count

    #obtain the pieces in four direction
    def straightFive(self, i, j, player):
        for axis in directions:
            posCount = 1
            for (xAxis, yAxis) in axis:
                posCount += self.countPos(i, j, xAxis, yAxis, player)
                if posCount >= 5:
                    return True
        return False

class GetBoardInfo(object):
    
    def __init__(self, gomoku):
        self.board = gomoku
        self.currentState = Board.black
        pygame.init()
        self.boardImage = pygame.display.set_mode((boardWidth, boardHeight), 0, 32)
        pygame.display.set_caption('MakeBoard AI')
        self.chessBoard = pygame.image.load(boardLoc + 'board.jpg').convert()
        self.blackPiece = pygame.image.load(boardLoc + 'black.png').convert_alpha()
        self.whitePiece = pygame.image.load(boardLoc + 'white.png').convert_alpha()

    #take position on the board and convert it to x and y coordinate
    def convertToCoord(self, i, j):
        return (edge + j * frame - totalPiece / 2, edge + i * frame - totalPiece / 2)

    #convert coordinate on board to actual number
    def convertToMap(self, x, y):
        (i, j) = (int(round((y - edge + totalPiece / 2) / frame)),
                  int(round((x - edge + totalPiece / 2) / frame)))
        if i < 0 or i >= N or j < 0 or j >= N:
            return (None, None)
        else:
            return (i, j)

    def applyResult(self):

        # board

        self.boardImage.blit(self.chessBoard, (0, 0))

        # chess totalPiece

        for i in range(0, N):
            for j in range(0, N):
                (x, y) = self.convertToCoord(i, j)
                state = self.board.boardState(i, j)
                if state == Board.black:
                    self.boardImage.blit(self.blackPiece, (x, y))
                elif state == Board.white:
                    self.boardImage.blit(self.whitePiece, (x, y))
                else:
                    Board.empty
                    pass

    def mouseClick(self):
        (x, y) = pygame.mouse.get_pos()
        if self.currentState == Board.black:
            self.boardImage.blit(self.blackPiece, (x - totalPiece / 2, y
                               - totalPiece / 2))
        else:
            self.boardImage.blit(self.whitePiece, (x - totalPiece / 2, y
                               - totalPiece / 2))

    def printResult(self, result):
        font = pygame.font.SysFont('Arial', 30)
        msg = 'Game Over:'
        if result == Board.black:
            msg = msg + 'Black Wins'
        elif result == Board.white:
            msg = msg + 'White Wins'
        else:
            msg = msg + 'Draw'
        text = font.render(msg, True, (0, 0, 255))
        self.boardImage.blit(text, (boardWidth / 2 - 200, boardHeight / 2 - 50))

    def turn(self):
        (i, j) = (None, None)
        click = pygame.mouse.get_pressed()
        if click[0]:
            (x, y) = pygame.mouse.get_pos()
            (i, j) = self.convertToMap(x, y)
        if not i is None and not j is None:
            if self.board.boardState(i, j) \
                != Board.empty:
                return False
            else:
                self.board.applyBoard(i, j,
                        self.currentState)
                return True
        return False

    def swap(self):
        if self.currentState == Board.black:
            self.currentState = Board.white
        else:
            self.currentState = Board.black


            