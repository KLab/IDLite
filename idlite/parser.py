import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

from .types import Class, Field, List
from ply import lex, yacc

DEBUG = 0

reserved = {
    'class': 'CLASS',
    'List': 'LIST',
}

tokens = [
    'ID',
] + list(reserved.values())


literals = '{}:<>?'

t_ignore = ' \t'

t_ignore_COMMENT = r'\#.*'


def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
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


def p_type(p):
    """
    type : ID
         | LIST '<' ID '>'
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Recursive type is not supported for now.
        assert len(p) == 5
        p[0] = List(p[3])


def p_field(p):
    """
    field : type ID
          | type '?' ID
    """
    if len(p) == 3:  # not nullable
        p[0] = Field(p[1], p[2], False)
    else:
        assert len(p) == 4  # nullable
        p[0] = Field(p[1], p[3], True)


def p_spec(p):
    """
    spec : spec class
         | empty
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]


def p_error(p):
    raise Exception(str(p))


start = 'spec'
lexer = lex.lex(debug=DEBUG)
parser = yacc.yacc(outputdir=__DIR__, debug=DEBUG, write_tables=False)
