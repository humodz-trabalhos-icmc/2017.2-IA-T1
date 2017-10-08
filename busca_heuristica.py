import sys
import random
import copy
import numpy
import boards
import domain



# Verifica se no sudoku se tem algum None      
def procura_none(board):
	for i in range(0,9):
		for j in range(0,9):
			if board[i][j] == None: return True
	return False

# Procura o dominio com mais restricoes
def max_restr(board):
	dom_board = domain.cell_domains(board)
	# tamanho maximo do dominio
	size = 9 
	maxdom = {}
	for i in range(0,9):
		for j in range(0,9): 
			dom = dom_board[i][j]
			t_aux = len(dom_board[i][j])
			if (t_aux <= size) and (dom != {}):
				size = t_aux 
				indice = [i,j]
				maxdom = dom
				if(size == 1): return([indice,list(maxdom)])
	# Se todos os dominio sao vazio entao o sudoku nao tem solucao			 
	if(maxdom == {}):
		return([[],[]])
	else: return ([indice, list(maxdom)])


def busca_cega(board):
	# Verifica se o sudoku esta resolvido
	#if(procura_none(board) == False):
	#	print(board)
    #    return
    
	[indice, dom] = max_restr(board)
	# Verifica se tem solucao
	if([indice, dom] == [[],[]]):
		print("O sudoku nao tem solucao")
	else:
		# Preenche o sudoku
		for i in range(0,len(dom)):
			#print(dom[i])
            board[indice[0]][indice[1]] = dom[i]
            busca_cega(board)
		
			
        
unsolved_board = numpy.array(boards.new_unsolved(45))
# sudoku nao resolvido
print(unsolved_board)
# sudoku resolvido

## comeca a busca do inicio
### Aqui poderia comecar procurando a celula que tem mais restricoes para comecar 
solved_board = busca_cega(unsolved_board)
print(solved_board)
#print(domain.cell_domains(unsolved_board))
#print(max_restr(unsolved_board))

