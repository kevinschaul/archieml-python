import ply.lex as lex
import ply.yacc as yacc

class Parser(object):
    """
    TODO
    """
    states = (
        ('value', 'inclusive'),
    )

    tokens = (
        'NEWLINE',
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

    t_COLON = r':'
    t_ASTERISK = r'\*'
    t_BACKSLASH = r'\\'
    t_OPEN_SBRACKET = r'\['
    t_CLOSE_SBRACKET = r'\]'
    t_CLOSE_MULTILINE = r':end'
    t_OPEN_SKIP = r':skip'
    t_CLOSE_SKIP = r':endskip'
    t_OPEN_IGNORE = r':ignore'

    t_ignore = ' \t'

    def __init__(self, debug=False):
        self.debug = debug

        # Top-level key storage
        self.keys = {}

        # Store the current object (if any) here, e.g. when entering a block
        # defined by {key}.
        self.current_object = False

        lex.lex(module=self, debug=debug)
        yacc.yacc(module=self, debug=debug)

    def t_NEWLINE(self, t):
        r'[\n]+'
        pass

    def t_OPEN_CBRACKET(self, t):
        r'\{'
        return t

    def t_CLOSE_CBRACKET(self, t):
        r'\}'
        t.lexer.begin('INITIAL')
        return t

    def t_IDENTIFIER(self, t):
        r'([a-zA-Z0-9-_]+)'
        t.lexer.begin('value')
        # Strip whitespace surrounding IDENTIFIER
        t.value = t.value.strip()
        return t

    def t_PERIOD(self, t):
        r'\.'
        t.lexer.begin('INITIAL')
        return t

    def t_value_TEXT(self, t):
        # TODO Why do we have to ignore tokens that are already defined?
        r'[^:\*\.\\{}\[\]\n]+'
        t.lexer.begin('INITIAL')
        # Strip whitespace surrounding TEXT
        t.value = t.value.strip()
        return t

    def t_error(self, t):
        if self.debug:
            print(t)
            print('Illegal character \'%s\'' % t.value[0])
        t.lexer.skip(1)

    def p_document(self, p):
        """
        document : statement
        """
        pass

    def p_statement_multiple(self, p):
        """
        statement : statement statement
        """
        pass

    def p_statement_assign(self, p):
        """
        statement : key COLON TEXT
        """
        # `key` is a tuple containing the nested structure of the key.
        # e.g.
        # colors.red -> ('colors', 'red',)

        # Set `root` to the extent of the current object (or to the top-level
        # store `self.keys` if there isn't one).
        #
        # e.g.
        # If `current_object` == ('colors', 'reds'), then set `root` to
        # `self.keys.colors.reds`.
        root = self.keys
        if self.current_object:
            for i, key in enumerate(self.current_object):
                root = root.get(key, {})

        # Follow the current key down its structure, and assign its value to
        # `root`.
        num_keys = len(p[1])
        stored = root
        # If this key is not a dict, reassign it. This happens when redefining
        # a value as a new object.
        if not isinstance(stored, dict):
            stored = {}
        for i, key in enumerate(p[1]):
            if i == num_keys - 1:
                stored[key] = p[3]
            else:
                stored[key] = stored.get(key, {})
                stored = stored[key]

        # Unwind the object if it exists, setting the value to `self.keys`
        if (self.current_object):
            num_keys = len(self.current_object)
            stored = self.keys
            for i, key in enumerate(self.current_object):
                if i == num_keys - 1:
                    stored[key] = root
                else:
                    stored[key] = stored.get(key, {})
                    stored = stored[key]

    def p_statement_object(self, p):
        """
        statement : object
        """
        pass

    def p_key_multiple(self, p):
        """
        key : key PERIOD key
        """
        p[0] = p[1] + p[3]

    def p_key(self, p):
        """
        key : IDENTIFIER
        """
        p[0] = (p[1],)

    def p_object_begin(self, p):
        """
        object : OPEN_CBRACKET key CLOSE_CBRACKET
        """
        self.current_object = p[2]

    def p_object_end(self, p):
        """
        object : OPEN_CBRACKET CLOSE_CBRACKET
        """
        self.current_object = False

    def p_error(self, p):
        if self.debug:
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
        return self.keys
