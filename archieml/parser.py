import ply.lex as lex
import ply.yacc as yacc

class Parser(object):
    """
    TODO
    """
    tokens = (
        'SPACE',
        'COLON',
        'ASTERISK',
        'PERIOD',
        'BACKSLASH',
        'OPEN_CBRACKET',
        'CLOSE_CBRACKET',
        'OPEN_SBRACKET',
        'CLOSE_SBRACKET',
        'CLOSE_MULTILINE',
        'OPEN_SKIP',
        'CLOSE_SKIP',
        'OPEN_IGNORE',
        'IDENTIFIER',
        'TEXT',
    )
    precedence = ()

    t_SPACE = r'\ '
    t_COLON = r':'
    t_ASTERISK = r'\*'
    t_PERIOD = r'\.'
    t_BACKSLASH = r'\\'
    t_OPEN_CBRACKET = r'{'
    t_CLOSE_CBRACKET = r'}'
    t_OPEN_SBRACKET = r'\['
    t_CLOSE_SBRACKET = r'\]'
    t_CLOSE_MULTILINE = r':end'
    t_OPEN_SKIP = r':skip'
    t_CLOSE_SKIP = r':endskip'
    t_OPEN_IGNORE = r':ignore'

    t_ignore = '\t'

    def __init__(self, debug=False):
        self.keys = {}

        lex.lex(module=self, debug=debug)
        yacc.yacc(module=self, debug=debug)

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z0-9-_]+'
        return t

    def t_TEXT(self, t):
        # TODO Why do we have to ignore tokens that are already defined?
        r'[^:\*\.\\{}\[\]]+$'
        return t

    def t_error(self, t):
        print(t)
        print('Illegal character \'%s\'' % t.value[0])
        t.lexer.skip(1)

    def p_statement_assign(self, p):
        """
        statement : IDENTIFIER COLON TEXT
                  | IDENTIFIER COLON IDENTIFIER
        """
        self.keys[p[1]] = p[3]

    def p_error(self, p):
        if p:
            print(p)
            print('Syntax error at \'%s\'' % p.value)
        else:
            print('Syntax error at EOF')

    def tokenize(self, s):
        tokens = []
        lex.input(s)
        while True:
             token = lex.token()
             if not token:
                 break
             tokens.append(token)
        return tokens

    def parse(self, s):
        yacc.parse(s)
