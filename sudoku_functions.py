import sys
import random
import copy


# x: str containing and integer or '_'
def convert(x):
    if x != '_':
        return int(x)
    else:
        return None


# Reads 9 lines, each containing 9 elements separated by spaces
# _ from input is converted to None
# Returns a 9x9 matrix of ints and Nones
def read_board():
    if sys.version < 3:  # python 2
        input = raw_input  # noqa

    board = []
    for _ in range(9):
        line = input().split()
        if len(line) != 9:
            raise Exception('Linha de tamanho errado')
        line = list(map(convert, line))
        board += [line]
    return board


solved_board = [
    '5 3 4  6 7 8  9 1 2',
    '6 7 2  1 9 5  3 4 8',
    '1 9 8  3 4 2  5 6 7',
    '8 5 9  7 6 1  4 2 3',
    '4 2 6  8 5 3  7 9 1',
    '7 1 3  9 2 4  8 5 6',
    '9 6 1  5 3 7  2 8 4',
    '2 8 7  4 1 9  6 3 5',
    '3 4 5  2 8 6  1 7 9',
]

solved_board = [
    list(map(int, line.split()))
    for line in solved_board
]


# num_holes: int in the range 0 < ... <= 81
# full_board: 9x9 matrix of ints and Nones
# Returns a copy of <full_board> with <num_holes> elements set to None
def random_puzzle(num_holes, full_board=solved_board):
    if not (0 < num_holes and num_holes <= 81):
        raise Exception('num_holes must be in the range 0 < ... <= 81')

    result = copy.deepcopy(full_board)

    for index1d in random.sample(range(81), num_holes):
        x, y = divmod(index1d, 9)
        result[x][y] = None

    return result
