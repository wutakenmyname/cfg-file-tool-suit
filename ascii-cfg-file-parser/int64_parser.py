import binascii
import struct
import sys
from base_parser import Base_parser
import numpy as np
import general_object
import sub_cfgs
import sub_cfgs_parser
import parser_collection as p


class Int64_parser(Base_parser):
    def generate_bin_data(self, int64_object):
        object_name = int64_object.get_object_name()
        cfg_data_string = int64_object.get_cfg_data()
        print("object name: ", "cfg data: ", cfg_data_string)
        bin_data = bytearray()
        if cfg_data_string == "":
            return None
        try:
            int64_value = np.int64(cfg_data_string)
            #print(int64_value)  # 输出: 3.14
        except ValueError:
            error_msg = "invalid cfg data" + cfg_data_string + ", it is not a string of int64 number\n"
            raise ValueError(error_msg)
            
        int64_bytes = bytearray(struct.pack('<q', int64_value))
       
        for i in range(len(int64_bytes)):
            print("Address:", i, ", Byte value:", hex(int64_bytes[i]))
            
        object_id = np.int64(sub_cfgs.Sub_cfgs().get_object_id_by_object_name(object_name))
        object_id_bytes = bytearray(struct.pack('<q', object_id))   
        for i in range(len(object_id_bytes)):
            print("Address:", i, ", Byte value:", hex(object_id_bytes[i]))
            
        length_bytes = bytearray(struct.pack('<q', 8))       
        ret = object_id_bytes + length_bytes + int64_bytes  
        print(binascii.hexlify(ret).decode('utf-8'))     
        return  

def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    int64_parser = Int64_parser()
    boo_object = general_object.general_object("boo")
    boo_object.push_cfg_data("688")
    print(int64_parser.generate_bin_data(boo_object))
    
if __name__ == "__main__":
    main()