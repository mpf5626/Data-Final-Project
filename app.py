from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Constants
ROWS, COLS = 10, 10
NUM_MINES = 10

# Game state
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

def initialize_board():
    # Create a blank game board
    global board
    global revealed
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

    # Place mines randomly on the board
    mines = random.sample(range(ROWS * COLS), NUM_MINES)
    for mine in mines:
        row = mine // COLS
        col = mine % COLS
        board[row][col] = 'X'

    return board

def count_adjacent_mines(row, col):
    count = 0
    for i in range(max(0, row - 1), min(ROWS, row + 2)):
        for j in range(max(0, col - 1), min(COLS, col + 2)):
            if board[i][j] == 'X':
                count += 1
    return count

def reveal_cell(row, col):
    if revealed[row][col]:
        return

    revealed[row][col] = True

    if board[row][col] == 'X':
        return False  # Game Over
    else:
        mines_nearby = count_adjacent_mines(row, col)
        if mines_nearby == 0:
            for i in range(max(0, row - 1), min(ROWS, row + 2)):
                for j in range(max(0, col - 1), min(COLS, col + 2)):
                    reveal_cell(i, j)

    return True

@app.route('/')
def index():
    initialize_board()
    return render_template('minesweeper.html', rows=ROWS, cols=COLS, board=board, revealed=revealed)

@app.route('/reveal', methods=['POST'])
def reveal():
    row = int(request.form['row'])
    col = int(request.form['col'])

    result = reveal_cell(row, col)

    return {'result': result, 'board': board, 'revealed': revealed}

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use a different port, e.g., 5001

