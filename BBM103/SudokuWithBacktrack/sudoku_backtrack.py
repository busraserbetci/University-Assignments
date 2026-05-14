import sys


def find_empty_location(board):
    # Find empty cell = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def calculate_probabilities(board):
    """ This function determines the possible values
        that can be placed in each empty cell"""

    probabilities = [[0 for _ in range(9)] for _ in range(9)]  # Create a 9x9 matrix

    for i in range(9):
        for j in range(9):
            # Check if the cell contains 0
            if board[i][j] == 0:
                # Find the set of values present in the current row, column and 3x3 grid
                row_values = set(board[i])
                col_values = set(board[row][j] for row in range(9))
                box_values = set(board[row][col] for row in range(i - i % 3, i - i % 3 + 3) for col in
                                 range(j - j % 3, j - j % 3 + 3))

                # Calculate the possible values for the empty cell
                empty_cell_probabilities = set(range(1, 10)) - row_values - col_values - box_values

                # Store the list of possible values in the probabilities matrix
                probabilities[i][j] = list(empty_cell_probabilities)

    return probabilities


def fill_single_probabilities(board):
    """ This function fills with the values of the sudoku grid cells
        where there is only one possible candidate value"""

    probabilities = calculate_probabilities(board)

    for i in range(9):
        for j in range(9):
            # Check if the cell is empty and has only one candidate value
            if board[i][j] == 0 and len(probabilities[i][j]) == 1:
                # Fill the cell with the single candidate valur
                board[i][j] = probabilities[i][j][0]


def fill_unique_row_numbers(board):
    """ This function fill cells in a Sudoku board
        where a number is uniquely determined within a row
        based on the calculated probabilities. """

    probabilities = calculate_probabilities(board)
    for i in range(len(probabilities)):
        # Count occurrences of each number in the current row
        number_counts = {}
        # Keep track of column indices where a number can appear
        element_index = {}

        for j in range(len(probabilities[i])):
            # Checks the probabilities for current cell are represent as a list.
            # This is done to ensure that there are multiple possibilities for a cell.
            if type(probabilities[i][j]) == list:
                # Iterates through each probability for the current cell
                for k in range(len(probabilities[i][j])):
                    number = probabilities[i][j][k]

                    # For each number in the list, it updates the number_counts dictionary,
                    # counting occurrences of the number in the row.
                    number_counts[number] = number_counts.get(number, 0) + 1

                    # Check if the number is already present in element_index
                    if number not in element_index:
                        # If not, create a new set for that number
                        element_index[number] = set()

                    # Add the column index j to the set for the current number
                    element_index[number].add(j)

        # Iterate through the counted numbers
        for number, count in number_counts.items():
            # Check if the number appears only once in the row
            if count == 1:
                # Get the column index from the set in element_index
                index = list(element_index[number])[0]
                # Place the unique number in the corresponding cell of the board
                board[i][index] = number

    # Return the modified board
    return board


def fill_unique_col_numbers(board):
    """ This function modifies the sudoku board by filling unique numbers for each column. """

    # Transpose the board to get columns as rows
    columns_list = [[row[i] for row in board] for i in range(9)]

    # Apply fill_unique_row_numbers to each transposed column
    # (which corresponds to the original rows)
    fill_unique_row_numbers(columns_list)

    rows_list = [[columns_list[j][i] for j in range(9)] for i in range(9)]

    return rows_list


def is_valid(board, row, col, num):
    """ This function checks whether the placed number complies with the
        sudoku rules by checking for the presence of the number in the same
        row, column and 3x3 grid. """

    # Check the presence of the number in the same row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check the presence of the number in the same column
    for j in range(9):
        if board[j][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3

    # Check the presence of the number in the 3x3 grid
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    # If the number is not present in the same row, column, or grid, it is valid
    return True


def solve_sudoku(board, probabilities):
    """ The function attempts to fill each empty cell with a valid number
            and recursively continues until sudoku is solved. """

    empty_location = find_empty_location(board)

    # If no empty cell is found, the puzzle is solved
    if not empty_location:
        return True

    row, col = empty_location

    # Try placing numbers 1 to 9 in the empty cell by using the list of possible candidate numbers.
    for num in probabilities[row][col]:
        if is_valid(board, row, col, num):
            # If the number is valid, place it in the cell
            board[row][col] = num

            # Recursively try to solve the rest of the puzzle
            if solve_sudoku(board, probabilities):
                return True

            # If placing the current number doesn't lead to a solution, backtrack
            board[row][col] = 0

    # No valid number was found for the current empty cell
    return False


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]


    with open(input_file, 'r') as file:
        sudoku_board = [list(map(int, line.split())) for line in file]

    fill_single_probabilities(sudoku_board)
    fill_unique_col_numbers(sudoku_board)
    fill_unique_row_numbers(sudoku_board)

    probabilities = calculate_probabilities(sudoku_board)

    if solve_sudoku(sudoku_board, probabilities):
        with open(output_file, 'w') as outputfile:
            for i in range(len(sudoku_board)):
                outputfile.write(" ".join(map(str, sudoku_board[i])))
                if i < len(sudoku_board) - 1:
                    outputfile.write('\n')



if __name__ == "__main__":
    main()
