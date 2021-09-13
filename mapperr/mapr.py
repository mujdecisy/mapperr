import importlib
import warnings

def _maprit(src, des, root_class):
    rwkey = "d2o" if isinstance(src, dict) else "o2d"
    rdr = __rw[rwkey]["r"]
    wtr = __rw[rwkey]["w"]
    rcv = __rw[rwkey]["rcv"]

    annots = root_class.__dict__["__annotations__"]

    for k,t in annots.items():
        v = rdr(src, k)
        tstr = str(t)

        if v != None and not __is_matching_types(t, type(v)):
            warnings.warn(f"{k} not in type [{t}], it is [{type(v)}], it is replaced as None")
            wtr(des, k, None)
            continue

        if (__is_defined_list(tstr) and __get_list_inner_type(tstr) in __prm.values()) or (v == None or t in __prm.keys()):
            wtr(des, k, v)
            continue

        if __is_defined_list(tstr):
            els = []
            itcls = __simport(__get_list_inner_type(tstr))
            for e in v:
                els.append( rcv(e, itcls) )
            wtr(des, k, els)
            continue

        itcls = __simport(__clean_type_str(tstr))
        wtr(des, k, rcv(v, itcls))
    return des

def __is_defined_list(type_str: str) -> bool:
    return type_str.startswith("typing.List")

def __get_list_inner_type(type_str: str) -> str:
    return type_str.replace("typing.List[","").replace("]","")

def __clean_type_str(type_str: str) -> str:
    return type_str.replace("<class '", "").replace("'>", "")

def __is_matching_types(t1, t2) -> bool:
    t1 = __type_check(t1)
    t2 = __type_check(t2)
    if t1 == t2:
        return True
    return False

def __type_check(t: type) -> type:
    if __is_defined_list(str(t)):
        return list
    if __clean_type_str(str(t)) not in __prm.values():
        return dict
    return t

__rw = {
    "d2o" : {
        "r" : lambda e, k: e.get(k),
        "w" : lambda e, k, v: e.__setattr__(k, v),
        "rcv" : lambda s, c: _maprit(s, c(), c)
    },
    "o2d" : {
        "r" : lambda e, k: e.__getattribute__(k),
        "w" : lambda e, k, v: e.update({k:v}),
        "rcv" : lambda s, c: _maprit(s, {}, s.__class__)
    }
}

__prm = {
    str: "str",
    int: "int",
    float: "float",
    dict: "dict",
    list: "list"
}

def __simport(module_and_class: str):
    cstr = module_and_class.split(".")[-1]
    mstr = module_and_class.replace(f".{cstr}", "")
    m = importlib.import_module(mstr)
    c = getattr(m, cstr)
    return c