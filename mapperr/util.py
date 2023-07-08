from enum import Enum

class MappingDirection(Enum):
    DICT_TO_OBJECT = 0
    OBJECT_TO_DICT = 1

class SourceIsNoneError(Exception):
    pass

class SourceIsPrimitiveError(Exception):
    pass

NOT_ALLOWED_BUILTINS = ["list", "dict", "set"]