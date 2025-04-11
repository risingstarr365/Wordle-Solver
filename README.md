# Wordle Solver

A Python-based Wordle solver that helps you find the target word using a systematic approach.

## Features

- Uses official Wordle word list
- Smart word selection strategy
- Clear feedback system
- Automatic word validation
- Easy to use command-line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/wordle-solver.git
cd wordle-solver
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Use

1. Basic usage:
```bash
python wordle_solver.py
```

2. Using a specific word list:
```bash
python wordle_solver.py --wordlist path/to/wordlist.txt
```

3. Using IBM Quantum backend (optional):
```bash
export IBM_QUANTUM_TOKEN="your_api_token_here"
python wordle_solver.py --backend ibmq
```

## Understanding the Feedback

The solver provides feedback for each guess using three colors:
- 🟩 Green: Letter is correct and in the right position
- 🟨 Yellow: Letter is in the word but in the wrong position
- ⬜ Gray: Letter is not in the word

## Example Output

```
Found the word: hello

Attempt history:
Guess: alert
Feedback: ['gray', 'yellow', 'yellow', 'gray', 'gray']

Guess: louse
Feedback: ['yellow', 'yellow', 'gray', 'gray', 'yellow']

Guess: hello
Feedback: ['green', 'green', 'green', 'green', 'green']
```

## Word List

The solver uses `wordle_words.txt` which contains:
- Common 5-letter words
- Official Wordle word list
- All words are lowercase

If you provide a word not in the list, the solver will automatically select a valid word from the list.

## Requirements

- Python 3.7 or higher
- numpy
- matplotlib
- qiskit (optional, for quantum features)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 
