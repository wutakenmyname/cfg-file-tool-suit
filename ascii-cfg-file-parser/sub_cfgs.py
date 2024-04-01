import os

class Sub_cfgs(object):
    _instance = None
    def __new__(Sub_cfgs, *args, **kw):
        if Sub_cfgs._instance is None:
            Sub_cfgs._instance = object.__new__(Sub_cfgs, *args, **kw)
        return Sub_cfgs._instance
    def __init__(self):
        self.type_map.updte({"BIGGEST_OBJECT_TYPE": ("BIGGESST_OBJECT_TYPE", 1, 1)})

    def register(self, type_to_register):
        self.type_map.update(type_to_register)
