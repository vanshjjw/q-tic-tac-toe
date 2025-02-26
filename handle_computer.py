import backend
import math
from copy import deepcopy



def DecideMoveOrMeasure(myBoard, measurables, neighborsOfEachPos):
    valueOne = []
    valueTwo = []
    x = 0
    for m in measurables:
        v1 = 1
        v2 = 1
        for index in m:
            if myBoard[0][index // 3][index % 3] == -1:
                v1 = v1 * 0
                v2 = v2 * 0
            else:
                if myBoard[2][index // 3][index % 3] >= 80:
                    pos = myBoard[2][index // 3][index % 3] - 80
                    if PositionIsInM(pos, m):
                        v1 = 0
                        v2 = 0
                    else:
                        v1 = v1 * (1 - myBoard[0][pos // 3][pos % 3] / 100)
                        v2 = v2 * (myBoard[0][pos // 3][pos % 3] / 100)

                elif myBoard[2][index // 3][index % 3] >= 70:
                    pos = myBoard[2][index // 3][index % 3] - 70
                    if not PositionIsInM(pos, m):
                        v1 = v1 * myBoard[0][pos // 3][pos % 3] / 100
                        v2 = v2 * (1 - myBoard[0][pos // 3][pos % 3] / 100)

                else:
                    v1 = v1 * myBoard[0][index // 3][index % 3] / 100
                    v2 = v2 * (1 - myBoard[0][index // 3][index % 3] / 100)

        valueOne.append(v1)
        valueTwo.append(v2)
        x = x + 1

    max0 = max(valueOne)
    max1 = max(valueTwo)

    if not checkEmptySpace(myBoard):
        if max0 > max1:
            return myBoard, measurables[valueOne.index(max0)]
        else:
            return myBoard, measurables[valueTwo.index(max1)]

    if max0 > 0.5 or max1 > 0.5:
        if max0 > max1:
            index = valueOne.index(max0)
            return myBoard, measurables[index]
        else:
            index = valueTwo.index(max1)
            return myBoard, measurables[index]
    else:
        return DecideMoveSquare(myBoard, measurables, neighborsOfEachPos)



def DecideMoveSquare(myBoard, measurables, neighborsOfEachPos):
    myBoardCopied = deepcopy(myBoard)
    pos = []
    zeroRatio = []
    score = []
    for p in range(0, 9):
        if myBoardCopied[0][p // 3][p % 3] == -1:
            pos.append(p)
            z = math.floor(computerMove(myBoard, p, neighborsOfEachPos) * 100)
            zeroRatio.append(z)
            myBoardCopied[0][p // 3][p % 3] = z
            score.append(FindScore(myBoardCopied, measurables))
            myBoardCopied[0][p // 3][p % 3] = myBoard[0][p // 3][p % 3]
    maximum = max(score)
    index = score.index(maximum)
    p = pos[index]
    myBoard[0][p // 3][p % 3] = 10 * round(zeroRatio[index] / 10)
    return myBoard, 0


def FindScore(myBoard, measurables):
    score = 0
    for m in measurables:
        i, j, k = m[0], m[1], m[2]
        a, b, c = myBoard[0][i // 3][i % 3] / 100, myBoard[0][j // 3][j % 3] / 100, myBoard[0][k // 3][k % 3] / 100
        if not (a < 0 or b < 0 or c < 0):
            score = score + a * b * c + (1 - a) * (1 - b) * (1 - c)
    return 8 - score


def PositionIsInM(pos, M):
    for m in M:
        if pos == m:
            return True
    return False


def checkEmptySpace(myBoard):
    for i in range(0, 9):
        if myBoard[0][i // 3][i % 3] == -1:
            return True
    return False


def computerMove(myBoard, pos, NeighborsOfEachPos):
    neighbours = NeighborsOfEachPos[pos]
    zeroes = 0
    ones = 0
    for i in range(0, len(neighbours), 2):
        c0, c1 = backend.QuantumMoveMaker(myBoard, neighbours[i], neighbours[i + 1])
        zeroes = zeroes + c0
        ones = ones + c1
    return zeroes / (zeroes + ones)

