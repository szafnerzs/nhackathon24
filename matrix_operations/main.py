def read_matrices(lines):
    matrices = {}
    index = 2  # skips "matrices"
    while index < len(lines):
        line = lines[index].strip()

        if line == 'operations':
            break
        # gives matrix ID from the current line
        matrix_id = line
        index += 1
        matrix = []

        while index < len(lines) and lines[index].strip():
            # split the line into integers and store them as a row in the matrix
            matrix.append(list(map(int, lines[index].strip().split())))
            index += 1
        # store the matrix data in the dictionary using its ID as Dict. Key
        matrices[matrix_id] = matrix
        index += 1  # skip blank line
    # return the dictionary of the matrices and the index where the function starts
    return matrices, index + 1

def read_operations(lines, start_index):
    # extract operations from the lines starting from the given index
    return [line.strip() for line in lines[start_index:] if line.strip()]

def to_postfix(expression, operator):
    # convert infix expression to postfix
    postfix_expr = []
    storage = []
    # loop through each character in the expression
    for char in expression.replace(' ', ''):
        # check if the character is an operator
        if char in operator:

            # pop operators with higher or equal precedence from storage
            while storage and storage[-1] != '(' and operator[char] <= operator[storage[-1]]:
                postfix_expr.append(storage.pop())
            storage.append(char)
    else:
        # append operands directly to the postfix expression
        postfix_expr.append(char)
    # append remaining operators from the storage to the postfix expression
    postfix_expr.extend(reversed(storage))
    return postfix_expr

def compute_expression(expression, matrices, operator):
    # evaluates the postfix expression using matrices
    storage = []
    # loopss through each token in the expression
    for char in expression:
        if char in operator:
            # pops two matrices from storage and do the operations
            b = storage.pop()
            a = storage.pop()
            if char == '+':
                # add matrices element-wise
                result = [[a[i][n] + b[i][n] for n in range(len(a[0]))] for i in range(len(a))]
            elif char == '*':
                # matrix multiplication
                result = [[sum(a[i][k] * b[k][n] for k in range(len(a[0]))) for n in range(len(b[0]))] for i in range(len(a))]
            storage.append(result)
        else:
            # push matrix onto the storage
            storage.append(matrices[char])
    return storage.pop()

def format_matrix(matrix):
    # format matrix as a string
    return '\n'.join([' '.join(map(str, row)) for row in matrix])

# open the input file
with open('./input.txt', 'r') as file:
    lines = file.readlines()

# read matrices and operations from the input_file
matrix_data, operation_start_index = read_matrices(lines)
operation_list = read_operations(lines, operation_start_index)
# gives back the operations needed
operator = {'+': 1, '*': 2}

# loop through each operation and compute the results
for operation in operation_list:
    postfix_expr = to_postfix(operation, operator)
    result_matrix = compute_expression(postfix_expr, matrix_data, operator)
    formatted_output = format_matrix(result_matrix)
    print(operation, formatted_output, end='\n\n', sep='\n')
