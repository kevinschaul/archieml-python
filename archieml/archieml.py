#!/usr/bin/env python

import json
import os
import sys

import ply.lex as lex
import ply.yacc as yacc

import cli
import tokens
import grammar

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

    def main(self):
        """
        TODO
        """
        archieml = """
er
"""
        aml_tokens = lex.lex(module=tokens, debug=self.args.debug)
        #print(aml_tokens)
        ts = tokens.tokenize(archieml)
        for token in ts:
            print(token)
        aml_grammar = yacc.yacc(module=grammar, debug=self.args.debug)
        aml_tree = aml_grammar.parse(archieml, lexer=aml_tokens, debug=self.args.debug)
        print(json.dumps(aml_tree, indent=4))
        #result = interpreter.interpret(aml_tree)
        #print(json.dumps(result))

def launch_new_instance():
    """
    Launch an instance of the ArchieML parser.

    This is the entry function of the command-line tool `archieml`.
    """
    archieml = ArchieML()
    archieml.main()

if __name__ == '__main__':
    launch_new_instance()
