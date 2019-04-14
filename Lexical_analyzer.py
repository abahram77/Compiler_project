import string

code_string = "void main() {}"
code_pointer = 0
# States: state_
token = []
symbols = ['{', '}', ';', ':', ',', '(', ')', '&', '*', '=', '+', '%', '^', '!', '|', '/', '>', '<', '~', '[', '[', '"',
          "'", '-', '?']
dict
symbol_permutations = {'&': ['&', '='], '=': ['='], '+': ['+', '='], '-': ['-', '='], '%': ['='], '*': ['*', '='],
                       '|': ['|', '='], '/': ['='], '>': ['>', '='], '<': ['<', '='], '~': ['='], '^': ['='],
                       '>>': ['='], '<<': ['=']}

key_words = ['auto', 'break', 'case', 'char',
             'const', 'continue', 'default', 'do',
             'double', 'else', 'enum', 'extern',
             'float', 'for', 'goto', 'if',
             'int', 'long', 'register', 'return',
             'short', 'signed', 'sizeof', 'static',
             'struct', 'switch', 'typedef', 'union',
             'unsigned', 'void', 'volatile', 'while']
letter = string.ascii_letters
digit = [str(i) for i in range(10)]
space = ['\n', '\t', ' ']
valid_token = True
token_list = []
error_list = []


def SymNumIdKeySpace():
    global new_state, code_pointer
    char = code_string[code_pointer]
    code_pointer += 1
    if char in symbols:
        new_state = ['symbol', char]
        return ''

    if char in space:
        new_state = ['end_of_token', ' ']
        return ''

    if char in digit:
        new_state = ['number', ' ']
        return char

    if char in letter:
        new_state = ['IdKey']
        return char

    valid_token = False
    code_pointer += 1


def IdKey():
    global new_state, code_pointer, valid_token
    char = code_string[code_pointer]

    if (char in space) or (char in symbols):
        new_state = ['end_of_token', ' ']
        return ''

    if (char in digit) or (char in letter):
        code_pointer += 1
        return char

    valid_token = False
    code_pointer += 1


def number():
    global new_state, code_pointer
    char = code_string[code_pointer]

    if (char in space) or (char in symbols):
        new_state = ['end_of_token', ' ']
        return ''

    if char in digit:
        code_pointer += 1
        return char

    valid_token = False
    code_pointer += 1


def symbol(pre_char):
    token = pre_char
    global code_pointer, new_state
    char = code_string[code_pointer]
    if char in symbol_permutations.get(pre_char):
        token += char
        code_pointer += 1
        if char == '>' or char == '<':
            char = code_string[code_pointer]
            if char == '=':
                token += char
                code_pointer += 1

    new_state = ['end_of_token', ' ']`
    return token


def get_next_token():
    global token_list, valid_token, error_list
    acceptable_state = [None, ' ']
    new_state = ['SymNumIdKeySpace', ' ']
    token = ''
    while code_pointer < len(code_string):
        while new_state[0]!= 'end_of_token' and code_pointer < len(code_string):
            acceptable_state = new_state
            # print(acceptable_state[0] + '(' + acceptable_state[1] + ')')
            token += eval(acceptable_state[0] + '(' + acceptable_state[1] + ')')

        if valid_token:
            if acceptable_state[0] == 'IdKey':
                acceptable_state[0] = 'ID'
                if token in key_words:
                    acceptable_state[0] = 'keyword'
            token_list += [(token, acceptable_state[0])]

        else:
            error_list += [(token, 'invalid input')]

        token = ''
        valid_token = True
        acceptable_state = [None, None]
        new_state = ['SymNumIdKeySpace', ' ']

get_next_token()
print(token_list, error_list)