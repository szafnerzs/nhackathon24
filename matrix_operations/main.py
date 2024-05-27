def read_matrices(lines):
    matrices = {}  # holds matrices data
    index = 2  # starts after the 'matrices' line

    while index < len(lines):
        line = lines[index].strip()

        if line == 'operations':
            break
        # takes out matrix ID from the current line
        matrix_id = line
        index += 1
        matrix = []
        # Read matrix elements until encountering a blank line or the end of the file
        while index < len(lines) and lines[index].strip():
            # Split the line into integers and store them as a row in the matrix
            matrix.append(list(map(int, lines[index].strip().split())))
            index += 1
        # Store the matrix data in the dict using its ID
        matrices[matrix_id] = matrix
        index += 1  # Skip blank line
    # Return the dictionary of matrices and the index where the operations start
    return matrices, index + 1

def read_operations(lines, start_index):
    # extract operations from the lines starting from the given index
    return [line.strip() for line in lines[start_index:] if line.strip()]

def to_postfix(expression, operator):
    # convert infix expression to postfix using the Shunting-yard algorithm
    postfix_expr = []
    stack = []
    # Loop through each character in the expression
    for char in expression.replace(' ', ''):
        # Check if the character is an operator
        if char in operator:
            if char == '(':
                stack.append(char)
            elif char == ')':
                # Pop operators from stack until '(' is encountered
                while stack and stack[-1] != '(':
                    postfix_expr.append(stack.pop())
                stack.pop()  # Discard the '('
            else:
                # Pop operators with higher or equal precedence from the stack
                while stack and stack[-1] != '(' and operator[char] <= operator[stack[-1]]:
                    postfix_expr.append(stack.pop())
                stack.append(char)
        else:
            # Append operands directly to the postfix expression
            postfix_expr.append(char)
    # Append remaining operators from the stack to the postfix expression
    postfix_expr.extend(reversed(stack))
    return postfix_expr

def compute_expression(expression, matrices, operator):
    # Evaluate the postfix expression using matrices
    stack = []
    # Loop through each token in the expression
    for char in expression:
        if char in operator:
            # Pop two matrices from stack and perform the operation
            b = stack.pop()
            a = stack.pop()
            if char == '+':
                # Add matrices element-wise
                result = [[a[i][n] + b[i][n] for n in range(len(a[0]))] for i in range(len(a))]
            elif char == '*':
                # Matrix multiplication
                result = [[sum(a[i][k] * b[k][n] for k in range(len(a[0]))) for n in range(len(b[0]))] for i in range(len(a))]
            stack.append(result)
        else:
            # Push matrix onto the stack
            stack.append(matrices[char])
    return stack.pop()

def format_matrix(matrix):  # format matrix as a string
    return '\n'.join([' '.join(map(str, row)) for row in matrix])

with open('./input.txt', 'r') as file:  # open the input file
    lines = file.readlines()

# Read matrices and operations from input
matrix_data, operation_start_index = read_matrices(lines)
operation_list = read_operations(lines, operation_start_index)
# Define operators needed
operator = {'+': 1, '*': 2}

# Loops through each operation and compute the results
for operation in operation_list:
    # Convert infix op. to postfix
    postfix_expr = to_postfix(operation, operator)
    result_matrix = compute_expression(postfix_expr, matrix_data, operator)
    formatted_output = format_matrix(result_matrix)
    print(operation, formatted_output, end='\n\n', sep='\n')
