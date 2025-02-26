import backend
import numpy as np
import handle_display


def FindAllOccupiedIndices(myBoard):
    indices = []
    for i in range(0, 3):
        for j in range(0, 3):
            if myBoard[i][j] != -1:
                indices.append(myBoard[i][j])
    return indices


def provideQubitChoices(myBoard, cell, probArray):
    print(
        "\nQubit Choices:\n0. 100/0\n1. 75/25\n2. 50/50\n3. 25/75\n4. 0/100\n5. Entangle positive\n6. Entangle negative"
    )
    choice = int(input())
    if choice <= 4:
        myBoard[0][cell // 3][cell % 3] = probArray[choice]
        return myBoard, 0
    elif choice <= 6:
        while True:
            print("\nEnter position of control Qubit (0-8)")
            pos = int(input())
            if myBoard[0][pos // 3][pos % 3] == -1:
                print("\nPlease choose an occupied block?")
            else:
                myBoard[2][cell // 3][cell % 3] = (choice + 2) * 10 + pos
                if choice == 5:
                    myBoard[0][cell // 3][cell % 3] = myBoard[0][pos // 3][pos % 3]
                else:
                    myBoard[0][cell // 3][cell % 3] = 100 - myBoard[0][pos // 3][pos % 3]
                break
        return myBoard, 0
    else:
        print("Invalid Choice, Please try again with a value between 0 and 6")
        return provideQubitChoices(myBoard, cell, probArray)



def userMove(myBoard, measurables, probArray):
    print("\nCurrent board:\n")
    handle_display.display_board(myBoard)
    Repeat = True

    while Repeat:
        print("\nChoose Move:\nEnter 0 to place Qubit\nEnter 1 to Measure")
        move = int(input())

        if move == 0:
            print("\nWhere do you want to place a Qubit? Choose from 0-8:")
            cell = int(input())
            if cell > 8 or cell < 0:
                print("Choice out of bounds, Please choose a value between 0-8")
            elif myBoard[0][cell // 3][cell % 3] == -1:
                return provideQubitChoices(myBoard, cell, probArray)
            else:
                print("\nYou chose a Non-Empty Cell, Please try again:")

        elif move == 1:
            print("\nChoose Measure row (0-2), column(3-5), diagonal(6-7) or Super Measurement(8):")
            index = int(input())
            if index == 8:
                return myBoard, FindAllOccupiedIndices(myBoard[0][:][:])
            else:
                x = measurables[index]
                if myBoard[0][x[0] // 3][x[0] % 3] != -1 and myBoard[0][x[1] // 3][x[1] % 3] != -1 and myBoard[0][x[2] // 3][
                    x[2] % 3] != -1:
                    return myBoard, measurables[index]
                else:
                    print("Choose occupied cells, please try again?")
        else:
            print("Wrong choice: re-enter")
            Repeat = True
