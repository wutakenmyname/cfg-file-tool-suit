import binascii
import struct
import sys
from base_parser import Base_parser
import numpy as np
import general_object
import sub_cfgs
import sub_cfgs_parser
import parser_collection as p


class String_parser(Base_parser):
    def generate_bin_data(self, string_object):
        object_name = string_object.get_object_name()
        cfg_data_string = string_object.get_cfg_data()
        print("object name: ", "cfg data: ", cfg_data_string)
        bin_data = bytearray()
        if cfg_data_string == "":
            print("empty string")
            return None
        
        cfg_data_string = cfg_data_string.strip()
        if cfg_data_string == "":
            print("empty string")
            return None
        if cfg_data_string[0] != "\"" or cfg_data_string[-1] != "\"":
            error_msg = "invalid cfg data" + cfg_data_string + ", it is not a string , it should start with\" and end with \"\n"
            raise ValueError(error_msg)
        cfg_data_string = cfg_data_string[1:]
        cfg_data_string = cfg_data_string[0:-1]
        string_bytes = bytearray(cfg_data_string, 'ascii')
        for i in range(len(string_bytes)):
            print("address: ", i, " value: ", hex(string_bytes[i]))
        
        length = len(cfg_data_string)
        length_bytes = bytearray(struct.pack('<q', length)) 
        object_id = sub_cfgs.Sub_cfgs().get_object_id_by_object_name(object_name)
        object_id_bytes = bytearray(struct.pack('<q', object_id))
        for i in range(len(object_id_bytes)):
            print("Address:", i, ", Byte value:", hex(object_id_bytes[i]))
            
        ret = object_id_bytes + length_bytes + string_bytes
        print(binascii.hexlify(ret).decode('utf-8'))  
        return object_id_bytes + string_bytes
            

def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    string_parser = String_parser()
    name_object = general_object.general_object("name")
    name_object.push_cfg_data("\"mok\"")
    print(string_parser.generate_bin_data(name_object))
    #string_parser.generate_bin_data("\"abcdefg\"")
    #string_parser.generate_bin_data("\"12.12 111")
    
if __name__ == "__main__":
    main()