from __future__ import absolute_import, division, print_function
import argparse
import sys

from idlite.parser import parser
from idlite import unitygen, idlitegen


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--namespace', default='IDLite')
    parser.add_argument('files', nargs='+')
    return parser.parse_args()

def main():
    args = parse_args()

    spec = []
    for fn in args.files:
        with open(fn) as f:
            spec += parser.parse(f.read())
            parser.restart()

    unitygen.generate(spec, sys.stdout, args.namespace)
