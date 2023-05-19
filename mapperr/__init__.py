from mapperr.mapr import _maprit

def to_obj( src: dict, root_class: type) -> object:
    des: object = root_class()
    required_variables = getattr(des, 'op_required', [])

    res = _maprit(src, des, root_class)

    res.__setattr__('op_required', required_variables)
    __check_required(res, root_class)
    return res

def to_dict( src: object ) -> dict:
    des = {}
    return _maprit(src, des, src.__class__)

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