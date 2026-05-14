import sys


def parse_input(input_lines):
    return [line.split() for line in input_lines[4:]]


def read_constraints():
    with open(sys.argv[1], 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    highs_col = list(map(int, lines[0].split()))
    bases_col = list(map(int, lines[1].split()))
    highs_row = list(map(int, lines[2].split()))
    bases_row = list(map(int, lines[3].split()))

    return highs_col, bases_col, highs_row, bases_row


def is_valid_placement(tile, count, constraint):
    return constraint == -1 or count <= constraint

def is_valid(row, col, tile, result, constraints):

    # Check constraints for 'H' in the given row
    count_h_row = result[row].count('H')
    if not is_valid_placement('H', count_h_row, constraints[0][row]):
       return False

    # Check constraints for 'B' in the given row
    count_b_row = result[row].count('B')
    if not is_valid_placement('B', count_b_row, constraints[1][row]):
        return False

    # Check constraints for 'H' in the given column
    count_h_col = sum(result[i][col] == 'H' for i in range(len(result)))
    if not is_valid_placement('H', count_h_col, constraints[2][col]):
        return False

    # Check constraints for 'B' in the given column
    count_b_col = sum(result[i][col] == 'B' for i in range(len(result)))
    if not is_valid_placement('B', count_b_col, constraints[3][col]):
        return False

    if tile == 'H':
        if row > 0 and result[row - 1][col] == 'H':
            return False
        if col > 0 and result[row][col - 1] == 'H':
            return False
    elif tile == 'B':
        if row > 0 and result[row - 1][col] == 'B':
            return False
        if col > 0 and result[row][col - 1] == 'B':
            return False

    return True

def solve_blind_valley(template):
    rows, cols = len(template), len(template[0])
    result = [['N' for _ in range(cols)] for _ in range(rows)]
    constraints = read_constraints()

    def backtrack(row, col):
        if row == rows:
            return True

        next_row, next_col = (row, col + 1) if col + 1 < cols else (row + 1, 0)

        if template[row][col] == 'L':
            for tile in ['H', 'B', 'N']:
                if is_valid(row, col, tile, result, constraints):
                    result[row][col] = tile
                    if backtrack(next_row, next_col):
                        return True
                    result[row][col] = ' '
        elif template[row][col] == 'R':
            for tile in ['H', 'B', 'N']:
                if is_valid(row, col, tile, result, constraints):
                    result[row][col] = tile
                    if backtrack(next_row, next_col):
                        return True
                    result[row][col] = ' '
        elif template[row][col] == 'U':
            for tile in ['H', 'B', 'N']:
                if is_valid(row, col, tile, result, constraints):
                    result[row][col] = tile
                    if backtrack(next_row, next_col):
                        return True
                    result[row][col] = ' '
        elif template[row][col] == 'D':
            for tile in ['H', 'B', 'N']:
                if is_valid(row, col, tile, result, constraints):
                    result[row][col] = tile
                    if backtrack(next_row, next_col):
                        return True
                    result[row][col] = ' '

        for r in result:
            print(r)
        print()
        return False

    if backtrack(0, 0):
        with open(sys.argv[2], 'w') as output_file:
            for row in result:
                output_file.write(' '.join(['H' if cell == 'H'
                                            else 'B' if cell == 'B'
                                            else 'N' for cell in row]) + '\n')
    else:
        with open(sys.argv[2], 'w') as output_file:
            output_file.write("No solution!")


def main():
    # Read input from a file
    with open(sys.argv[1], 'r') as file:
        input_lines = [line.strip() for line in file.readlines()]

    # Parse input
    template = parse_input(input_lines)

    # Solve and write the result to a file
    solve_blind_valley(template)


if __name__ == "__main__":
    main()
