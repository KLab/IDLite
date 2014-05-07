from __future__ import absolute_import, division, print_function
import sys

from idlite.types import List, Object, Class, Enum

if sys.version_info[0] == 3:
    basestring = str


def generate(spec, out, namespace):
    w = Writer(out)
    w.writeln(u'\ufeff')
    w.writeln("// This code is automatically generated.")
    w.writeln("// Don't edit this file directly.")
    w.writeln("using System;")
    w.writeln("using System.Collections.Generic;")
    w.writeln('')
    w.writeln('namespace %s' % namespace)
    with w:
        for n in sorted(spec.enums):
            generate_enum(w, spec.enums[n])
        for n in sorted(spec.classes):
            generate_type(w, spec.classes[n])


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
    if isinstance(t, basestring):
        if t == "float":
            return "double?" if nullable else "double"
        elif t in ["int", "long", "bool"]:
            return t + "?" if nullable else t
        elif t == Object:
            return "Dictionary<string, object>"
        else:
            return escape_reserved(t)
    elif isinstance(t, List):
        return "List<%s>" % (cstype(t.T, False))
    elif isinstance(t, Class):
        return escape_reserved(t.name)
    else:
        raise ValueError("Unknown type: " + repr(t))


def get_value(expr, type_name, nullable, enum=False):
    if type_name == Object:
        return "(Dictionary<string, object>)%s" % expr
    elif type_name in ['int', 'long', 'string', 'float', 'bool']:
        #: :type: string
        t = type_name
        if t == 'float':
            t = 'double'
        return 'Parse%s%s(%s)' % (
            'Nullable' if nullable else '',
            t.title(),
            expr)
    elif enum:
        return "(%s)ParseInt(%s)" % (type_name, expr)
    else:
        return '%snew %s((Dictionary<string, object>)%s)' % (
            ('%s == null ? null : ' % expr) if nullable else '',
            type_name,
            expr)

class FieldWrapper(object):
    def __init__(self, field):
        self.name = field.name
        self.csname = escape_reserved(field.name)
        self.type = field.type
        self.cstype = cstype(field.type, field.nullable)
        self.nullable = field.nullable
        self.enum = field.enum
        self.doc = field.doc


def generate_type(w, t):
    fields = list(map(FieldWrapper, t.fields))
    if t.doc:
        w.writeln("")
        w.writeln("/// <summary>")
        for L in t.doc.splitlines():
            w.writeln("///"+ L)
        w.writeln("/// </summary>")
    # Begin
    w.writeln("[Serializable]")
    w.writeln("public partial class " + escape_reserved(t.name) + " : IDLiteBase")
    with w:
        # Field declaration
        for f in fields:
            if f.doc is not None:
                w.writeln("/// <summary>")
                for L in f.doc.splitlines():
                    w.writeln("///" + L)
                w.writeln("/// </summary>")
            w.writeln("public {0.cstype} {0.csname};", f)
        w.writeln('')

        # Handy Constructor
        args = ", ".join("{0.cstype} {0.csname}".format(f) for f in fields)
        w.writeln("public {0}({1})", t.name, args)
        with w:
            for f in fields:
                w.writeln("this.{0.csname} = {0.csname};", f)
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
                w.writeln('this.{0.csname} = {1};', f, e)

        # ToString
        w.writeln('')
        w.writeln('public override string ToString()')
        with w:
            buf = 'return "%s(' % escape_reserved(t.name)
            buf += ', '.join('{0.csname}=" + {0.csname} + "'.format(f) for f in fields)
            buf += ')";'
            w.writeln(buf)

        # Serialize
        w.writeln('')
        w.writeln('public override Dictionary<string, object> Serialize()')
        with w:
            w.writeln('return new Dictionary<string, object>()')
            with w:
                for f in fields:
                    if isinstance(f.type, List):
                        if f.type.T in ['int', 'long', 'string', 'float', 'bool']:
                            w.writeln('{"%s", %s},' % (f.name, f.csname))
                        else:
                            w.writeln('{"%s", SerializeList(%s)},' % (f.name, f.csname))
                    elif f.enum:
                        w.writeln('{"%s", (int) %s},' % (f.name, f.csname))
                    elif f.type in ['int', 'long', 'string', 'float', 'bool', Object]:
                        w.writeln('{"%s", %s},' % (f.name, f.csname))
                    else:
                        w.writeln('{"%s", %s%s.Serialize()},' % (
                            f.name,
                            ('%s == null ? null : ' % f.csname) if f.nullable else '',
                            f.csname))
            w.writeln(';')

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
    w.writeln("public enum {0}", escape_reserved(name))
    with w:
        sep = ',\n' + '\t' * w.indent
        w.writeln(sep.join("%s = %s" % (escape_reserved(k),v) for (k,v) in values))
    w.writeln('')


def escape_reserved(w):
    if w in RESERVED_WORDS:
        return w + '_'
    return w


RESERVED_WORDS = """
abstract
as
base
bool
break
byte
case
catch
char
checked
class
const
continue
decimal
default
delegate
do
double
else
enum
event
explicit
extern
false
finally
fixed
float
for
foreach
goto
if
implicit
[in]
in
int
interface
internal
is
lock
long
namespace
new
null
object
operator
[out]
out
override
params
private
protected
public
readonly
ref
return
sbyte
sealed
short
sizeof
stackalloc
static
String
struct
switch
this
throw
true
try
typeof
uint
ulong
unchecked
unsafe
ushort
using
virtual
void
volatile
""".split()
