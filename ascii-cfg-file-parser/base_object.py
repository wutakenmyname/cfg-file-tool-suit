import queue
import traceback


class base_object():
    def __init__(self, object_name):
        if not object_name:
            stack_trace = traceback.format_stack()
            error_msg = "object_name不能为空字符串\n" + "".join(stack_trace)
            raise ValueError(error_msg)
        self.object_name = object_name
        self.child = queue.Queue();
    
    def get_object_name(self):
        return self.object_name
    
    def is_biggest_object(self):
        if not self.object_name:
            return False
        if self.object_name == "biggest_object":
            return True
        else:
            return False