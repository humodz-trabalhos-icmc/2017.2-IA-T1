import sys
import random
import copy
import numpy
import boards
import domain


# Nao consegui pensar em algo mais eficiente nessas
# duas funcoes max_restr e procura_none
# Procura o dominio com mais restricoes
def max_restr(solved_board):
    # sem restricao
    max = 9
    indice = [None, None]
    for i in range(1, 10):
        for j in range(1, 10):
            aux = domain.calculate_domains(solved_board)
            dom = domain.get_domain_at(i, j, aux)
            if len(dom) < max:
                max = len(dom)
        indice = [i, j]
        maxdom = dom
        if(maxdom == 0):
            return ([indice, list(dom)])
        else:
            return ([indice, list(maxdom)])


# Procura se o sudoku nao esta preenchido
def procura_none(solved_board):
    for i in range(1, 10):
        for j in range(1, 10):
            if solved_board[i][j] is not None:
                return True
            else:
                return False


def busca_cega(r, c, possible_values):
    # Verificando se o sudoku ja foi resolvido
    if procura_none(solved_board) is False:  # Imprimir a solucao
        print(solved_board)
        return

    # Calcula a proxima celda para prencher
    # Verificar se eh a proxima mesmo
    [posicao, next_possible_values] = max_restr(solved_board)
    nR = posicao[0]
    nC = posicao[1]

    # Verifica se a celula (r,c) eh vazia, senao estiver vai pra proxima celula
    # calculada acima (nR,nC)
    if solved_board[r][c] is not None:
        busca_cega(nR, nC, next_possible_values)
    else:

        # Faz a busca em pronfundidade
        for i in len(possible_values):
            solved_board[r][c] = possible_values[i]  # Preenche
            busca_cega(nR, nC, possible_values)

        # Se nao for possivel preencher entao fica vazio
        solved_board[r][c] = None  # Volto ao valor vazio


solved_board = numpy.array(boards.generate_unsolved(45))
# sudoku nao resolvido
print(solved_board)
# sudoku resolvido

# Supondo que sempre tera uma posicao
[posicao, possible_values] = max_restr(solved_board)
busca_cega(posicao[0], posicao[1], possible_values)
