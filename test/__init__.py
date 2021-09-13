from mapperr.mapr import _maprit


def to_obj( src: dict, root_class) -> object:
    des = root_class()
    return _maprit(src, des, root_class)
                
def to_dict( src: object ) -> dict:
    des = {}
    return _maprit(src, des, src.__class__)

def obj_to_obj( src: object, dest_class ) -> object:
    d = to_dict(src)
    return to_obj(d, dest_class)