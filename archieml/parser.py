import ply.yacc as yacc

from lexer import tokens

class Parser(object):
    """
    Parser for ArchieML
    """

    keys = {}

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=True)

    def parse(self, tokens):
        self.parser.parse(tokens)
