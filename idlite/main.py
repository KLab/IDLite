from __future__ import absolute_import, division, print_function
import sys

from idlite.parser import parser
from idlite import unitygen, idlitegen


def main():
    files = sys.argv[1:]
    spec = []
    for fn in files:
        with open(fn) as f:
            spec += parser.parse(f.read())
            parser.restart()

    #for t in spec:
    #    print(t)

    unitygen.generate(spec, sys.stdout)
