import backend
import handle_user
import handle_computer
import numpy as np
import sys


class Configuration:
    def __init__(self):
        self.measurables = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.probArray = [100, 75, 50, 25, 0]

        self.m = [
            [[100, 100, 0], [100, 100, 0], [0, 0, -1]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
        ]

        self.A = np.array([
            [[70, 67, 77], [66, 78, 6], [6, 67, 11]],
            [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
            [[-1, 70, 71], [-1, 80, 82], [84, 76, -1]]
        ])

        self.NeighborsOfEachPos = {
            0: [1, 2, 3, 6, 4, 8],
            1: [0, 2, 4, 7],
            2: [0, 1, 5, 8, 4, 6],
            3: [0, 6, 4, 5],
            4: [3, 5, 1, 7, 0, 8, 2, 6],
            5: [3, 4, 2, 8],
            6: [0, 3, 7, 8, 4, 2],
            7: [1, 4, 6, 8],
            8: [0, 4, 6, 7, 2, 5],
        }

        self.SuperMeasureIndexes = []
        self.SuperMeasureValue = 0



def playGame():
    myBoard = np.array([
        [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
        [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
        [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    ])
    NumMeasurePlayer = 0
    NumMeasureComputer = 0
    GameOver = False

    myValues = Configuration()

    try:
        while not GameOver:
            print("Your turn")
            myBoard, MeasureAlong = handle_user.userMove(myBoard, myValues.measurables, myValues.probArray)

            if MeasureAlong != 0:
                NumMeasurePlayer = NumMeasurePlayer + 1
                Super = len(MeasureAlong) > 3
                GameOver = backend.makeCirc(
                    myBoard,
                    MeasureAlong,
                    Super,
                    myValues.measurables,
                    myValues.SuperMeasureIndexes,
                    myValues.SuperMeasureValue
                )
                if Super:
                    if GameOver:
                        print(
                            f"\nSuper Measure successful. You measured: {myValues.SuperMeasureValue} "
                            f"at indices: {myValues.SuperMeasureIndexes}"
                        )
                    else:
                        print("\nSuper measured failed. You Lose!")
                    sys.exit(0)
                else:
                    if GameOver:
                        print("\nYou measured correctly! You win!")
                        sys.exit(0)
                    elif NumMeasurePlayer >= 5:
                        print("\nYou have exhausted all your measurement moves! You lose!")
                        sys.exit(0)
                    else:
                        print(
                            f"\nOops. Measurement failed. No worries, keep playing. "
                              f"You have {5 - NumMeasurePlayer} Measurement moves left!"
                        )
                        makeMeasurements(MeasureAlong, myBoard)

            # clear_output(wait=True)

            print("Computer's turn\n...\n")

            myBoard, MeasureAlong = handle_computer.DecideMoveOrMeasure(
                myBoard,
                myValues.measurables,
                myValues.NeighborsOfEachPos
            )

            if MeasureAlong != 0:
                NumMeasureComputer = NumMeasureComputer + 1
                GameOver = backend.makeCirc(
                    myBoard,
                    MeasureAlong,
                    False,
                    myValues.measurables,
                    myValues.SuperMeasureIndexes,
                    myValues.SuperMeasureValue
                )

                if GameOver:
                    print(f"\nThe Computer choose to measure along {MeasureAlong} and won. You lose!")
                    sys.exit(0)
                elif NumMeasureComputer >= 5:
                    print("The Computer exhausted all its Measurement moves. You Win!")
                    sys.exit(0)
                else:
                    print(f"\nThe Computer choose to measure along {MeasureAlong} but failed! You're lucky")
                    makeMeasurements(MeasureAlong, myBoard)
            else:
                print("Computer placed a Qubit\n...\n")

    except SystemExit:
        print("\n...\n\nGAME OVER\n\n...\n\nRerun gameplay to play again!")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n\nExiting game...\n\n")



def makeMeasurements(MeasureAlong, myBoard):
    myBoard[0][MeasureAlong[0] // 3][MeasureAlong[0] % 3] = -1
    myBoard[0][MeasureAlong[1] // 3][MeasureAlong[1] % 3] = -1
    myBoard[0][MeasureAlong[2] // 3][MeasureAlong[2] % 3] = -1
    myBoard[2][MeasureAlong[0] // 3][MeasureAlong[0] % 3] = -1
    myBoard[2][MeasureAlong[1] // 3][MeasureAlong[1] % 3] = -1
    myBoard[2][MeasureAlong[2] // 3][MeasureAlong[2] % 3] = -1
    removeEntangles(myBoard, MeasureAlong)


def removeEntangles(myBoard, MeasureAlong):
    for m in MeasureAlong:
        for i in range(0, 3):
            for j in range(0, 3):
                if myBoard[2][i][j] == (70 + m) or myBoard[2][i][j] == (80 + m):
                    myBoard[0][i][j] = -1
                    myBoard[2][i][j] = -1



if __name__ == "__main__":
    playGame()