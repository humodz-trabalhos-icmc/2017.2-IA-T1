import numpy as np
import boards


# board: np.array of shape 9x9
# return value: tuple (len=3) of
#   1. list (len 9) of sets (row domains)
#   2. list (len 9) of sets (column domains)
#   3. 2d list (len 3,3) of sets (block domains)
def calculate_domains(board):
    full_domain = set(range(1, 10))

    row_domains = [
        full_domain - set(row)
        for row in board
    ]

    col_domains = [
        full_domain - set(col)
        for col in board.T
    ]

    blocks = block_split(board)

    # Eu ia fazer esse que nem os outros, mas ficou bem confuso de ler
    block_domains = [
        [
            full_domain - set(block.flatten())
            for block in row_of_blocks
        ]
        for row_of_blocks in blocks
    ]

    return (row_domains, col_domains, block_domains)


# Note: use cell_domains insted
# all_domains: return value of calculate_domains()
# return value: set
def get_domain_at(row, col, all_domains):
    row_doms, col_doms, block_doms = all_domains

    row_domain = row_doms[row]
    col_domain = col_doms[col]
    block_domain = block_doms[row // 3][col // 3]
    intersection = row_domain & col_domain & block_domain

    return intersection


# all_domains: (optional) return value of calculate_domains(board)
# return value: 81x81 matrix of sets
def cell_domains(board, all_domains=None):
    if all_domains is None:
        all_domains = calculate_domains(board)

    rowd, cold, blockd = all_domains

    result = np.empty((9, 9), dtype=object)

    for x in range(9):
        for y in range(9):
            # insersection of domains
            if board[x][y] is None:
                result[x][y] = rowd[x] & cold[y] & blockd[x // 3][y // 3]
            else:
                result[x][y] = {}

    return result


# Split <board> into 3x3 matrix of blocks
def block_split(board):
    # split board into 3 np.arrays, each containing 3 rows
    rows_of_blocks = np.split(board, 3)

    # 3x3 matrix of blocks
    blocks = [
        np.hsplit(row, 3)
        for row in rows_of_blocks
    ]

    return blocks


# Count number of valid state transitions from current board state
# cell_doms: return value of cell_domains
def count_paths(cell_doms):
    fn = np.vectorize(len)
    return np.sum(fn(cell_doms))
