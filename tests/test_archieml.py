import unittest

from archieml.parser import Parser

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_keyValue(self):
        # TODO Figure out a better way to test than a string comparison.
        # Not immediately sure how to import `IDENTIFIER`, etc. from parser.py
        archieml = 'key: This is a value'
        expected = "[LexToken(IDENTIFIER,'key',1,0),LexToken(COLON,':',1,3),LexToken(TEXT,'This is a value',1,5)]"
        output = str(self.parser.tokenize(archieml))
        self.assertEqual(expected, output)

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_keyValue(self):
        archieml = 'key: This is a value'
        expected = {
            'key': 'This is a value'
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)
