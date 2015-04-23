import unittest

from archieml.lexer import Lexer

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def test_keyValue(self):
        # TODO Figure out a better way to test than a string comparison.
        # Not immediately sure how to import `IDENTIFIER`, etc. from lexer.py
        archieml = 'key: This is a value'
        expected = "[LexToken(IDENTIFIER,'key',1,0),LexToken(COLON,':',1,3),LexToken(TEXT,'This is a value',1,5)]"
        output = str(self.lexer.tokenize(archieml))
        self.assertEqual(expected, output)
