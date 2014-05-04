import sys
from sudoku_solver import SudokuSolver

# Usage:
# python solve.py 093105640 700000005 501209307 200000003 036907520 900000001 302408109 600000004 047302850
#
# 8 9 3 1 7 5 6 4 2
# 7 2 4 8 3 6 9 1 5
# 5 6 1 2 4 9 3 8 7
# 2 1 5 6 8 4 7 9 3
# 4 3 6 9 1 7 5 2 8
# 9 7 8 5 2 3 4 6 1
# 3 5 2 4 6 8 1 7 9
# 6 8 9 7 5 1 2 3 4
# 1 4 7 3 9 2 8 5 6

def solve(row_list):
    rows = [map(int, list(row)) for row in row_list]
    solver = SudokuSolver()
    result = solver.solve(rows)
    output(result)

def output(rows):
    print('')
    for row in rows:
        print(' '.join(map(str, row)))

if __name__ == '__main__':
    if len(sys.argv) != 10:
        print('Usage: python solve.py row1 row2 ... row9')
        sys.exit(0)
    rows = [arg for arg in sys.argv[1:]]
    solve(rows)
