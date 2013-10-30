import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

from .types import Class, Field, List
from ply import lex, yacc

reserved = {
    'class': 'CLASS',
    'List': 'LIST',
}

tokens = [
    'ID',
] + list(reserved.values())


literals = '{}:<>'

t_ignore = ' \t'

t_ignore_COMMENT = r'\#.*'


def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError("Illegal character %r on %d" % (t.value[0], t.lexer.lineno))


def p_empty(p):
    "empty :"


def p_class(p):
    "class : CLASS ID '{' fields '}'"
    p[0] = Class(p[2], p[4])


def p_fields(p):
    """fields : fields field
              | empty
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


def p_field(p):
    """
    field : ID ID
          | LIST '<' ID '>' ID
    """
    if p[1] == 'List':
        p[0] = Field(List(p[3]), p[5])
    else:
        p[0] = Field(p[1], p[2])


def p_spec(p):
    """
    spec : spec class
         | empty
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


start = 'spec'
lexer = lex.lex()
parser = yacc.yacc(outputdir=__DIR__)
