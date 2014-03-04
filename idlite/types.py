from collections import namedtuple

Class = namedtuple('Class', 'name doc fields')
Field = namedtuple('Field', 'type name nullable enum')
Enum = namedtuple('Enum', 'name values')

# Generic types
List = namedtuple('List', 'T')
Object = "object"
