import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

from .types import Class, Field, List, Enum
from ply import lex, yacc

DEBUG = 0

reserved = {
    'class': 'CLASS',
    'enum': 'ENUM',
    'List': 'LIST',
}

tokens = [
    'ID', 'NUMBER', 'COMMENT',
] + list(reserved.values())


literals = '{}:<>?=,;'

t_ignore = ' \t'

t_ignore_XCOMMENT = r'\#.*'


def t_COMMENT(t):
    r'//.*'
    t.value = t.value[2:]
    return t


def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError("Illegal character %r on %d" % (t.value[0], t.lexer.lineno))


def p_empty(p):
    "empty :"

def p_document(p):
    """
    document : COMMENT
             | COMMENT COMMENT
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + '\n' + p[2]


def p_class(p):
    """
    class : document class
          | CLASS ID '{' fields '}' ';'
    """
    if len(p) == 3:
        cls = p[2]
        p[0] = cls._replace(doc=p[1])
    else:
        p[0] = Class(p[2], None, p[4])


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
    field : document field
          | type ID ';'
          | type '?' ID ';'
          | ENUM ID ID ';'
    """
    if len(p) == 3:
        assert isinstance(p[2], Field)
        p[0] = p[2]._replace(doc=p[1])
    elif len(p) == 4:  # not nullable
        p[0] = Field(p[1], p[2], False, False, None)
    elif len(p) == 5:
        if p[2] == '?':
            p[0] = Field(p[1], p[3], True, False, None)
        else:
            p[0] = Field(p[2], p[3], False, True, None)
    else:
        raise Exception(str(p.slice))


def p_enum(p):
    """
    enum : document enum
         | ENUM ID '{' enum_values '}' ';'
    """
    if len(p) == 3:
        p[0] = p[2]._replace(doc=p[1])
    else:
        p[0] = Enum(p[2], None, p[4])


def p_enum_values(p):
    """
    enum_values : enum_values ',' enum_value
                | enum_value
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_enum_value(p):
    """
    enum_value : ID '=' NUMBER
    """
    p[0] = (p[1], p[3])  # (id, number)

def p_spec(p):
    """
    spec : spec class
         | spec enum
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
