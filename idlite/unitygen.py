from __future__ import absolute_import, division, print_function
import sys

from idlite.types import List, Object, Class, Enum


def generate(spec, out, namespace):
    w = Writer(out)
    w.writeln("// This code is automatically generated.")
    w.writeln("// Don't edit this file directly.")
    w.writeln("using System;")
    w.writeln("using System.Collections.Generic;")
    w.writeln('')
    w.writeln('namespace %s' % namespace)
    with w:
        for def_ in spec:
            if isinstance(def_, Class):
                generate_type(w, def_)
            elif isinstance(def_, Enum):
                generate_enum(w, def_)
            else:
                raise ValueError("Can't generater for %s" % (def_,))


class Writer(object):
    newline = True
    indent = 0

    def __init__(self, out):
        self.out = out

    def _write(self, s):
        self.out.write(s)

    def _write_indent(self):
        if self.newline:
            self._write("\t" * self.indent)

    def writeln(self, s, *args, **kw):
        if args or kw:
            s = s.format(*args, **kw)
        if s:
            self._write_indent()
            self._write(s)
        self._write("\n")
        self.newline = True

    def write(self, s, *args, **kw):
        if args or kw:
            s = s.format(*args, **kw)
        self._write_indent()
        self._write(s)
        self.newline = False

    def enter(self):
        self.writeln('{')
        self.indent += 1

    def exit(self):
        self.indent -= 1
        self.writeln('}')

    def __enter__(self):
        self.enter()
        return self

    def __exit__(self, *exc):
        self.exit()


def cstype(t, nullable):
    if isinstance(t, str):
        if t == "float":
            return "double?" if nullable else "double"
        elif t in ["int", "long", "bool"]:
            return t + "?" if nullable else t
        elif t == Object:
            return "Dictionary<string, object>"
        else:
            return t
    elif isinstance(t, List):
        return "List<%s>" % (cstype(t.T, False))
    elif isinstance(t, Class):
        return t.name
    else:
        raise ValueError("Unknown type: " + repr(t))


def get_value(expr, type_name, nullable, enum=False):
    if type_name in ['int', 'long', 'string', 'float', 'bool']:
        #: :type: string
        t = type_name
        if t == 'float':
            t = 'double'
        return 'To%s%s(%s)' % (
            'Nullable' if nullable else '',
            t[0].upper() + t[1:],
            expr
        )
    elif enum:
        return "(%s)ToInt(%s)" % (type_name, expr)
    else:
        return 'new %s((Dictionary<string, object>)%s)' % (type_name, expr)

class FieldWrapper(object):
    def __init__(self, field):
        self.name = field.name
        self.type = field.type
        self.cstype = cstype(field.type, field.nullable)
        self.nullable = field.nullable
        self.enum = field.enum


def generate_type(w, t):
    fields = list(map(FieldWrapper, t.fields))
    if t.doc:
        w.writeln("/// <summary>")
        for L in t.doc.splitlines():
            w.writeln("///"+ L)
        w.writeln("/// </summary>")
    # Begin
    w.writeln("[Serializable]")
    w.writeln("public partial class " + t.name + " : IDLiteBase")
    with w:
        # Field declaration
        for f in fields:
            w.writeln("public {0.cstype} {0.name};", f)
        w.writeln('')

        # Handy Constructor
        args = ", ".join("{0.cstype} {0.name}".format(f) for f in fields)
        w.writeln("public {0}({1})", t.name, args)
        with w:
            for f in fields:
                w.writeln("this.{0.name} = {0.name};", f)
        w.writeln('')

        # From dict
        w.writeln("public {0}(Dictionary<string, object> dict)", t.name)
        with w:
            for f in fields:
                if isinstance(f.type, List):
                    e = 'GetList<%s>(dict, "%s", (object o) => { return %s; })' % (
                        cstype(f.type.T, False),
                        f.name,
                        get_value(
                            'o',
                            f.type.T,
                            False
                        )
                    )
                else:
                    e = get_value(
                        'GetItem(dict, "%s")' % f.name,
                        f.type, f.nullable, f.enum)
                w.writeln('this.{0.name} = {1};', f, e)

        #w.writeln('')
        # TODO: ToDict
    w.writeln('')


def generate_enum(w, E):
    name = E.name
    values = E.values
    doc = E.doc

    if doc:
        w.writeln("/// <summary>")
        for L in doc.splitlines():
            w.writeln("///" + L)
        w.writeln("/// </summary>")
    w.writeln("public enum {0}", name)
    with w:
        sep = ',\n' + '\t' * w.indent
        w.writeln(sep.join("%s = %s" % v for v in values))
    w.writeln('')
