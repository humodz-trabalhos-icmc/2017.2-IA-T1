import numpy as np
import sys


# Convert input file to 9x9 np.array
# text: string (len=81) of digits 1-9 and periods
def convert_input(text):
    text = text.replace('.', '0')
    # Convert string of digits to list of ints
    int_list = list(map(int, text))
    # Convert list of ints to 9x9 np.array
    array = np.array(int_list).reshape(9, 9)
    return array


def display(board, file=sys.stdout):
    for row in board:
        for elem in row:
            if elem == 0:
                elem = '_'
            print(elem, end=' ', file=file)
        print()


def blind_search(text):
    board = convert_input(text)
    return blind_search_aux(board)


# Return value: (solved_board, num_steps)
#   solved_board is None if it couldn't be solved
def blind_search_aux(board, index1d=0):
    if index1d >= 81:  # Already solved
        return board, 0
    x, y = divmod(index1d, 9)

    # Find first empty cell
    while board[x, y] != 0:
        index1d += 1

        if index1d >= 81:  # Already solved
            return board, 0
        x, y = divmod(index1d, 9)

    new_index = index1d + 1
    total_backtracks = 0

    for value in range(1, 10):
        if is_available(value, board, x, y):
            board[x, y] = value
            new_board, backtracks = blind_search_aux(board, new_index)
            total_backtracks += backtracks

            if new_board is not None:
                # Found solution
                return new_board, total_backtracks

    # Return to original state
    board[x][y] = 0

    # Could not solve
    return None, total_backtracks + 1


# True if value can be placed at x, y
def is_available(value, board, x, y):
    # block coordinates
    bx = 3 * (x // 3)
    by = 3 * (y // 3)

    row = board[x, :]
    col = board[:, y]
    block = board[bx:bx+3, by:by+3]

    joined = np.concatenate((row, col, block.flatten()))
    return value not in joined


def go():
    ln = open('input.txt').readline().replace('\n', '')
    return blind_search(ln)
