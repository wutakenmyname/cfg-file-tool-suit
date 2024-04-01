import os
import threading
import traceback

class Sub_cfgs(object):
    _instance = None
    def __new__(Sub_cfgs, *args, **kw):
        if Sub_cfgs._instance is None:
            Sub_cfgs._instance = object.__new__(Sub_cfgs, *args, **kw)
            Sub_cfgs._instance.lock = threading.Lock()
            Sub_cfgs._instance.type_map = {}
            print("call __init__")
            Sub_cfgs._instance.type_map.update({"BIGGEST_OBJECT_TYPE": (1, "object_parser")})
        return Sub_cfgs._instance
    #def __init__(self):
        #self.lock = threading.Lock()
        #self.type_map = {}
        #print("call __init__")
        #self.type_map.update({"BIGGEST_OBJECT_TYPE": 1})

    def register(self, type_to_register):
        for k,v in type_to_register.items():
            print("key: ", k, ", value: (", v[0], ", ", v[1], ")")
        self.lock.acquire()
        if self.type_map:
            k = list(type_to_register)[0]
            print("k: ", k)
            if k in self.type_map:
                error_msg = "key: " + "".join(type_to_register.keys()) +" has been registered\n"
                raise ValueError(error_msg)
        self.type_map.update(type_to_register)
        self.lock.release()
        
    def dump(self):
        print("##############dump start##############")
        self.lock.acquire()
        for k,v in self.type_map.items():
            print("key: ", k, ", value: (", v[0], ", ", v[1], ")")
        self.lock.release()
        print("##############dump end##############")
