import sys
import random
import copy
import numpy

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

def random_puzzle(num_holes, full_board=solved_board):
    if not (0 < num_holes and num_holes <= 81):
        raise Exception('num_holes must be in the range 0 < ... <= 81')

    result = copy.deepcopy(full_board)

    for index1d in random.sample(range(81), num_holes):
        x, y = divmod(index1d, 9)
        result[x][y] = None

    return result

def busca_cega(r, c):
    if (r == 9 and c == 0): # Imprimir a solucao
        print(solved_board)
        return

    # Calcula a proxima celda para prencher
    if ((c + 1) % 9) == 0: nR = r + 1
    else: nR = r
    
    nC = (c + 1) % 9

    if solved_board[r][c] != None:
        busca_cega(nR, nC)
    else:
        possible_values = [True for i in range(10)]

        # Verifica as linhas
        for i in range(0, 9):
            if solved_board[r][i] != None:
                possible_values[solved_board[r][i]] = False

        # Verifica as colunas
        for i in range(0, 9):
            if solved_board[i][c] != None:
                possible_values[solved_board[i][c]] = False

        # Verifica os bloquinhos 3x3
        iStart = (r // 3) * 3
        iEnd = iStart + 3
        jStart = (c // 3) * 3
        jEnd = jStart + 3

        for i in range(iStart, iEnd):
            for j in range(jStart, jEnd):
                if solved_board[i][j] != None:
                    possible_values[solved_board[i][j]] = False
                

        # Faz a busca em pronfundidade
        for i in range(1, 10):
            if possible_values[i]:
                solved_board[r][c] = i # Encho com o possivel valor
                busca_cega(nR, nC)

        solved_board[r][c] = None # Volto ao valor vazio

        
solved_board = numpy.array(random_puzzle(30))
# sudoku nao resolvido
print(solved_board)
# sudoku resolvido
busca_cega(0, 0)
