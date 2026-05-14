import sys

# Function to read key matrix from file
def read_key_matrix(key_file):
    try:
        with open(key_file, 'r') as f:
            lines = f.readlines()
            key_matrix = []
            for line in lines:
                row = [int(num) for num in line.strip().split(',')]
                key_matrix.append(row)
            return key_matrix
    except FileNotFoundError:
        print("Error: Key file not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid character in key file.")
        sys.exit(1)

# Function to read input text from file
def read_input_text(input_file):
    try:
        with open(input_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: Input file not found.")
        sys.exit(1)

# Function to encode text into numbers
def encode_text(text):
    mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
               'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
               'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, ' ': 27}
    encoded_text = []
    for char in text:
        if char.upper() in mapping:
            encoded_text.append(mapping[char.upper()])
        elif char in ',':  # Add support for commas
            pass
        else:
            print(f"Character '{char}' not found in mapping.")
    return encoded_text

# Function to divide numbers into matrices
def divide_into_matrices(numbers, matrix_size):
    return [numbers[i:i+matrix_size] for i in range(0, len(numbers), matrix_size)]

# Function to perform matrix multiplication
def matrix_multiplication(matrix_a, matrix_b):
    # Perform matrix multiplication
    result = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_b[0])):
            value = 0
            for k in range(len(matrix_a[0])):
                value += matrix_a[i][k] * matrix_b[k][j]
            row.append(value)
        result.append(row)
    return result

# Function to calculate inverse of a matrix
def matrix_inversion(matrix):
    # Calculate the inverse of the matrix using Gaussian elimination
    n = len(matrix)
    identity = [[0] * n for _ in range(n)]
    for i in range(n):
        identity[i][i] = 1

    for i in range(n):
        # Find pivot row
        pivot_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                pivot_row = j
        # Swap rows
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        identity[i], identity[pivot_row] = identity[pivot_row], identity[i]

        # Scale pivot row to have 1 in pivot position
        scale = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= scale
            identity[i][j] /= scale

        # Eliminate other rows
        for j in range(n):
            if j != i:
                scale = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= scale * matrix[i][k]
                    identity[j][k] -= scale * identity[i][k]

    # Round float values to integers
    for i in range(n):
        for j in range(n):
            matrix[i][j] = round(matrix[i][j])

    return identity

# Function to decrypt text using key matrix
def decrypt_text(text, key_matrix):
    key_matrix_inv = matrix_inversion(key_matrix)
    try:
        decrypted_numbers = [[int(num)] for num in text.strip().replace(',', '').split()]
    except ValueError:
        print("Error: The input text could not be read.")
        sys.exit(1)
    decrypted_matrices = [matrix_multiplication([matrix], key_matrix_inv)[0][0] for matrix in decrypted_numbers]
    decrypted_text = ''.join([chr(int(num) + 64) if int(num) <= 26 else ' ' for num in decrypted_matrices])
    return decrypted_text

# Function to write output to file
def write_output(output_file, data):
    try:
        with open(output_file, 'w') as f:
            f.write(data)
            print(f"Output written to {output_file}")
    except Exception as e:
        print("Error: Output file could not be written.")
        print(e)
        sys.exit(1)

# Main function
def main():
    # Check if correct number of parameters are provided
    if len(sys.argv) != 5:
        print("Error: Parameter number")
        sys.exit(1)

    # Extract parameters
    operation_type = sys.argv[1]
    key_file = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    # Check operation type
    if operation_type not in ['enc', 'dec']:
        print("Error: Undefined parameter")
        sys.exit(1)

    # Read key matrix
    key_matrix = read_key_matrix(key_file)

    # Perform encryption or decryption based on operation type
    if operation_type == 'enc':
        # Read input text
        input_text = read_input_text(input_file)
        # Encode text into numbers
        encoded_numbers = encode_text(input_text)
        # Divide numbers into matrices
        input_matrices = divide_into_matrices(encoded_numbers, len(key_matrix))
        # Encrypt text
        encrypted_matrices = [matrix_multiplication([matrix], key_matrix) for matrix in input_matrices]
        encrypted_numbers = [num for matrix in encrypted_matrices for num in matrix[0]]
        encrypted_text = ','.join(map(str, encrypted_numbers))
        # Write encrypted text to output file
        write_output(output_file, encrypted_text)
    elif operation_type == 'dec':
        # Read encrypted text
        encrypted_text = read_input_text(input_file)
        # Decrypt text
        decrypted_text = decrypt_text(encrypted_text, key_matrix)
        # Write decrypted text to output file
        write_output(output_file, decrypted_text)

if __name__ == "__main__":
    main()
