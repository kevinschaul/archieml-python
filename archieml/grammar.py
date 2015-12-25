import ply.yacc as yacc

from tokens import tokens

start = 'aml'

precedence = ()

def p_aml(p):
    """
    aml : element aml
    """
    p[0] = [p[1]] + p[2]

def p_aml_empty(p):
    """
    aml :
    """
    p[0] = []

def p_element_statement(p):
    """
    element : statement
    """
    p[0] = ('statement', p[1])

def p_statement_assignment(p):
    """
    statement : key COLON value
    """
    p[0] = ('assign', p[1], p[3])

def p_key(p):
    """
    key : IDENTIFIER
    """
    p[0] = ('identifier', p[1])

def p_value(p):
    """
    value : TEXT
    """
    p[0] = ('text', p[1])

def p_error(p):
    if p:
        print(p)
        print('Syntax error at \'%s\'' % p.value)
    else:
        print('Syntax error at EOF')

    # ArchieML disreguards anything that is not explicitly in its grammar
    print(dir(p))
    #p.lexer.skip(1)
    print(dir(yacc))
    print(yacc.token())
    #yacc.restart()
    #yacc.errok()
