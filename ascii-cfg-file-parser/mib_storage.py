

import threading
import character_set_validator

class Mib_storage(object):   
    _instance = None
    mib_name_character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    oid_chracter_set = "0123456789."
    def __new__(Mib_storage, *args, **kw):
        if Mib_storage._instance is None:
            Mib_storage._instance = object.__new__(Mib_storage, *args, **kw)
            Mib_storage._instance.lock = threading.Lock()
            Mib_storage._instance.mib_cfgs = {}
        return Mib_storage._instance
    
    def register(self, mib_name, oid):
        if mib_name == "" or oid == "" or len(mib_name) == 0 or len(oid) == 0:
            error_msg = "empty mib name or oid you have provided"
            raise ValueError(error_msg)
        #print("name: ", mib_name, ", oid: ", oid)
        self.lock.acquire()
        self.mib_cfgs.update({mib_name: oid})
        self.lock.release()
        
    def dump(self):
        self.lock.acquire()
        for k,v in self.mib_cfgs.items():
            print("name: ", k, ", mib: ", v)
        self.lock.release()
        
    def get_oid_by_mib_name(self, mib_name):
        ret = ""
        self.lock.acquire()
        res = self.mib_cfgs.get(mib_name.strip())
        ret = res
        self.lock.release()
        return ret
    
    def generate_from_file(self, file_name):
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
        for l in lines:
            line_number = line_number + 1
            if len(l.strip()) == 0:
                continue
            #print("cfg line[", line_number, " ,", l)
            validator = character_set_validator.Character_set_validator()
            name_and_oid = l.strip().split(None)
            #print(name_and_oid)
            if len(name_and_oid) != 2:
                error_msg = "invalid mib cfg \""+ l + "\" in line[" + str(line_number) + "\n"
                raise ValueError(error_msg)
            if validator.in_character_set(name_and_oid[0], "", self.mib_name_character_set, "") is False:
                error_msg = "invalid mib name \""+ name_and_oid[0] + "\" in line[" + str(line_number) + "\n"
                raise ValueError(error_msg)
            if validator.in_character_set(name_and_oid[1], "", self.oid_chracter_set, "") is False:
                error_msg = "invalid oid \""+ name_and_oid[1] + "\" in line[" + str(line_number) + "\n"
                raise ValueError(error_msg)
            self.register(name_and_oid[0].strip(), name_and_oid[1].strip())
            
            
            
def main():
    mib_storage = Mib_storage()
    mib_storage.generate_from_file("mib_cfg")
    mib_storage.dump()
    
if __name__ == "__main__":
    main()