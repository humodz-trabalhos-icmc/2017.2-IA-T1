import sys
import random
import copy
import numpy
import sudoku_function.py

# Procura o domínio com mais restrições
def max_restr(solved_board):
  max = -1;
  indice = [None,None];
  for i in range(1,10):
    for j in range(1,10):
      ## Nao sei ainda como vai ser
      if len(inteseccao) > max 
      indice = [i,j];
      
# Procura se o sudoku não está preenchido      
def procura_none(solved_board):
  for i in range(1,10):
    for j in range(1,10):
      if solved_board[i][j] == None: return True
      else: return False


def busca_cega(r, c):
    # Verificando se o sudoku ja foi resolvido
    if (procura_none(solved_board) == False): # Imprimir a solucao
        print(solved_board)
        return

    # Calcula a proxima celda para prencher
    posicao = max_restr(solved_board)
    nR = posicao[0]
    nC = posicao[1]
      
    # Verifica se a celula (r,c) é vazia, senão estiver vai pra proxima celula calculada acima (nR,nC)  
    if solved_board[r][c] != None:
        busca_cega(nR, nC)
    else:
        # Verifica os valores possiveis nessa celulas
        
        #possible_values = ? funcao() ## recebe os valores possiveis

        # Faz a busca em pronfundidade
        for i in len(possible_values):
            solved_board[r][c] = i # Encho com o possivel valor
            busca_cega(nR, nC)
                
        # Se nao for possivel preencher entao fica vazio 
        solved_board[r][c] = None # Volto ao valor vazio

        
solved_board = numpy.array(random_puzzle(45))
# sudoku nao resolvido
print(solved_board)
# sudoku resolvido

# Supondo que sempre tera uma posicao
posicao = max_restr(solved_board) 
busca_cega(posicao[0],posicao[1])
