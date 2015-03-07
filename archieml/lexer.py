import ply.lex as lex

class Lexer(object):
    """
    Lexicon analyzer for ArchieML
    """
    tokens = (
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
        'KEYTEXT',
        'TEXT',
    )

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

    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_KEYTEXT(self, t):
        r'[a-zA-Z0-9-_]+'
        return t

    def t_TEXT(self, t):
        # TODO Why do we have to escape tokens that are already defined?
        r'[^:\*\.\\{}\[\]]+'
        return t

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def tokenize(self, data):
        self.lexer.input(data)
        while True:
            token = self.lexer.token()
            if not token:
                break
            print token
