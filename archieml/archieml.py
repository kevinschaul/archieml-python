#!/usr/bin/env python

import json
import os
import sys

import cli

import parser

class ArchieML(object):
    """
    An ArchieML parser
    """

    def __init__(self, args=None):
        """
        Get the options from cli.
        """
        self.cli = cli.CLI()
        self.args = self.cli.parse_arguments(args)
        self.parser = parser.Parser(debug=self.args.debug)

    def main(self):
        """
        TODO
        """
        archieml = """1: value
2:value
3   : value
 4:    value
5:	value	

a: lowercase a
A: uppercase A

        """
        tokens = self.parser.tokenize(archieml)
        print tokens
        parsed = self.parser.parse(archieml)
        print(json.dumps(parsed))

def launch_new_instance():
    """
    Launch an instance of the ArchieML parser.

    This is the entry function of the command-line tool `archieml`.
    """
    archieml = ArchieML()
    archieml.main()

if __name__ == '__main__':
    launch_new_instance()
