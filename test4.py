import numpy as np
import random
import threading
import time

# Spielfeldinitialisierung
def initField():
    return [[None for _ in range(7)] for _ in range(6)]

# Spielfeld in flaches Array umwandeln
def flattenField(field):
    return [1 if cell == "X" else -1 if cell == "O" else 0 for row in field for cell in row]

# Prüfen, ob eine Spalte voll ist
def isXFull(field, x):
    return all(field[i][x] is not None for i in range(len(field)))

# Symbol in Spalte setzen
def PlaceAtX(field, x, symbol):
    for i in range(len(field)):
        if field[i][x] is None:
            field[i][x] = symbol
            return True
    return False

# Gewinnprüfung
def isGameOver(field, symbol):
    # Horizontale Prüfung
    for row in field:
        count = 0
        for cell in row:
            count = count + 1 if cell == symbol else 0
            if count == 4:
                return True

    # Vertikale Prüfung
    for col in range(7):
        count = 0
        for row in range(6):
            count = count + 1 if field[row][col] == symbol else 0
            if count == 4:
                return True

    # Diagonale Prüfung
    for row in range(3):
        for col in range(4):
            if (field[row][col] == symbol and
                field[row+1][col+1] == symbol and
                field[row+2][col+2] == symbol and
                field[row+3][col+3] == symbol):
                return True
            if (field[row][col+3] == symbol and
                field[row+1][col+2] == symbol and
                field[row+2][col+1] == symbol and
                field[row+3][col] == symbol):
                return True
    return False

# Neural Network
class NeuralNetwork:
    def __init__(self, input_size=42, hidden_size=100, output_size=7):
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01
        self.bias_hidden = np.zeros((1, hidden_size))
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01
        self.bias_output = np.zeros((1, output_size))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, x):
        hidden = self.relu(np.dot(x, self.weights_input_hidden) + self.bias_hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        return output

# Neural Network Move
def neuralNetworkMove(nn, field):
    input_data = np.array([flattenField(field)])
    output = nn.forward(input_data)
    predicted_column = np.argmax(output)

    while isXFull(field, predicted_column):
        predicted_column = random.randint(0, 6)

    PlaceAtX(field, predicted_column, "X")

# Regel-basierter Computer Move
def computerMove(field):
    for col in range(7):
        if not isXFull(field, col):
            field_copy = [row[:] for row in field]
            PlaceAtX(field_copy, col, "O")
            if isGameOver(field_copy, "O"):
                PlaceAtX(field, col, "O")
                return
    while True:
        rrandom = random.randint(0, 6)
        if not isXFull(field, rrandom):
            PlaceAtX(field, rrandom, "O")
            return

# Spielfeld anzeigen
def printField(field):
    for zeile in reversed(field):
        print("|", end=" ")
        for wert in zeile:
            print(wert if wert else " ", end=" ")
        print("|")
    print("|", " ".join(str(i) for i in range(7)), "|")

# Lernmodus: NN vs. Computer
def learningMode(nn):
    global game_count, nn_win_count
    while True:
        field = initField()
        game_count += 1
        winner = None

        while True:
            neuralNetworkMove(nn, field)
            if isGameOver(field, "X"):
                nn_win_count += 1
                break

            computerMove(field)
            if isGameOver(field, "O"):
                break

            if all(isXFull(field, col) for col in range(7)):
                break
        
        # Ausgabe der Statistik im Lernmodus
        #print(f"\r[NN Win ratio: {nn_win_count}/{game_count}] -> {round((nn_win_count / game_count) * 100, 2)}%", end="", flush=True)

# Spielmodus: Mensch vs. NN
def playAgainstNN(nn):
    field = initField()
    while True:
        printField(field)
        # Menschlicher Spielerzug
        while True:
            try:        
                print(f"\r\nNN Win ratio: {nn_win_count}/{game_count} -> {round((nn_win_count / game_count) * 100, 2)}%\r\n", end="", flush=True)

                col = int(input("\r\nDein Zug (0-6): "))
                if 0 <= col <= 6 and not isXFull(field, col):
                    PlaceAtX(field, col, "O")
                    break
                else:
                    print("Ungültige Eingabe! Versuche es erneut.")
            except ValueError:
                print("Bitte eine Zahl zwischen 0 und 6 eingeben.")

        if isGameOver(field, "O"):
            printField(field)
            print("Du hast gewonnen!")
            break

        # Neural Network Zug
        neuralNetworkMove(nn, field)
        if isGameOver(field, "X"):
            printField(field)
            print("Das Neural Network hat gewonnen!")
            break

        if all(isXFull(field, col) for col in range(7)):
            printField(field)
            print("Unentschieden!")
            break

# Hauptprogramm
if __name__ == "__main__":
    nn = NeuralNetwork()
    game_count = 0
    nn_win_count = 0

    # Starte Lernmodus in separatem Thread
    learning_thread = threading.Thread(target=learningMode, args=(nn,), daemon=True)
    learning_thread.start()

    # Spielmodus: Mensch vs. NN
    playAgainstNN(nn)
