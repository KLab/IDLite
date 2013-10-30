import sys

from idlite.parser import parser
from idlite.unitygen import generate


def main():
    files = sys.argv[1:]
    spec = []
    for fn in files:
        with open(fn) as f:
            spec += parser.parse(f.read())
            parser.restart()

    #for t in spec:
    #    print(t)

    generate(spec, '.')
