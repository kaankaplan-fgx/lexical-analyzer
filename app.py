import re
from prettytable import PrettyTable


token_patterns = [
    ('FLOAT', r'\b-?\d+\.\d+'),  
    ('INTEGER', r'\b-?\d+\b'), 
    ('DO', r'\bdo\b'),  
    ('REPEAT', r'\brepeat\b'),
    ('WHILE', r'\bwhile\b'),
    ('FOR', r'\bfor\b'),
    ('DOUBLE', r'\bdouble\b'),
    ('BOOLEAN_LITERAL', r'\b(true|false)\b'), 
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),  
    ('LOGICAL_AND', r'&&'), 
    ('BITWISE_AND', r'&'),
    ('LOGICAL_OR', r'\|\|'),
    ('BITWISE_OR', r'\|'),
    ('POWER', r'\*\*'),
    ('ADD', r'\+'),
    ('SUBTRACT', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('ASSOP', r'=')
]

symbol_table = {}

def lex(filename):
    with open(filename, 'r') as file:
        content = file.read()

    content = content.lstrip()

    tokens = []
    while content:
        match = None
        for token_type, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(content)
            if match:
                lexeme = match.group(0)
                tokens.append((token_type, lexeme))
                content = content[match.end():].lstrip()
                if lexeme not in symbol_table:
                    symbol_table[lexeme] = token_type
                break
        if not match:
            error_lexeme = re.match(r'\S+', content)
            if error_lexeme:
                error_lexeme = error_lexeme.group(0)
                tokens.append(('ERROR', error_lexeme))
                if error_lexeme not in symbol_table:
                    symbol_table[error_lexeme] = 'ERROR'
                content = content[len(error_lexeme):].lstrip()
            else:
                break

    return tokens

def show_symbol_table(symbol_table):
    table = PrettyTable()
    table.field_names = ["Lexeme", "Token"]
    for lexeme, token in symbol_table.items():
        table.add_row([lexeme, token])
    print(table)

def main():
    filename = "input.txt"

    while True:
        print("\nMenu:")
        print("1. Call lex()")
        print("2. Show symbol table")
        print("3. Exit")
        choice = input("Choose an option: ")
        print("\n")

        if choice == '1':
            tokens = lex(filename)
            for token in tokens:
                print(f"Token: {token[0]}")
                print(f"Lexeme: {token[1]}\n")
        elif choice == '2':
            show_symbol_table(symbol_table)
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()