import numpy as np
from copy import deepcopy
from random import sample


text_board = """
    5 3 4  6 7 8  9 1 2
    6 7 2  1 9 5  3 4 8
    1 9 8  3 4 2  5 6 7
    8 5 9  7 6 1  4 2 3
    4 2 6  8 5 3  7 9 1
    7 1 3  9 2 4  8 5 6
    9 6 1  5 3 7  2 8 4
    2 8 7  4 1 9  6 3 5
    3 4 5  2 8 6  1 7 9
"""

text_board = """
    4 3 8  7 6 5  1 9 2
    2 6 1  8 9 4  5 3 7
    5 7 9  1 3 2  6 4 8

    1 8 4  9 2 3  7 5 6
    3 9 2  5 7 6  8 1 4
    6 5 7  4 8 1  9 2 3

    8 4 5  2 1 7  3 6 9
    7 1 6  3 4 9  2 8 5
    9 2 3  6 5 8  4 7 1
"""


# Convert string (like above) to np.array 9x9 of int
def convert_input(text):
    int_list = list(map(int, text.split()))
    mat2d = np.array(int_list, dtype=np.int).reshape([9, 9])
    return mat2d


solved_board = convert_input(text_board)


# Return copy of <solved> with some values removed
def make_unsolved(num_holes, solved=solved_board):
    assert 0 <= num_holes and num_holes <= 81
    assert solved.shape == (9, 9)

    unsolved = deepcopy(solved)

    for index1d in sample(range(81), num_holes):
        x, y = divmod(index1d, 9)
        unsolved[x][y] = 0

    return unsolved


def display(board):
    for row in board:
        for elem in row:
            if elem == 0:
                elem = '_'
            print(elem, end=' ')
        print()


def blind_search(board):
    return blind_search_aux(deepcopy(board))


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
    total_steps = 0

    for value in range(1, 10):
        if is_available(value, board, x, y):
            board[x, y] = value
            new_board, steps = blind_search_aux(board, new_index)
            total_steps += steps + 1

            if new_board is not None:
                # Found solution
                return new_board, total_steps

    # Return to original state
    board[x][y] = 0

    # Could not solve
    return None, total_steps


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


def test_performance(solver=blind_search):
    print('holes\tsteps')
    for holes in range(5, 81, 5):
        board = make_unsolved(holes)
        result = solver(board)
        print('{}\t{}'.format(holes, result[1]))
