from __future__ import absolute_import, division, print_function, unicode_literals
from functools import partial

from idlite.types import List, Class, Enum


def generate(spec, out):
    for t in spec:
        if isinstance(t, Class):
            generate_class(t, out)
        elif isinstance(t, Enum):
            generate_enum(t, out)


def generate_class(t, out):
    p = partial(print, file=out)
    doc = t.doc

    if doc:
        for L in doc.splitlines():
            p("//" + L)
    p("class %s {" % t.name)
    for f in t.fields:
        if f.enum:
            p("    enum %s %s;" % (f.type, f.name))
        elif isinstance(f.type, List):
            p("    List<%s> %s;" % (f.type.T, f.name))
        else:
            p("    %s %s;" % (f.type, f.name))
    p("};\n")


def generate_enum(t, out):
    p = partial(print, file=out)
    doc = t.doc

    if doc:
        for L in doc.splitlines():
            p("//" + L)

    p("enum %s {" % t.name)
    L = ',\n    '.join("%s = %s" % t for t in t.values)
    p("    " + L)
    p("};\n")
