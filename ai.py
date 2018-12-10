import random
from copy import deepcopy
from makeboard import *

whitePos = [['empty', 'white', 'white', 'white', 'white','empty'],
                   ['empty', 'white', 'white', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'white', 'white','empty'],
                   ['empty', 'white', 'empty', 'white', 'white','empty'], 
                   ['empty', 'white', 'white', 'empty', 'white','empty'],
                   ['empty', 'empty', 'white', 'white', 'empty','empty'],
                   ['empty', 'white', 'empty', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'empty', 'white','empty'],
                   ['empty', 'empty', 'empty', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'empty', 'empty','empty']]
whitePosPoint = [8640,720,720,720,720,120,120,120,20,20]

whiteDangerPiece = [['white', 'white', 'white', 'white', 'white'],
                   ['white', 'white', 'white', 'white', 'empty'],
                   ['empty', 'white', 'white', 'white', 'white'],
                   ['white', 'empty', 'white', 'white', 'white'],
                   ['white', 'white', 'empty', 'white', 'white'],
                   ['white', 'white', 'white', 'empty', 'white']]
whiteDangerPoint = [50000,720,720,720,720,720]

blackPos = [['empty', 'black', 'black', 'black', 'black','empty'],
                   ['empty', 'black', 'black', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'black', 'black','empty'],
                   ['empty', 'black', 'black', 'empty', 'black','empty'],
                   ['empty', 'black', 'empty', 'black', 'black','empty'],
                   ['empty', 'empty', 'black', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'empty', 'black','empty'],
                   ['empty', 'black', 'empty', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'empty', 'empty','empty'],
                   ['empty', 'empty', 'empty', 'black', 'empty','empty']]
blackPosPoint = [8640,720,720,720,720,120,120,120,20,20]

blackDangerPiece = [['black', 'black', 'black', 'black', 'black'],
                   ['black', 'black', 'black', 'black', 'empty'],
                   ['empty', 'black', 'black', 'black', 'black'],
                   ['black', 'black', 'empty', 'black', 'black'],
                   ['black', 'empty', 'black', 'black', 'black'],
                   ['black', 'black', 'black', 'empty', 'black']]
blackDangerPoint = [50000,720,720,720,720,720]

#determine whether or not the pieces vector that similar to one of the list above
def findSublist(small, big):
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return True
    return False

#convert the black and white pieces to a list
def pieceToString(vector):
    pieceList = []
    for piece in vector:
        if piece == Board.white:
            pieceList.append('white')
        elif piece == Board.black:
            pieceList.append('black')
        else:
            pieceList.append('empty')
    return pieceList

#analyze the vector and return the point according to each vector
def analyzeList(vector):
    pList = pieceToString(vector)
    point = {'white': 0, 'black': 0}
    length = len(pList)

    if length == 5:
        for i in range(len(whiteDangerPiece)):
            if whiteDangerPiece[i] == pList:
                point['white'] += whiteDangerPoint[i]
            if blackDangerPiece[i] == pList:
                point['black'] += blackDangerPoint[i]
        return point

    for i in range(length - 5):
        temp = [pList[i], pList[i + 1], pList[i + 2],
                pList[i + 3], pList[i + 4]]
        for i in range(len(whiteDangerPiece)):
            if whiteDangerPiece[i] == temp:
                point['white'] += whiteDangerPoint[i]
            if blackDangerPiece[i] == temp:
                point['black'] += blackDangerPoint[i]

    for i in range(length - 6):
        temp = [pList[i], pList[i + 1], pList[i + 2],
            pList[i + 3], pList[i + 4], pList[i + 5]]
        for i in range(len(whitePos)):
            if whitePos[i] == temp:
                point['white'] += whitePosPoint[i]
            if blackPos[i] == temp:
                point['black'] += blackPosPoint[i]
    return point

class AI(object):
 
    def __init__(self, gomoku, currentState, depth):

        self.ai = gomoku
        self.color = currentState
        self.depth = depth
        self.posI = -1
        self.posJ = -1

    def applyBoard(self, i, j, color):
        self.ai.applyBoard(i, j, color)

    #determine whether or not a piece has neighbor in 2 empty spot
    def checkSurrounding(self, color, i, j):
        #exhaustive search for four axes
        for axis in directions:
            for (xAxis, yAxis) in axis:

                if xAxis != 0 and (j + xAxis < 0 or j + xAxis >= N):
                    break
                if yAxis != 0 and (i + yAxis < 0 or i + yAxis >= N):
                    break
                if self.ai.getPos()[i + yAxis][j + xAxis] != Board.empty:
                    return True
                if xAxis != 0 and (j + xAxis * 2 < 0 or j + xAxis * 2 >= N):
                    break
                if yAxis != 0 and (i + yAxis * 2 < 0 or i + yAxis * 2 >= N):
                    break
                if self.ai.getPos()[i + yAxis * 2][j + xAxis * 2] != Board.empty:
                    return True
        return False

    #count the pieces that connect in a line
    def connectedCount(self, i, j, xAxis, yAxis, color):
        count = 0
        for s in range(1, 5): 
            if xAxis != 0 and (j + xAxis * s < 0 or j + xAxis * s >= N):
                break
            if yAxis != 0 and (i + yAxis * s < 0 or i + yAxis * s >= N):
                break
            if self.ai.getPos()[i + yAxis * s][j + xAxis * s] == color:
                count += 1
            else:
                break
        return count

    #collect 6 pieces in a row for analyze later
    def piecePos(self, i, j, xAxis, yAxis, color):
        position = []
        for s in range(-1, 5): 
            if xAxis != 0 and (j + xAxis * s < 0 or j + xAxis * s >= N):
                break
            if yAxis != 0 and (i + yAxis * s < 0 or i + yAxis * s >= N):
                break
            position.append(self.ai.getPos()[i + yAxis * s][j + xAxis * s])
        return position

    def checkmate(self, color, i, j):
        for axis in directions:
            axis_count = 1
            for (xAxis, yAxis) in axis:
                axis_count += self.connectedCount(i, j, xAxis, yAxis, color)
                if axis_count >= 5:
                    return True
        return False

    #check for 4 pieces in a row
    def straightFour(self, color, i, j):
        for axis in directions:
            currentPattern = []
            for (xAxis, yAxis) in axis:
                currentPattern += self.piecePos(i, j, xAxis, yAxis, color)
                if len(currentPattern) > 2:
                    currentPattern[1] = color
                if pieceToString(currentPattern) == whitePos[0]:
                    return True
                if pieceToString(currentPattern) == blackPos[0]:
                    return True
        return False

    def checkmateEnemy(self, color):
        vectors = []
        #exhaustive search
        for i in range(N):
            vectors.append(self.ai.getPos()[i])

        for j in range(N):
            vectors.append([self.ai.getPos()[i][j] for i in range(N)])

        vectors.append([self.ai.getPos()[x][x] for x in range(N)])
        
        for i in range(1, N - 4):
            vectors.append([self.ai.getPos()[x][x - i] for x in range(i, N)])
            vectors.append([self.ai.getPos()[y - i][y] for y in range(i, N)])
        
        for x in range(N):
            vectors.append(self.ai.getPos()[x][N - x - 1])
        
        for i in range(4, N - 1):
            vectors.append([self.ai.getPos()[x][i - x] for x in range(i, -1, -1)])
            vectors.append([self.ai.getPos()[x][N - x + N - i - 2] for x in range(N - i - 1, N)])
                  
        #checkmate
        for vector in vectors:
            temp = pieceToString(vector)
            if color == Board.black:
                for position in whiteDangerPiece:
                    if findSublist(position, temp):
                        return True
            if color == Board.white:
                for position in blackDangerPiece:
                    if findSublist(position, temp):
                        return True
        return False

    def startList(self):
        genList = []
        for i in range(N):
            for j in range(N):
                if self.ai.getPos()[i][j] \
                    != Board.empty:
                    continue  
                if not self.checkSurrounding(self.ai.getPos()[i][j], i, j):
                    continue
                if self.color == Board.white:
                    nextTurn = Board.black
                else:
                    nextTurn = Board.white

                nextMove = AI(deepcopy(self.ai), nextTurn, self.depth - 1)
                nextMove.applyBoard(i, j, self.color)
                genList.append((nextMove, i, j))

        #using heuristics search, and then sort it based on points 
        genScore = []
        for i in genList:
            genScore.append(self.analyzeScore(i[1], i[2]))

        genZipped = zip(genList, genScore)
        genSorted = sorted(genZipped, key=lambda t: t[1])
        (genList, genScore) = zip(*genSorted)
        return genList

    #convert a list of pieces in to points using analyzeList above 
    #return a list of points for MiniMax search
    def analyzeBoard(self):
        vectors = []
        #exhaustive search
        for i in range(N):
            vectors.append(self.ai.getPos()[i])

        for j in range(N):
            vectors.append([self.ai.getPos()[i][j] for i in range(N)])

        vectors.append([self.ai.getPos()[x][x] for x in range(N)])

        for i in range(1, N - 4):
            vectors.append([self.ai.getPos()[x][x - i] for x in range(i, N)])
            vectors.append([self.ai.getPos()[y - i][y] for y in range(i, N)])

        vectors.append([self.ai.getPos()[x][N - x - 1] for x in range(N)])

        for i in range(4, N - 1):
            vectors.append([self.ai.getPos()[x][i - x] for x in range(i, -1, -1)])
            vectors.append([self.ai.getPos()[x][N - x + N - i - 2] for x in range(N - i - 1, N)])

        board_score = 0
        for v in vectors:
            score = analyzeList(v)
            if self.color == Board.white:
                board_score += score['black'] - score['white']
            else:
                board_score += score['white'] - score['black']
        return board_score

    def analyzeScore(self, i, j):
        '''
        Return a point score for Degree Heuristics.
        '''
        vectors = []
        vectors.append(self.ai.getPos()[i])
        vectors.append([self.ai.getPos()[i][j] for i in range(N)])

        if j > i:
            vectors.append([self.ai.getPos()[x][x + j - i] for x in range(0, N - j + i)])
            
        elif j == i:
            vectors.append([self.ai.getPos()[x][x] for x in range(N)])
        elif j < i:
            vectors.append([self.ai.getPos()[x + i - j][x] for x in range(0, N - i + j)])
         
        if i + j == N - 1:
            vectors.append([self.ai.getPos()[x][N - 1 - x] for x in range(N)])

        elif i + j < N - 1:
            vectors.append([self.ai.getPos()[x][N - 1 - x - abs(i - j)] for x in range(N - abs(i - j))])
          
        elif i + j > N - 1:
            vectors.append([self.ai.getPos()[x][N - 1 - x + i + j - N + 1] for x in range(i + j - N + 1, N)])

        point_score = 0
        for v in vectors:
            score = analyzeList(v)
            if self.color == Board.white:
                point_score += score['white']
            else:
                point_score += score['black']
        return point_score

    def MiniMax(self, ai, alpha=-500000, beta=500000):
        if ai.depth <= 0:
            score = -ai.analyzeBoard()
            return score
    
        for (nextMove, i, j) in ai.startList():
            temp_score = -self.MiniMax(nextMove, -beta, -alpha)
            if temp_score > beta:
                return beta
            if temp_score > alpha:
                alpha = temp_score
                (ai.posI, ai.posJ) = (i, j)
        return alpha

    def randomMove(self):
        self.ai.applyBoard(random.randint(2,13), random.randint(2,13), self.color)
        return True

    def turn(self):
        for i in range(N):
            for j in range(N):
                if self.ai.getPos()[i][j] \
                    != Board.empty:
                    continue
                if self.checkmate(self.color, i, j):
                    print ('checkmate')
                    self.ai.applyBoard(i, j, self.color)
                    return True

                if not self.checkSurrounding(self.ai.getPos()[i][j], i, j):
                    continue

                if self.straightFour(self.color, i, j):
                    if self.checkmateEnemy(self.color) \
                        is True:
                        print ('be careful')
                    elif self.checkmateEnemy(self.color) \
                        is False:
                        print ('safe')
                        self.ai.applyBoard(i, j, self.color)
                        return True

        i = AI(self.ai, self.color, self.depth)
        score = self.MiniMax(i)
        (i, j) = (i.posI, i.posJ)

        if i is not None and j is not None:
            if self.ai.boardState(i, j) \
                != Board.empty:
                self.turn()
            else:
                self.ai.applyBoard(i, j,
                        self.color)
                return True
        return False



            