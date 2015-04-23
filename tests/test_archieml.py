import unittest

from archieml.parser import Parser

class TestLexer(unittest.TestCase):
    """
    Test lexing. This is an intermediate step to actually converting an
    ArchieML string to json.
    """
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
    """
    Test the full conversion from an ArchieML string to json.

    These test cases are pulled from the interactive ArchieML example page:
    http://archieml.org/
    """
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

    def test_objectBlocks(self):
        archieml = """
{colors}
red: #f00
green: #0f0
blue: #00f

{numbers}
one: 1
ten: 10
one-hundred: 100
{}

key: value
        """
        expected = {
            "colors": {
                "red": "#f00",
                "green": "#0f0",
                "blue": "#00f"
            },
            "numbers": {
                "one": "1",
                "ten": "10",
                "one-hundred": "100"
            },
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_dotNotationObjectNamespaces(self):
        archieml = """
{colors.reds}
crimson: #dc143c
darkred: #8b0000

{colors.blues}
cornflowerblue: #6495ed
darkblue: #00008b
        """
        expected = {
            "colors": {
                "reds": {
                    "crimson": "#dc143c",
                    "darkred": "#8b0000"
                },
                "blues": {
                    "cornflowerblue": "#6495ed",
                    "darkblue": "#00008b"
                }
            }
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_array(self):
        archieml = """
[scope.array]
[]
        """
        expected = {
            "scope": {
                "array": []
            }
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_newObjectUponRepeatedFirstKey(self):
        archieml = """
[arrayName]

Jeremy spoke with her on Friday, follow-up scheduled for next week
name: Amanda
age: 26

# Contact: 434-555-1234
name: Tessa
age: 30

[]
        """
        expected = {
            "arrayName": [
                {
                    "name": "Amanda",
                    "age": "26"
                }, {
                    "name": "Tessa",
                    "age": "30"
                }
            ]
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_arrayOfStrings(self):
        archieml = """
[days]
* Sunday
note: holiday!
* Monday
* Tuesday

Whitespace is still fine around the '*'
  *   Wednesday

* Thursday

Friday!
* Friday
* Saturday
[]
        """
        expected = {
            "days": [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ]
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_multiLineValues(self):
        archieml = """
key: value
 More value

Even more value
:end
        """
        expected = {
            "key": "value\n More value\n\nEven more value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_multiLineValuesWithinArraysObjects(self):
        archieml = """
[arrays.complex]
key: value
more value
:end

[arrays.simple]
* value
more value
:end
        """
        expected = {
            "arrays": {
                "complex": [
                    {
                        "key": "value\nmore value"
                    }
                ],
                "simple": [
                    "value\nmore value"
                ]
            }
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_backslashEnd(self):
        archieml = """
key: value
\:end
:end
        """
        expected = {
            "key": "value\n:end"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_withoutBackslashEnd(self):
        archieml = """
key: value
:end
:end
        """
        expected = {
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_backslashValueEnd(self):
        archieml = """
key: value
\more: value
:end
        """
        expected = {
            "key": "value\nmore: value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_withoutBackslashValueEnd(self):
        archieml = """
key: value
more: value
:end
        """
        expected = {
            "key": "value",
            "more": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_backslashArray(self):
        archieml = """
key: value
[escaping *s is not necessary if we're not inside an array, but will still be removed]
\* value
:end
        """
        expected = {
            "key": "value\n\n* value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_backslashArray(self):
        archieml = """
key: value
[escaping *s is not necessary if we're not inside an array, but will still be removed]
\* value
:end
        """
        expected = {
            "key": "value\n\n* value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_withoutBackslashArray(self):
        archieml = """
key: value
[escaping *s is not necessary if we're not inside an array, but will still be removed]
* value
:end
        """
        expected = {
            "key": "value\n\n* value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_backslashKeywords(self):
        archieml = """
key: value
\:ignore
\:skip
\:endskip
:end
        """
        expected = {
            "key": "value\n:ignore\n:skip\n:endskip"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_withoutBackslashKeywords(self):
        archieml = """
key: value
\:ignore
\:skip
\:endskip
:end
        """
        expected = {
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_inlineComment(self):
        archieml = """
title: Lorem ipsum [IGNORED] dolor sit amet
        """
        expected = {
            "title": "Lorem ipsum  dolor sit amet"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_preserveInlineComment(self):
        archieml = """
title: Lorem ipsum [[PRESERVED]] dolor sit amet
        """
        expected = {
            "title": "Lorem ipsum [PRESERVED] dolor sit amet"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_blockComment(self):
        archieml = """
:skip
  this: text
  will: be
  ignored
:endskip
        """
        expected = {}
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_ignore(self):
        archieml = """
key: value
:ignore

[array]
* Blah
[]

other-key: other value
        """
        expected = {
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

    def test_ignoreWithinSkip(self):
        archieml = """
key: value
:skip
:ignore
:endskip

[array]
* Blah
[]

other-key: other value
        """
        expected = {
            "key": "value"
        }
        output = self.parser.parse(archieml)
        self.assertEqual(expected, output)

