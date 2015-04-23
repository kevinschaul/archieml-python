#!/usr/bin/env python

import os
import sys

import cli

import lexer
import parser

class ArchieML(object):
    """
    An ArchieML parser
    """

    def __init__(self, args=None):
        """
        Get the options from cli.
        """
        #self.cli = cli.CLI()
        #self.args = self.cli.parse_arguments(args)
        self.lexer = lexer.Lexer()
        #self.parser = parser.Parser()

    def main(self):
        """
        TODO
        """
        tokens = self.lexer.tokenize('{headline}: * this :ignore is a headline')
        #self.parser.parse(tokens)

def launch_new_instance():
    """
    Launch an instance of the ArchieML parser.

    This is the entry function of the command-line tool `archieml`.
    """
    archieml = ArchieML()
    archieml.main()

if __name__ == '__main__':
    launch_new_instance()
