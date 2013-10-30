from collections import namedtuple

Class = namedtuple('Class', 'name fields')
Field = namedtuple('Field', 'type name')

# Generic types
List = namedtuple('List', 'T')
Object = "Object"

# Premitive types
premitives = [
    "bool",
    "string",
    "float",
    "int"]
