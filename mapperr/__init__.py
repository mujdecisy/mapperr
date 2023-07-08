from mapperr.mapper import _Mapper, MappingDirection

def to_dict( src: object ) -> dict:
    mapper = _Mapper(MappingDirection.OBJECT_TO_DICT)
    des = mapper.map(src, type(src))
    return des

def to_obj( src: dict, root_class: type) -> object:
    des: object = root_class()
    required_variables = getattr(des, 'op_required', [])

    mapper = _Mapper(MappingDirection.DICT_TO_OBJECT)
    des = mapper.map(src, root_class)

    des.__setattr__('op_required', required_variables)
    __check_required(des, root_class)
    return des

def obj_to_obj( src: object, dest_class: type ) -> object:
    d = to_dict(src)
    return to_obj(d, dest_class)

def __check_required(o: object, root_class: type) -> bool:
    required_variables: list = getattr(o, 'op_required', [])
    annot_keys = root_class.__annotations__.keys()
    for e in required_variables:
        if e not in annot_keys:
            raise TypeError(f'{e} can not be required due to not being attribute of the class')
        if o.__getattribute__(e) == None:
            raise AttributeError(f'{e} is required')