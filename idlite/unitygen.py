import os

from idlite.types import List, Object, Class, premitives


def generate(spec, outdir):
    with open(os.path.join(outdir, "types.cs"), "w") as f:
        w = Writer(f)
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
        else:
            return t
    elif isinstance(t, List):
        return "List<%s>" % (cstype(t.T),)
    elif isinstance(t, Object):
        return "Dictionary<string, %s>" % (cstype(t.type))
    elif isinstance(t, Class):
        return t.name
    else:
        raise ValueError("Unknown type: " + repr(t))


class FieldWrapper(object):
    def __init__(self, field):
        self.name = field.name
        self.type = field.type
        self.cstype = cstype(field.type)


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

        # Constructor
        args = ", ".join("{0.cstype} {0.name}".format(f) for f in fields)
        w.writeln("public {0}({1})", t.name, args)
        with w:
            for f in fields:
                w.writeln("this.{0.name} = {0.name};", f)
        w.writeln('')

        # FromDict
        w.writeln("public static {0} FromDict(Dictionary<string, object> dict)", t.name)
        with w:
            for f in fields:
                if f.type in premitives:
                    w.writeln('var {0.name} = dict.GetValue<{0.cstype}>("{0.name}");', f)
                elif isinstance(f.type, List):
                    w.writeln("var {0.name} = new {0.cstype}();", f)
                    w.writeln('foreach (var o in dict.GetValue<List<object>>("{0}"))', f.name)
                    with w:
                        if f.type.T in premitives:
                            w.writeln('{0}.Add(({1}o));', f.name, cstype(f.type.T))
                        else:
                            w.writeln('{0}.Add({1}.FromDict((Dictionary<string, object>)o));',
                                      f.name, cstype(f.type.T))
                elif f.type == Object:
                    w.writeln('var {0} = dict.GetValue<Dictionary<string, object>>("{0}");',
                              f.name)
                else:
                    print("Unknwon type: ", repr(f.type))

            w.writeln("return new {0}({1});",
                      t.name, ', '.join(f.name for f in fields))

        #w.writeln('')
        # TODO: ToDict

    w.writeln('')
