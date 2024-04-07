import binascii
import struct
import sys
from base_parser import Base_parser
import numpy as np
import general_object
import sub_cfgs
import sub_cfgs_parser
import parser_collection as p

class Double_parser(Base_parser):
    def generate_bin_data(self, double_object):
        object_name = double_object.get_object_name()
        cfg_data_string = double_object.get_cfg_data()
        print("object name: ", object_name, " cfg data: ", cfg_data_string)
        bin_data = bytearray()
        
        if cfg_data_string == "":
            return None
        try:
            double_value = np.float64(cfg_data_string)
            #print(double_value)  # 输出: 3.14
        except ValueError:
            mib_object
            
        double_bytes = struct.pack('d', double_value)
        
        object_id = sub_cfgs.Sub_cfgs().get_object_id_by_object_name(object_name)
        object_id_bytes = bytearray(struct.pack('<q', object_id))   
        for i in range(len(object_id_bytes)):
            print("Address:", i, ", Byte value:", hex(object_id_bytes[i]))  
        
        length_bytes = bytearray(struct.pack('<q', 8))
        ret = object_id_bytes + length_bytes + double_bytes  
        print(binascii.hexlify(ret).decode('utf-8'))           
        return  ret

def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    double_parser = Double_parser()
    double_object = general_object.general_object("height")
    double_object.push_cfg_data("688.34543")
    print(double_parser.generate_bin_data(double_object))
    
if __name__ == "__main__":
    main()