import sys
import re

# Global variables
tokens = []
current_token_index = 0
error_flag = False

# Token types
LET = "let"
IN = "in"
END = "end"
INT = "int"
REAL = "real"
IF = "if"
THEN = "then"
ELSE = "else"
ID = "id"
NUMBER = "number"
ASSIGN = "="
SEMI = ";"
PLUS = "+"
MINUS = "-"
MULTIPLY = "*"
DIVIDE = "/"
LEFT_PAREN = "("
RIGHT_PAREN = ")"
LEFT_BRACE = "{"
RIGHT_BRACE = "}"
PIPE = "|"
LESS = "<"
LESSEQ = "<="
GREATER = ">"
GREATEREQ = ">="
EQUAL = "=="
NOTEQUAL = "<>"
COLON = ":"

# Store variable values
variables = {}

# Token regex patterns
token_patterns = {
    LET: r'\blet\b',
    IN: r'\bin\b',
    END: r'\bend\b',
    INT: r'\bint\b',
    REAL: r'\breal\b',
    IF: r'\bif\b',
    THEN: r'\bthen\b',
    ELSE: r'\belse\b',
    NUMBER: r'\b\d+(\.\d+)?\b',
    ID: r'\b[a-zA-Z_]\w*\b',
    ASSIGN: r'=',
    SEMI: r';',
    PLUS: r'\+',
    MINUS: r'-',
    MULTIPLY: r'\*',
    DIVIDE: r'/',
    LEFT_PAREN: r'\(',
    RIGHT_PAREN: r'\)',
    LEFT_BRACE: r'\{',
    RIGHT_BRACE: r'\}',
    PIPE: r'\|',
    LESS: r'<',
    LESSEQ: r'<=',
    GREATER: r'>',
    GREATEREQ: r'>=',
    EQUAL: r'==',
    NOTEQUAL: r'<>',
    COLON: r':'
}

def get_token():
    global current_token_index
    if current_token_index < len(tokens):
        current_token_index += 1
        return tokens[current_token_index - 1]
    else:
        return None

def peek_token():
    global current_token_index
    if current_token_index < len(tokens):
        return tokens[current_token_index]
    else:
        return None

def match(expected_token):
    global error_flag
    if peek_token()[0] == expected_token:
        get_token()
    else:
        print(f"Error: expected {expected_token}, but found {peek_token()[0]}")
        error_flag = True

def parse_program():
    while peek_token() and peek_token()[0] == LET:
        parse_let_in_end()
    if not error_flag:
        print("Program successfully parsed.")

def parse_let_in_end():
    match(LET)
    parse_decl_list()
    match(IN)
    result = parse_type_and_expr()
    match(END)
    match(SEMI)
    
    if not error_flag:
        print(result)  # Print the result of the expression

def parse_decl_list():
    while peek_token()[0] == ID:
        parse_decl()

def parse_decl():
    var_name = get_token()[1]  # Get the variable name (second element is the actual value)
    match(COLON)
    var_type = parse_type()
    match(ASSIGN)
    var_value = parse_expr()  # Get the value of the expression
    match(SEMI)
    
    # Store the variable in the variables dictionary
    if var_type == INT:
        variables[var_name] = int(var_value)
    elif var_type == REAL:
        variables[var_name] = float(var_value)

def parse_type():
    if peek_token()[0] == INT:
        match(INT)
        return INT
    elif peek_token()[0] == REAL:
        match(REAL)
        return REAL
    else:
        print(f"Error: expected type 'int' or 'real', but found {peek_token()[0]}")
        error_flag = True

def parse_type_and_expr():
    type_token = parse_type()
    match(LEFT_PAREN)
    result = parse_expr()
    match(RIGHT_PAREN)
    
    if type_token == INT:
        return int(result)
    elif type_token == REAL:
        return float(result)

def parse_expr():
    if peek_token()[0] == IF:
        return parse_conditional_expr()
    else:
        return parse_term_arithmetic()

def parse_term_arithmetic():
    result = parse_term()
    while peek_token()[0] == PLUS or peek_token()[0] == MINUS:
        operator = get_token()[0]
        next_term = parse_term()
        if operator == PLUS:
            result += next_term
        elif operator == MINUS:
            result -= next_term
    return result

def parse_term():
    result = parse_factor()
    while peek_token()[0] == MULTIPLY or peek_token()[0] == DIVIDE:
        operator = get_token()[0]
        next_factor = parse_factor()
        if operator == MULTIPLY:
            result *= next_factor
        elif operator == DIVIDE:
            result /= next_factor
    return result

def parse_factor():
    token_type, token_value = peek_token()
    if token_type == LEFT_PAREN:
        match(LEFT_PAREN)
        result = parse_expr()
        match(RIGHT_PAREN)
        return result
    elif token_type == ID:
        var_name = get_token()[1]
        if var_name in variables:
            return variables[var_name]
        else:
            print(f"Error: variable '{var_name}' not defined.")
            error_flag = True
            return 0
    elif token_type == NUMBER:
        get_token()  # Consume the number token
        return float(token_value) if '.' in token_value else int(token_value)
    elif token_type == REAL:
        match(REAL)
        match(LEFT_PAREN)
        result = parse_expr()
        match(RIGHT_PAREN)
        return float(result)  # Apply the real type conversion
    else:
        print(f"Error: invalid factor '{token_value}'")
        error_flag = True
        return 0

def parse_conditional_expr():
    match(IF)
    condition = parse_cond()  # Evaluate the condition
    match(THEN)
    if_true = parse_expr()  # Evaluate the "then" expression
    match(ELSE)
    if_false = parse_expr()  # Evaluate the "else" expression

    # Return the appropriate value based on the condition
    return if_true if condition else if_false

def parse_cond():
    left_operand = parse_operand()
    operator = peek_token()[0]
    if operator in [LESS, LESSEQ, GREATER, GREATEREQ, EQUAL, NOTEQUAL]:
        get_token()  # Consume the operator
        right_operand = parse_operand()

        # Evaluate the condition based on the operator
        if operator == LESS:
            return left_operand < right_operand
        elif operator == LESSEQ:
            return left_operand <= right_operand
        elif operator == GREATER:
            return left_operand > right_operand
        elif operator == GREATEREQ:
            return left_operand >= right_operand
        elif operator == EQUAL:
            return left_operand == right_operand
        elif operator == NOTEQUAL:
            return left_operand != right_operand
    else:
        print(f"Error: expected a comparison operator, but found '{operator}'")
        error_flag = True
        return False

def parse_operand():
    token_type, token_value = peek_token()
    if token_type == ID:
        return variables[get_token()[1]]  # Get the value of the variable
    elif token_type == NUMBER:
        return float(get_token()[1]) if '.' in token_value else int(get_token()[1])
    else:
        print(f"Error: invalid operand '{token_value}'")
        error_flag = True
        return 0

def tokenize(input_string):
    token_list = []
    i = 0
    while i < len(input_string):
        match_found = False
        for token_type, pattern in token_patterns.items():
            regex = re.compile(pattern)
            match = regex.match(input_string, i)
            if match:
                match_found = True
                token_value = match.group()
                token_list.append((token_type, token_value))  # Store both type and value
                i = match.end()
                break
        if not match_found:
            if input_string[i].isspace():
                i += 1
            else:
                print(f"Unknown character: {input_string[i]}")
                i += 1
    return token_list

def main():
    global tokens
    if len(sys.argv) != 2:
        print("Usage: python3 parser_2887869.py <inputfile>")
        return

    input_filename = sys.argv[1]
    try:
        with open(input_filename, 'r') as file:
            input_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return

    tokens = tokenize(input_data)
    parse_program()

if __name__ == "__main__":
    main()