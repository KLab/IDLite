from collections import namedtuple

Class = namedtuple('Class', 'name doc fields')
Field = namedtuple('Field', 'type name nullable enum doc')
Enum = namedtuple('Enum', 'name doc values')

# Generic types
List = namedtuple('List', 'T')
Object = "object"
