import unittest

from archieml.parser import Parser

class TestLexer(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_keyValue(self):
        # TODO Figure out a better way to test than a string comparison.
        # Not immediately sure how to import `IDENTIFIER`, etc. from parser.py
        archieml = 'key: This is a value'
        expected = "[LexToken(IDENTIFIER,'key',1,0), LexToken(COLON,':',1,3), LexToken(TEXT,'This is a value',1,5)]"
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

    def test_surroundingWhitespace(self):
        archieml = """
        1: value
2:value
3   : value
 4:    value
5:	value	

a: lowercase a
A: uppercase A
        """
        expected = {
            "1": "value",
            "2": "value",
            "3": "value",
            "4": "value",
            "5": "value",
            "a": "lowercase a",
            "A": "uppercase A"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_ignoreNonKeys(self):
        archieml = """
This is a key:

  key: value

It's a nice key!
        """
        expected = {
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_dotNotation(self):
        archieml = """
colors.red: #f00
colors.green: #0f0
colors.blue: #00f
        """
        expected = {
            "colors": {
                "red": "#f00",
                "green": "#0f0",
                "blue": "#00f"
            }
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

