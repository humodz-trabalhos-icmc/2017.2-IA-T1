#<<< nao atualiza tab só os domínios
import collections

def combine(rows, cols): 
	'''Cria representações de todas as combinações 
		entre as linhas e as colunas inseritas '''
	return [row + col for row in rows for col in cols]


DIGITS = '123456789'
ALL_ROWS = 'ABCDEFGHI'
ALL_COLS = DIGITS
ALL_SQUARES = combine(ALL_ROWS, ALL_COLS)

# unit (unidade): bloco, linha ou coluna
ALL_UNITS = ([combine(ALL_ROWS, c) for c in ALL_COLS] # unidades de colunas
			+ [combine(r, ALL_COLS) for r in ALL_ROWS] # unidades de linhas
			+ [combine(rows, cols) for rows in ['ABC', 'DEF', 'GHI'] for cols in ['123', '456', '789']])

# dicionário que relaciona quadrado e unidades impactadas pelo mesmo
impacted_units = dict((sqr, [unit for unit in ALL_UNITS if sqr in unit])
					for sqr in ALL_SQUARES)

# peers (colegas): quadrados impactados por um dado quadrado
# dicionário que relaciona quadrado e os demais quadrados impactados pelo mesmo 
impacted_peers = dict((sqr, set().union(*impacted_units[sqr])-set([sqr])) # todos os quadrados das suas units menos si mesmo
					for sqr in ALL_SQUARES)

def init_domains(start_grid_str): 
	''' Recebe a string representando o 'tabuleiro' 
		e devolve o dicionário que representa o domínio de cada quadrado.
		{<quadrado>, <string com todos os dígitos possíveis>}
		A fim de adiantar o resultado,
		propaga-se imediatamente os dígitos fixos, 
		resolvendo assim os quadrados que só apresentam 1 possibilidade desde o começo.
	'''
	# filtra qualquer caracter 'de enfeite',
	# transformando a entrada em uma array de caracteres que incluem apenas dígitos e símbolos de vazio('_', '0' ou '.')
	start_grid_ch_array = [ch for ch in start_grid_str if ch in DIGITS or ch in '0._']
	if len(start_grid_ch_array) != 81:
		print('Tabuleiro de tamanho inconsitente')
		return False
	
	start_grid_dict = dict(zip(ALL_SQUARES, start_grid_ch_array)) # {<quadrado>, <valor inicial>} 

	domains = dict((sqr, DIGITS) for sqr in ALL_SQUARES) # inicia todos os quadrados com todos os dígitos sendo possíveis

	# inicializa o domínio e propaga os quadrados marcados
	for sqr, val in start_grid_dict.items():
		if val in DIGITS:
			res = assign(domains, sqr, val) # se estiver preenchido, refletir isso no domínio e nos seus impactados
			# <<<<< ver .com
	return domains


def assign(domains, sqr, val):
	'''
		Tenta atribuir um novo valor a um dado quadrado.
		(Removendo o valor dos domínios dos quadrados de impacto)
	'''
	if all(eliminate(domains, sqr, diff_val) 
		for diff_val in domains[sqr] if diff_val != val): # se eliminar todas as outras possibilidade não quebrar nada
			return domains # dicts são passados por referência, logo foi atualizado em eliminate()
	else:
		return False # atribuição quebra algum outro quadrado

def eliminate(domains, sqr, val):
	''' 
		Remove um dado valor do domínio de um dado quadrado. 
		Testa as consequências dessa remoção(forward checking).
		Propaga as restrições de valores acabaram sendo atribuídos devido a essa remoção. 
	'''
	if val not in domains[sqr]: # já não era uma possibilidade
		return domains # não precisa fazer nada porque não alterou o domínio

	domains[sqr] = domains[sqr].replace(val, '') # remove de fato
	# <<< ver a questão da cópia
	
	# ======= FORWARD CHECKING =======
	if len(domains[sqr]) == 0:
		return False # alteração de domínio inválida pois quadrado fica sem opções
	
	# ===== PROPAGAÇÃO DE RESTRIÇÕES ====
	# checa se só restou uma opção no quadrado (atribuição involuntária)
	if len(domains[sqr]) == 1: 
			final_val = domains[sqr] 
			# forward checking dessa 'subatribuição'
			if not all(eliminate(domains, peer, final_val)
					for peer in impacted_peers[sqr]): # elimina valor atribuído de todos os afetados
				return False # atribuição com consequências inválidas

	# checa se alguma unidade afetada por esse quadrado sofreu uma atribuição involuntária do valor por causa do valor removido
	for unit in impacted_units[sqr]:
		unit_domain = [peer for peer in unit if val in domains[peer]] # lista colegas que ainda tem o valor
		if len(unit_domain) == 0: # não sobrou nenhum lugar para esse valor
			return False
		if len(unit_domain) == 1: # ou seja, realizar uma atribuição ali não afeta ninguém mais
			sqr2 = unit_domain[0]
			if not assign(domains, sqr2, val):
				return False
	return domains


def mrv(domains):
	''' 
		Retorna o quadrado não-preechido de menor domínio.
	'''
	min_len_dom, next_sqr = min((len(domains[sqr]), sqr) for sqr in ALL_SQUARES if len(domains[sqr]) > 1) 

	# << adicionar desempate por grau depois
	return next_sqr


def less_restrictive_value_seq(domains, sqr):
	'''
		Retorna o dígito que quando atribuído ao quadrado sqr afeta o menor número de quadrados.
	'''
	all_peer_domains = ''.join([domains[p] for p in impacted_peers[sqr]])
	counts = collections.Counter(all_peer_domains)
	seq = sorted(counts.items(), key = lambda i: i[1])

	return [item[0] for item in seq if item[0] in domains[sqr]]


def try_new_val(domains):
	'''
		Encontra valores e variáveis em potencial e testa sua validade.
		Retorna:
			- Sudoku resolvido até o momento.
			- Nº de passos dados.
	'''
	total_steps = 0
	if all(len(domains[sqr]) == 1 for sqr in ALL_SQUARES): # todos os quadrados ficaram só com 1 opção
		return domains, total_steps

	chosen_sqr = mrv(domains)
	
	for val in less_restrictive_value_seq(domains, chosen_sqr):
		old_domains = domains.copy()
		
		domains = assign(domains, chosen_sqr, val)
		if domains is not False:
			domains, partial_steps = try_new_val(domains)
			total_steps += partial_steps + 1
			if domains is not False:
			 	return domains, total_steps
			else:
				domains = old_domains
		else:
			domains = old_domains

	return False, total_steps


# >>>>>>>>>>>>>>>> Código bonito que o Hugo fez eu apagar! <<<<<<<<<<<<<<<

# def try_new_val(domains):
# 	if domains is False:
# 		return False

# 	if all(len(domains[sqr]) == 1 for sqr in ALL_SQUARES): # todos os quadrados ficaram só com 1 opção
# 		return domains 

# 	chosen_sqr = mrv(domains)
	
# 	for val in less_restrictive_value_seq(domains, chosen_sqr):
# 		old_domains = domains.copy()
# 		domains = try_new_val(assign(domains, chosen_sqr, val))
# 		if domains is not False:
# 			return domains
# 		else:
# 			domains = old_domains

# 	return False


def display(values):
    ''' 
    	Imprime o sudoku.
    '''
    if not values:
    	print('False recebido por display(values)')
    	return

    width = 1 + max(len(values[s]) for s in ALL_SQUARES)
    line = '+'.join(['-'*(width*3)]*3)
    for r in ALL_ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in ALL_COLS))
        if r in 'CF': print(line)
    print('\n')

if __name__ == '__main__':
	input = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
	
	domains = init_domains(input)
	result, n_steps = try_new_val(domains)
	display(result)
	print(n_steps)

	
