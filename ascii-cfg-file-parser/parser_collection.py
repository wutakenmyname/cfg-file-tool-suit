import threading
import inspect
import importlib
import os


class Parser_collection(object):
    _instance = None
    parser_name_character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    def __new__(Parser_collection, *args, **kw):
        if Parser_collection._instance is None:
            Parser_collection._instance = object.__new__(Parser_collection, *args, **kw)
            Parser_collection._instance.lock = threading.Lock()
            Parser_collection._instance.type_map = {}
            Parser_collection._instance.parsers = dict()
        return Parser_collection._instance
    
    def register(self, parser_dict):
        print("registered parser name: ", list(parser_dict.keys())[0])
        self.parsers.update(parser_dict)
    
    def is_parser_name_ok(self, parser_name):
        for c in parser_name:
            if self.parser_name_character_set.find(c) == -1:
                return False
        return True
            
    def load_all(self):
        file_name = "parser.conf"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(script_dir, file_name)
        try:
            with open(file_name, 'r') as file:
                file_content = file.read()  # 读取文件的所有内容
                file.close()
        except FileNotFoundError:
            print("File not found:", file_name)
            error_msg = "File not found:" + file_name + "\n"
            raise ValueError(error_msg)
        
        lines = file_content.splitlines()
        line_number = 0
        for parser_name in lines:
            line_number = line_number + 1
            parser_name = parser_name.strip()
            if len(parser_name) == 0:
                continue
            if self.is_parser_name_ok(parser_name) is False:
                error_msg = "line[" + str(line_number), "] invalid parser name: " + parser_name
                raise ValueError(error_msg)
            self.load(parser_name)
            
        
    def load(self, parser_to_load):
        print("parser to load: ", parser_to_load)
        import importlib

        target_module = importlib.import_module(parser_to_load)

        # 获取模块中定义的所有类
        classes = [obj for name, obj in inspect.getmembers(target_module, inspect.isclass)]

        
        for cls in classes:
            #print(cls.__name__)
            if cls.__name__.lower() == parser_to_load.lower():
                print("meet it: ", cls.__name__)
                parser = cls()
                self.register({parser_to_load.lower(): parser})
    def retrieve_parser_by_parser_name(self, parser_name):
        return self.parsers[parser_name.lower()]

            
    
    
    
def main():
    pc = Parser_collection()
    pc.load_all()
    
if __name__ == "__main__":
    main()        