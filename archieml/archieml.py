#!/usr/bin/env python

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
        #self.cli = cli.CLI()
        #self.args = self.cli.parse_arguments(args)
        self.parser = parser.Parser(debug=True)

    def main(self):
        """
        TODO
        """
        archieml = 'key: This is a value'
        self.parser.tokenize(archieml)
        self.parser.parse(archieml)
        print self.parser.keys

def launch_new_instance():
    """
    Launch an instance of the ArchieML parser.

    This is the entry function of the command-line tool `archieml`.
    """
    archieml = ArchieML()
    archieml.main()

if __name__ == '__main__':
    launch_new_instance()
