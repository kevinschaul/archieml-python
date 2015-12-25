import ply.lex as lex

tokens = (
    'COLON',
    'ASTERISK',
    'PERIOD',
    'BACKSLASH',
    'OPEN_CBRACKET',
    'CLOSE_CBRACKET',
    'OPEN_SBRACKET',
    'CLOSE_SBRACKET',
    'OPEN_SKIP',
    'CLOSE_SKIP',
    'OPEN_IGNORE',
    'IDENTIFIER',
    'TEXT'
)

states = (
    ('value', 'exclusive'),
)

def t_value_TEXT(t):
    r'.+'
    t.lexer.begin('INITIAL')
    t.value = t.value.strip()
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z0-9-_]+'
    return t

def t_COLON(t):
    r':'
    t.lexer.begin('value')
    return t

def t_ASTERISK(t):
    r'\*'
    t.lexer.begin('value')
    return t

t_PERIOD = r'\.'
t_OPEN_CBRACKET = r'\{'
t_CLOSE_CBRACKET = r'\}'
t_OPEN_SBRACKET = r'\['
t_CLOSE_SBRACKET = r'\]'
t_BACKSLASH = r'\\'
t_OPEN_SKIP = r':skip'
t_CLOSE_SKIP = r':endskip'
t_OPEN_IGNORE = r':ignore'

t_ignore = ' \t'
t_value_ignore = ''

def t_newline(t):
    r'\n'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += 1

def t_error(t):
    print('Illegal character \'%s\'' % t.value[0])
    t.lexer.skip(1)
    t.lexer.begin('INITIAL')

def t_value_error(t):
    print('Illegal character \'%s\'' % t.value[0])
    t.lexer.skip(1)
    t.lexer.begin('INITIAL')

def tokenize(s):
    tokens = []
    lex.input(s)
    while True:
        token = lex.token()
        if not token:
            break
        tokens.append(token)
    return tokens
