import importlib

def maprit(src, des, root_class):

    rwkey = "d2o" if isinstance(src, dict) else "o2d"
    rdr = __rw[rwkey]["r"]
    wtr = __rw[rwkey]["w"]
    rcv = __rw[rwkey]["rcv"]

    annots = root_class.__dict__["__annotations__"]

    for k,t in annots.items():
        v = rdr(src, k)
        if v == None:
            wtr(des, k, None)
        else:
            if t in __prm.keys() and t == type(v):
                wtr(des, k, v)
            else:
                t = str(t)
                if t.startswith("typing.List"):
                    if type(v) != list:
                        wtr(des, k, None)
                        continue

                    it = t.replace("typing.List[","").replace("]","")
                    if it in __prm.values():
                        if it == __prm[type(v[0])]:
                            wtr(des, k, v)
                        else:
                            wtr(des, k, None)
                    else:
                        els = []
                        itcls = __simport(it)
                        for e in v:
                            els.append( rcv(e, itcls) )
                        wtr(des, k, els)
                else:
                    it = t.replace("<class '", "").replace("'>", "")
                    itcls = __simport(it)
                    wtr(des, k, rcv(v, itcls))
    return des


__rw = {
    "d2o" : {
        "r" : lambda e, k: e.get(k),
        "w" : lambda e, k, v: e.__setattr__(k, v),
        "rcv" : lambda s, c: maprit(s, c(), c)
    },
    "o2d" : {
        "r" : lambda e, k: e.__getattribute__(k),
        "w" : lambda e, k, v: e.update({k:v}),
        "rcv" : lambda s, c: maprit(s, {}, s.__class__)
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