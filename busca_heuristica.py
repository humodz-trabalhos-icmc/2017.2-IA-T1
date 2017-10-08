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
			if board[i][j] == None:
				return True
	return False

# Procura o dominio com mais restricoes
def max_restr(board):
	dom_board = domain.cell_domains(board)
	# size: tamanho maximo de cada dominio
	size = 9 
	maxdom = {}
	dominio = {}
	for i in range(0,9):
		for j in range(0,9): 
			dom = dom_board[i][j]
			t_aux = len(dom_board[i][j])
			# Verifica se o dominio nao eh igual a zero
			if (dom != {}):
				# Verifica se foi encontrado o menor
				if(t_aux <= size):
					size = t_aux 
					indice = [i,j]
					maxdom = dom
					# Se o dominio encontrado eh o minimo pra preencher entao serve esse
					if(size == 1): return([indice,list(maxdom)])
				# Senao foi entao ficamos com esse
				else:
					dominio = dom
					
	# Se todos os dominio sao vazio entao o sudoku nao tem solucao			 
	if(maxdom == {}) and (dominio == {}):
		return([[],[]])
	elif(maxdom != {}): 
		return ([indice, list(maxdom)])
	else:
		return ([indice, list(dominio)])
		
def busca_heuristica(sudoku):
	# Verifica se o sudoku esta resolvido
	if(procura_none(sudoku) == False):
		# Print de cada solucao encontrada
		print(sudoku)
		return
	
	# Procurando o dominio com mais restricoes
	[indice, dom] = max_restr(sudoku)
	# Verifica se tem solucao
	if([indice, dom] == [[],[]]):
		print("O sudoku nao tem solucao")
	else:
		# Preenche o sudoku 
		for d in range(0,len(dom)):
			sudoku[ indice[0] ][ indice[1] ] = dom[d]
			busca_heuristica(sudoku)
			
	# Volta ao valor vazio se nao achou nada		
	sudoku[ indice[0] ][ indice[1] ] = None 

# Gerando um sudoku nao resolvido
unsolved_board = numpy.array(boards.new_unsolved(45))

print(unsolved_board)

# Resolvendo o sudoku
busca_heuristica(unsolved_board)

