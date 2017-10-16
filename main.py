import sys

import informed
import blind


# Usage:
# python main.py < input.txt > output.csv

print_header = '--header' in sys.argv
print_answer = '--show' in sys.argv


if print_header:
    print('blind,informed')

puzzle_count = 0

for line in sys.stdin:
    puzzle_count += 1

    line = line.replace('\n', '').replace('\r', '')
    assert len(line) == 81, 'Linha de tamanho errado: {}.'.format(len(line))

    blind_result = blind.blind_search(line)
    informed_result = informed.solve_w_heuristics(line)

    b_board, b_backtracks = blind_result
    i_board, i_backtracks = informed_result
    print(b_backtracks, i_backtracks)

    if print_answer:
        print()
        blind.display(b_board, file=sys.stderr)
        print()
        informed.display(i_board, file=sys.stderr)

print('Total de casos:', puzzle_count, file=sys.stderr)
