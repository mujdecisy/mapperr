from mapperr.mapr import maprit


def to_obj( src: dict, root_class) -> object:
    des = root_class()
    return maprit(src, des, root_class)
                
def to_dict( src: object ) -> dict:
    des = {}
    return maprit(src, des, src.__class__)