import binascii
import base_parser

import struct
import sys
from base_parser import Base_parser
import numpy as np
import general_object
import sub_cfgs
import sub_cfgs_parser
import parser_collection as p


class Hex_parser(Base_parser):
    def generate_bin_data(self, hex_object):
        object_name = hex_object.get_object_name()
        cfg_data_string = hex_object.get_cfg_data()
        print("object name: ", object_name, " cfg data: ", cfg_data_string)
        bin_data = bytearray()

        if cfg_data_string == "":
            return None
        try:
            hex_bytes = bytearray.fromhex(cfg_data_string)
            for i in range(len(hex_bytes)):
                print("address: ", i, " value: ", hex(hex_bytes[i]))
        except ValueError as e:
            error_msg = "invalid cfg data" + cfg_data_string + ", it is not a string of hex sequence\n"
            raise ValueError(error_msg)
        
        length = len(cfg_data_string)
        length_bytes = bytearray(struct.pack('<q', int(length/2)))
        object_id = sub_cfgs.Sub_cfgs().get_object_id_by_object_name(object_name)
        object_id_bytes = bytearray(struct.pack('<q', object_id))   
        for i in range(len(object_id_bytes)):
            print("Address:", i, ", Byte value:", hex(object_id_bytes[i]))   
        ret =  object_id_bytes + length_bytes + hex_bytes
        
        print(binascii.hexlify(ret).decode('utf-8'))        
        return  ret

def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    hex_parser = Hex_parser()
    id_object = general_object.general_object("id")
    id_object.push_cfg_data("11223344")
    print(hex_parser.generate_bin_data(id_object))
    
if __name__ == "__main__":
    main()