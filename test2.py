import random

field = [[None for _ in range(7)] for _ in range(6)] # cols, rows (spalten, zeilen), (x, y), (width, height)

#field[0][0] = "n"
#field[0][3] = "x"
#field[1][0] = "y"

def printField():
    for zeile in reversed(field):
        print("|", end=" ")
        for wert in zeile:
            if wert is None:
                print(" ", end=" ")
            else:
                print(wert, end=" ")
        print("|")

    print("|", end=" ")
    for i in range(len(field[0])):
        if True:
            print(i, end=" ")
        else:
            print("  ", end=" ")
    print("|")

def isXFull(x):
    for i in range(len(field)):
        if field[i][x] == None:
            return False
    return True

def PlaceAtX(field, x, symbol):
    for i in range(len(field)):
        if field[i][x] == None:
            field_copy = [row[:] for row in field]
            field_copy[i][x] = symbol
            return field_copy
    
def isGameOver(field, checkSymbol):
    rows = len(field)
    cols = len(field[0])
    
    # Horizontale Prüfung
    for row in field:
        count = 0
        for symbol in row:
            if symbol == checkSymbol:
                count += 1
                if count == 4:
                    return True  # Vier Symbole horizontal
            else:
                count = 0

    # Vertikale Prüfung
    for col in range(cols):
        count = 0
        for row in range(rows):
            if field[row][col] == checkSymbol:
                count += 1
                if count == 4:
                    return True  # Vier Symbole vertikal
            else:
                count = 0

    # Diagonale Prüfung (von oben links nach unten rechts)
    for row in range(rows - 3):  # Sicherstellen, dass genug Platz nach unten ist
        for col in range(cols - 3):  # Sicherstellen, dass genug Platz nach rechts ist
            if (field[row][col] == checkSymbol and
                field[row + 1][col + 1] == checkSymbol and
                field[row + 2][col + 2] == checkSymbol and
                field[row + 3][col + 3] == checkSymbol):
                return True  # Vier Symbole diagonal (positive Steigung)

    # Diagonale Prüfung (von oben rechts nach unten links)
    for row in range(rows - 3):  # Sicherstellen, dass genug Platz nach unten ist
        for col in range(3, cols):  # Sicherstellen, dass genug Platz nach links ist
            if (field[row][col] == checkSymbol and
                field[row + 1][col - 1] == checkSymbol and
                field[row + 2][col - 2] == checkSymbol and
                field[row + 3][col - 3] == checkSymbol):
                return True  # Vier Symbole diagonal (negative Steigung)

    return False

def computerMove():
    global field
    for i in range(len(field[0])):
        if not isXFull(i):
            field_copy = [row[:] for row in field]
            temp_field = PlaceAtX(field_copy, i, "X")
            if isGameOver(temp_field, "X"):
                field = PlaceAtX(field, i, "X")
                return

    # Blockieren des Spielers prüfen
    for i in range(len(field[0])):
        if not isXFull(i):
            field_copy = [row[:] for row in field]
            temp_field = PlaceAtX(field_copy, i, "0")
            if isGameOver(temp_field, "0"): 
                field = PlaceAtX(field, i, "X")
                return
    
    while True:
        rrandom = random.randrange(0, 7)
        if not isXFull(rrandom):
            field = PlaceAtX(field, rrandom, "X")
            break


    
def isFieldFull():
    for row in field: 
        for cell in row: 
            if cell is None: 
                return False
    return True





while True:
    printField()
    x_coord = int(input("Enter x-coord: "))

    if x_coord < 0 or x_coord > 6:
        print("number must be between 0 and 6")
    elif isXFull(x_coord):
        print("not possible")
    else:
        field = PlaceAtX(field, x_coord, "0")

    if isGameOver(field, "0"):
        print("0 won!")
        printField()
        break

    if isFieldFull():
        print("feld ist voll, unendschieden!")
        break

    computerMove()

    if isGameOver(field, "X"):
        print("X won!")
        printField()
        break

    if isFieldFull():
        print("feld ist voll, unendschieden!")
        break
