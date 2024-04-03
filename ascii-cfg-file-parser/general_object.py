import queue
import base_object

class general_object(base_object.base_object):
    def __init__(self, object_name):
        super().__init__(object)
        self.child = queue.Queue()
        self.cfg_data = ""
        self.bin_data = bytearray()
        self.look_for_object_name = True
        self.look_for_object_content = False
        
    def push_cfg_data(self, cfg_data):
        self.cfg_data = cfg_data
        self.__generate_bin_data()
    
    def get_cfg_data(self):
        return self.cfg_data
    
    def show_cfg_data(self):
        print("cfg data: ", self.cfg_data)
        
    def __generate_bin_data(self):
        #to do
        return
    
    def get_bin_data(self):
        return self.bin_data
    
    def is_child_empty(self):
        return self.child.empty()
    
    def push_child(self, child_object):
        self.child.put(child_object)
    
    def get_look_for_object_name(self):
        return self.look_for_object_name
    
    def get_look_for_object_content(self, to_set):
        self.look_for_object_content = to_set
    
    def set_look_for_object_name(self, to_set):
        self.look_for_object_name = to_set
        
    def set_look_for_object_content(self, to_set):
        self.look_for_object_content = to_set
    