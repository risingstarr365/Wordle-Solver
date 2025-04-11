import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import argparse
import os
import random

class WordleSolver:
    def __init__(self, wordlist_path="wordle_words.txt", use_ibm_quantum=False):
        self.wordlist = self._load_wordlist(wordlist_path)
        self.use_ibm_quantum = use_ibm_quantum
        self.backend = self._setup_backend()
        self.attempt_history = []

    def _load_wordlist(self, path):
        with open(path, 'r') as f:
            return [word.strip().lower() for word in f.readlines()]

    def _setup_backend(self):
        if self.use_ibm_quantum:
            try:
                from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
                service = QiskitRuntimeService()
                return service.backend("ibmq_qasm_simulator")
            except Exception as e:
                print(f"Error setting up IBM Quantum: {e}")
                print("Falling back to local simulator")
                self.use_ibm_quantum = False
        
        return Aer.get_backend('qasm_simulator')

    def _create_grover_circuit(self, target_word):
        # Number of qubits needed: 5 letters * 5 bits per letter
        n_qubits = 25
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Initialize superposition
        for i in range(n_qubits):
            qc.h(i)
        
        # Oracle for target word
        for i, letter in enumerate(target_word):
            letter_bits = format(ord(letter) - ord('a'), '05b')
            for j, bit in enumerate(letter_bits):
                if bit == '0':
                    qc.x(i*5 + j)
        
        # Grover diffusion operator
        for i in range(n_qubits):
            qc.h(i)
            qc.x(i)
        qc.h(n_qubits-1)
        qc.mcx(list(range(n_qubits-1)), n_qubits-1)
        qc.h(n_qubits-1)
        for i in range(n_qubits):
            qc.x(i)
            qc.h(i)
        
        # Measurement
        qc.measure(range(n_qubits), range(n_qubits))
        return qc

    def _get_feedback(self, guess, target):
        feedback = []
        target_list = list(target)
        guess_list = list(guess)
        
        # First pass: mark greens
        for i in range(5):
            if guess_list[i] == target_list[i]:
                feedback.append('green')
                target_list[i] = None
                guess_list[i] = None
            else:
                feedback.append('gray')
        
        # Second pass: mark yellows
        for i in range(5):
            if guess_list[i] is not None:
                if guess_list[i] in target_list:
                    feedback[i] = 'yellow'
                    target_list[target_list.index(guess_list[i])] = None
        
        return feedback

    def solve(self, target_word):
        if len(target_word) != 5:
            raise ValueError("Target word must be 5 letters long")
        
        target_word = target_word.lower()
        if target_word not in self.wordlist:
            print(f"Word '{target_word}' not in word list. Trying a different word...")
            # Pick a random word from the list
            target_word = random.choice(self.wordlist)
            print(f"New target word: {target_word}")
        
        remaining_words = self.wordlist.copy()
        
        while len(remaining_words) > 0:
            # Pick a word from the remaining valid words
            guess = remaining_words[0]
            
            # Get feedback
            feedback = self._get_feedback(guess, target_word)
            self.attempt_history.append((guess, feedback))
            
            # Check if we found the word
            if all(f == 'green' for f in feedback):
                return guess, self.attempt_history
            
            # Filter remaining words based on feedback
            remaining_words = self._filter_words(remaining_words, guess, feedback)
            
            if len(remaining_words) == 0:
                return None, self.attempt_history
        
        return None, self.attempt_history

    def _bits_to_word(self, bits):
        word = ''
        for i in range(0, len(bits), 5):
            letter_bits = bits[i:i+5]
            letter = chr(int(letter_bits, 2) + ord('a'))
            word += letter
        return word

    def _filter_words(self, words, guess, feedback):
        filtered = []
        for word in words:
            valid = True
            word_list = list(word)
            guess_list = list(guess)
            
            # Check greens
            for i in range(5):
                if feedback[i] == 'green' and word_list[i] != guess_list[i]:
                    valid = False
                    break
                elif feedback[i] == 'green':
                    word_list[i] = None
                    guess_list[i] = None
            
            if not valid:
                continue
            
            # Check yellows
            for i in range(5):
                if feedback[i] == 'yellow':
                    if guess_list[i] not in word_list or word_list[i] == guess_list[i]:
                        valid = False
                        break
                    word_list[word_list.index(guess_list[i])] = None
                    guess_list[i] = None
            
            if not valid:
                continue
            
            # Check grays
            for i in range(5):
                if feedback[i] == 'gray' and guess_list[i] is not None:
                    if guess_list[i] in word_list:
                        valid = False
                        break
            
            if valid:
                filtered.append(word)
        
        return filtered

    def visualize_circuit(self, target_word):
        qc = self._create_grover_circuit(target_word)
        return qc.draw(output='mpl')

def main():
    parser = argparse.ArgumentParser(description='Quantum Wordle Solver')
    parser.add_argument('--wordlist', type=str, default='wordle_words.txt',
                      help='Path to word list file')
    parser.add_argument('--backend', type=str, default='local',
                      choices=['local', 'ibmq'],
                      help='Quantum backend to use')
    args = parser.parse_args()

    use_ibm_quantum = args.backend == 'ibmq'
    solver = WordleSolver(wordlist_path=args.wordlist, use_ibm_quantum=use_ibm_quantum)

    # Example usage
    target = "hello"
    result, history = solver.solve(target)

    if result:
        print(f"Found the word: {result}")
    else:
        print("Could not find the word within the maximum attempts")

    print("\nAttempt history:")
    for guess, feedback in history:
        print(f"\nGuess: {guess}")
        print(f"Feedback: {feedback}")

    # Visualize the circuit
    fig = solver.visualize_circuit(target)
    plt.show()

if __name__ == "__main__":
    main() 
