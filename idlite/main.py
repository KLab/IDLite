from __future__ import absolute_import, division, print_function
import argparse
import io
import sys

from idlite.parser import parser
from idlite.spec import Spec
from idlite import unitygen, idlitegen, types


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--namespace', default='IDLite')
    parser.add_argument('--output-type', default='unity')
    parser.add_argument('files', nargs='+')
    return parser


def main():
    argparser = build_argparser()
    args = argparser.parse_args()

    spec = Spec()
    for fn in args.files:
        with io.open(fn, 'r') as f:
            for t in parser.parse(f.read()):
                spec.add(t)
            parser.restart()

    spec.check_undefined()

    if args.output_type == 'unity':
        unitygen.generate(spec, sys.stdout, args.namespace)
    elif args.output_type == 'idlite':
        idlitegen.generate(spec, sys.stdout)
    else:
        sys.exit("""
Unknown output type: %r
Available types are: unity, idlite""" % args.output_type)
