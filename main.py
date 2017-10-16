import sudoku_com_heuristicas as sch
import sys

count = 0
total_h = 0
for line in sys.stdin:
	line = line.replace('\n', '')
	if len(line) != 81:
		print('Erro: entrada inválida')
		continue
	result, n_back_h = sch.solve_w_heuristics(line)
	count += 1
	total_h += n_back_h
	if len(sys.argv) > 1 and sys.argv[1] == '--show':
		print()
		sch.display(result)
	print(str(n_back_h) + ' backtrackings realizados')
print('Média : '+ str(total_h/count))