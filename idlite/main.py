from __future__ import absolute_import, division, print_function
import argparse
from functools import partial
import sys

from idlite.parser import parser
from idlite import unitygen, idlitegen, types


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--namespace', default='IDLite')
    parser.add_argument('--output-type', default='unity')
    parser.add_argument('files', nargs='+')
    return parser


def check_undefined(spec):
    premitives = ("object", "float", "double", "int", "long", "bool", "string")
    warn = partial(print, file=sys.stderr)
    classes = {}
    enums = {}
    for typedef in spec:
        if isinstance(typedef, types.Enum):
            enums[typedef.name] = typedef
        else:
            assert isinstance(typedef, types.Class)
            classes[typedef.name] = typedef

    for cls in classes.values():
        for field in cls.fields:
            fieldtype = field.type
            if isinstance(fieldtype, types.List):
                fieldtype = fieldtype.T

            if isinstance(fieldtype, str):
                if fieldtype.endswith('?'):
                    fieldtype = fieldtype[:-1]

                if field.enum:
                    if fieldtype not in enums:
                        warn(fieldtype, "enum is not defined")
                        enums[fieldtype] = None  # Don't warn twice.
                elif fieldtype not in premitives:
                    if fieldtype not in classes:
                        warn(fieldtype, "class is not defined")
                        classes[fieldtype] = None



def main():
    argparser = build_argparser()
    args = argparser.parse_args()

    spec = []
    for fn in args.files:
        with open(fn) as f:
            spec += parser.parse(f.read())
            parser.restart()

    type_order = {types.Enum: 0, types.Class: 1}
    spec.sort(key=lambda s: (type_order[type(s)], s.name))

    check_undefined(spec)

    if args.output_type == 'unity':
        unitygen.generate(spec, sys.stdout, args.namespace)
    elif args.output_type == 'idlite':
        idlitegen.generate(spec, sys.stdout)
    else:
        sys.exit("""
Unknown output type: %r
Available types are: unity, idlite""" % args.output_type)
