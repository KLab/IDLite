# coding: utf-8
from __future__ import absolute_import, division, print_function
from functools import partial
import sys

from .types import Class, Enum, List


# TODO: This should be somewhere else?
_PREMITIVES = ("object", "float", "double", "int", "long", "bool", "string")


class Spec(object):
    def __init__(self):
        self.classes = {}
        self.enums = {}

    def add(self, type_):
        if isinstance(type_, Class):
            self.classes[type_.name] = type_
        elif isinstance(type_, Enum):
            self.enums[type_.name] = type_
        else:
            raise TypeError("type_ should Class or Enum")

    def check_undefined(self, file=None):
        """Write undefined types to stderr."""
        if file is None:
            file = sys.stderr
        warn = partial(print, file=file)
        undefined = set()

        for cls in self.classes.values():
            for field in cls.fields:
                fieldtype = field.type
                if isinstance(fieldtype, List):
                    fieldtype = fieldtype.T
                if not isinstance(fieldtype, str):
                    continue

                if fieldtype.endswith('?'):  # skip nullable.
                    fieldtype = fieldtype[:-1]

                if field.enum:
                    if fieldtype not in self.enums:
                        if fieldtype not in undefined:
                            warn(fieldtype, "enum is not defined")
                            undefined.add(fieldtype)
                elif fieldtype not in _PREMITIVES:
                    if fieldtype not in self.classes:
                        if fieldtype not in undefined:
                            warn(fieldtype, "class is not defined")
                            undefined.add(fieldtype)

        return undefined
