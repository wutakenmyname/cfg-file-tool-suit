import queue
import base_object

class general_object(base_object.base_object):
    def __init__(self, object_name):
        super().__init__(object_name)
        self.child = queue.Queue()
        self.cfg_data = ""
        #self.bin_data = bytearray()
        self.look_for_object_name = True
        self.look_for_object_content = False
        
    def push_cfg_data(self, cfg_data):
        self.cfg_data = cfg_data
        
    
    def get_cfg_data(self):
        return self.cfg_data
    
    def show_cfg_data(self):
        print("cfg data: ", self.cfg_data)
        
    def is_child_empty(self):
        return self.child.empty()
    
    def push_child(self, child_object):
        print("push child for object ", self.get_object_name())
        self.child.put(child_object)
        
    def get_child_list(self):
        return  list(self.child.queue)
    
    def get_look_for_object_name(self):
        return self.look_for_object_name
    
    def get_look_for_object_content(self):
        return self.look_for_object_content
    
    def set_look_for_object_name(self, to_set):
        self.look_for_object_name = to_set
        
    def set_look_for_object_content(self, to_set):
        self.look_for_object_content = to_set
        
    def show_child(self):
        if self.is_child_empty():
            if self.cfg_data == "":
                print("object name: ", super().get_object_name(), ", no child, no cfg data")
            else:
                print("object name: ", super().get_object_name(), ", no child, cfg data: ", self.get_cfg_data())
        else:
            print("object name: ", super().get_object_name(), "has child: ")
            temp_list = list(self.child.queue)
            for item in temp_list:
                print("object:", self.get_object_name(), ",", "child object: ", end="")
                item.show_child()

    