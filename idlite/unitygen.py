import sys

from idlite.types import List, Object, Class, premitives


def generate(spec, outdir):
    w = Writer(sys.stdout)
    w.writeln("// This code is automatically generated.")
    w.writeln("// Don't edit this file directly.")
    w.writeln("using System;")
    w.writeln("using System.Collections.Generic;")
    w.writeln("using UnityEngine;")
    w.writeln('')
    for def_ in spec:
        generate_type(w, def_)


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


def cstype(t):
    if isinstance(t, str):
        if t == "float":
            return "double"
        elif t == Object:
            return "Dictionary<string, object>"
        else:
            return t
    elif isinstance(t, List):
        return "List<%s>" % (cstype(t.T),)
    elif isinstance(t, Class):
        return t.name
    else:
        raise ValueError("Unknown type: " + repr(t))


class FieldWrapper(object):
    def __init__(self, field):
        self.name = field.name
        self.type = field.type
        self.cstype = cstype(field.type)
        self.nullable = field.nullable


def generate_type(w, t):
    fields = list(map(FieldWrapper, t.fields))
    # Begin
    w.writeln("[Serializable]")
    w.writeln("public partial class " + t.name)
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
            w.writeln("object _o;");
            for f in fields:
                if f.type in premitives:
                    w.writeln('if (dict.TryGetValue("{0.name}", out _o))', f)
                    with w:
                        w.writeln('{0.name} = ({0.cstype})_o;', f)
                    if not f.nullable:
                        w.writeln('else')
                        with w:
                            w.writeln('Debug.Log("{0.name} not found");', f)
                elif isinstance(f.type, List):
                    w.writeln("{0.name} = new {0.cstype}();", f)
                    w.writeln('if (dict.TryGetValue("{0.name}", out _o))', f)
                    with w:
                        w.writeln('foreach (var _v in (List<object>)_o)')
                        with w:
                            if f.type.T in premitives:
                                w.writeln('{0}.Add(({1})_v);', f.name, cstype(f.type.T))
                            elif f.type.T == Object:
                                w.writeln('{0}.Add((Dictionary<string, object>)_v);', f.name)
                            else:
                                w.writeln('{0}.Add(new {1}((Dictionary<string, object>)_v));',
                                          f.name, cstype(f.type.T))
                elif f.type == Object:
                    w.writeln('dict.TryGetValue("{0.name}", out {0.name});', f)
                else:
                    print("Unknwon type: ", repr(f.type))

        #w.writeln('')
        # TODO: ToDict

    w.writeln('')
