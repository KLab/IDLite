from __future__ import absolute_import, division, print_function
from functools import partial

from mako.template import Template
import mako.exceptions

from idlite.types import List, Class, Enum


def generate(spec, out):
    try:
        for n in sorted(spec.enums):
            out.write(_enum_t.render_unicode(enum=spec.enums[n]))
        for n in sorted(spec.classes):
            out.write(_class_t.render_unicode(class_=spec.classes[n]))
    except Exception:
        print(mako.exceptions.text_error_template().render())


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
""", imports=["from idlite.types import List"])


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
""")
