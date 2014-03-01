from collections import namedtuple

Class = namedtuple('Class', 'name fields')
Field = namedtuple('Field', 'type name nullable')

# Generic types
List = namedtuple('List', 'T')
Object = "object"
