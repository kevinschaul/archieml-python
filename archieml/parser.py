import ply.yacc as yacc

class Parser(object):
    """
    Parser for ArchieML
    """

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True)

    def p_key_expression(self, p):
        """
        key : TEXT
        """
        p[0] = p[1]

    def parse(self, tokens):
        self.parser.parse(tokens)
