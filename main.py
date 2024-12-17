import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=6, hidden_size=10, output_size=6):
        self.hidden_size = hidden_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size) * 0.01 #0.01
        self.bias_hidden = np.zeros((1, hidden_size))
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) * 0.01#0.01
        self.bias_output = np.zeros((1, output_size))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, x):
        self.hidden = self.relu(np.dot(x, self.weights_input_hidden) + self.bias_hidden)
        output = np.dot(self.hidden, self.weights_hidden_output) + self.bias_output
        return output

    def train(self, inputs, targets, epochs, lr):
        prev_word = None
        for epoch in range(epochs):
            # Forward
            outputs = self.forward(inputs)
            loss = np.mean((outputs - targets) ** 2)

            # Abbruchbedingung prüfen
            predicted_chars = [
                chr(max(32, min(127, int(round(val))))) if 32 <= int(round(val)) <= 127 else ""
                for val in outputs[0]
            ]
            predicted_word = "".join(predicted_chars)
            if predicted_word == word:
                print(f"\033[32mEpoch {epoch}, Loss: {loss:.4f}, Vorhergesagtes Wort: {predicted_word}\033[0m")
                print("\r\nWort Gefunden")
                break
            
            # Backward
            output_error = 2 * (outputs - targets) / targets.size
            hidden_error = np.dot(output_error, self.weights_hidden_output.T) * (self.hidden > 0)
            
            # Gradienten berechnen
            d_weights_hidden_output = np.dot(self.hidden.T, output_error)
            d_bias_output = np.sum(output_error, axis=0, keepdims=True)
            d_weights_input_hidden = np.dot(inputs.T, hidden_error)
            d_bias_hidden = np.sum(hidden_error, axis=0, keepdims=True)
            
            # Gewichte und Biases aktualisieren
            self.weights_hidden_output -= lr * d_weights_hidden_output
            self.bias_output -= lr * d_bias_output
            self.weights_input_hidden -= lr * d_weights_input_hidden
            self.bias_hidden -= lr * d_bias_hidden

            # Early Stopping prüfen
            if epoch % 100 == 0 and prev_word == predicted_word:
                #print("lr * 1.5")
                #lr *= 1.5 
                lr *= 1.5

            #v:{np.prod(outputs[0])}
            
            # Fortschritt ausgeben
            if epoch % 1000 == 0:
                # Vorhersage in Buchstaben umwandeln
                if prev_word == predicted_word:
                    print(f"\033[31mEpoch {epoch}, Loss: {loss:.4f}, Vorhergesagtes Wort: {predicted_word}\033[0m")
                else:
                    print(f"Epoch {epoch}, Loss: {loss:.4f}, Vorhergesagtes Wort: {predicted_word}")


            prev_word = predicted_word
            


# Zielausgabe: ASCII-Werte des Wortes
word = "Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz"

# ASCII-Werte:
ascii_target = np.array([[ord(c) for c in word]])
input_size = len(ascii_target[0])

# Zufällige Eingabe als Startwert
inputs = np.random.rand(1, input_size)
#inputs = np.random.randint(0, 2, (1, input_size))  # 0 oder 1 als Eingabewerte

# Netzwerk initialisieren und trainieren
nn = NeuralNetwork(input_size=input_size, hidden_size=100, output_size=input_size)
nn.train(inputs, ascii_target, epochs=500000, lr=0.01)

# Vorhersage und Dekodierung
predicted_output = nn.forward(inputs)
predicted_chars = [chr(int(round(val))) for val in predicted_output[0]]


