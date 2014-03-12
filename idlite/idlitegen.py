from __future__ import absolute_import, division, print_function, unicode_literals
from functools import partial

from mako.template import Template

from idlite.types import List, Class, Enum


def generate(spec, out):
    for t in spec:
        if isinstance(t, Class):
            out.write(_class_t.render(class_=t))
        elif isinstance(t, Enum):
            out.write(_enum_t.render(enum=t))


_class_t = Template(
"""
% if class_.doc:
    % for L in class_.doc.splitlines():
//${L}
    % endfor
% endif
class ${class_.name} {
% for field in class_.fields:
    % if field.doc is not None:
        % for L in field.doc.splitlines():
    //${L}
        % endfor
    % endif
    % if field.enum:
    enum ${field.type} ${field.name};
    % elif isinstance(field.type, List):
    List<${field.type.T}> ${field.name};
    % else:
    ${field.type}${'?' if field.nullable else ''} ${field.name};
    % endif
% endfor
};
""", format_exceptions=True, imports=["from idlite.types import List"])


_enum_t = Template(
"""
% if enum.doc:
    % for L in enum.doc.splitlines():
//${L}
    % endfor
% endif
enum ${enum.name} {
% for (name, value) in enum.values:
    ${name} = ${value}${'' if loop.last else ','}
% endfor
};
""", format_exceptions=True)
