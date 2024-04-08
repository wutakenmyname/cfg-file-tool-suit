import binascii
import queue
import struct
import threading

import numpy as np
import base_parser
import general_object as g
import parser_collection as p
import sub_cfgs 
import general_object
import sub_cfgs_parser
import mib_storage as m
import character_set_validator 

class Mib_parser(base_parser.Base_parser):
    _instance = None
    def __new__(Mib_parser, *args, **kw):
        if Mib_parser._instance is None:
            Mib_parser._instance = object.__new__(Mib_parser, *args, **kw)
            Mib_parser._instance.lock = threading.Lock()
            mib_storage = m.Mib_storage()
            mib_storage.generate_from_file("mib_cfg")
            Mib_parser.mib_storage = mib_storage
        return Mib_parser._instance
    
    @staticmethod
    def generate_type_arraybyte_by_type_string(type_string):
        ret = bytearray()
        if type_string == "string":
            ret = ret + bytearray(struct.pack('B', 4))
        return ret
    
    @staticmethod
    def generate_oid_arraybyte_by_oid_string(oid_string):
        ret = bytearray()
        oid_parts = oid_string.strip().split('.')
        oid_uint32_parts = []
        print("oid part: ", oid_parts)
        if len(oid_parts) < 2:
            error_msg = "oid is too short, it must have more than 2 parts\n"
            raise ValueError(error_msg)
        for i in range(len(oid_parts)):
            oid_uint32_parts.append(int(oid_parts[i]))
            
        ret = ret + struct.pack('B', oid_uint32_parts[0] * 40 + oid_uint32_parts[1])
        for i in range(2, len(oid_uint32_parts)):
            cur_number = oid_uint32_parts[i]
            q = 0
            r = 0
            res_queue = queue.LifoQueue()
            
            while(True):
                q = cur_number // 128
                r = cur_number % 128
                res_queue.put(r)
                if q >= 128:
                    cur_number = q
                    r = 0
                else:
                    if q != 0:
                        res_queue.put(q)
                    break
            
            print("qsize: ", res_queue.qsize())
            for iter in range(res_queue.qsize() - 1):
                t = res_queue.get()
                print("t: ", t)
                ret = ret + bytearray(struct.pack('B', t + 128))
                    
            ret = ret + bytearray(struct.pack('B', res_queue.get()))
                
        #for i in range(len(ret)):
         #   print("Address:", i, ", Byte value:", hex(ret[i]))   
            
        return ret
    def generate_bin_data(self, mib_object):
        object_name = mib_object.get_object_name()
        cfg_data_string = mib_object.get_cfg_data()
        print("object name: ", object_name, " cfg data: ", cfg_data_string)
        cfg_data_string = cfg_data_string.strip()
        mib_parts = cfg_data_string.split(None)
        if len(mib_parts) != 3:
            error_msg = "wrong mib cfg, it should be compose of oid value-type value these 3 parts\n"
            raise ValueError(error_msg)
        
        oid_string = mib_parts[0]
        value_type = mib_parts[1]
        value = mib_parts[2]
        
        if value_type != "string":
            error_msg = "only support string type for mib now\n"
            raise ValueError(error_msg)
        else:
            type_bytes = self.generate_type_arraybyte_by_type_string(value_type)
        
        if value[0] != "\"" or value[-1] != "\"":
            error_msg = "invalid mib value" + value + ", it is not a string , it should start with\" and end with \"\n"
            raise ValueError(error_msg)
        value = value[1:]
        value = value[0:-1]
        value_bytes = bytearray(value, 'ascii')
        
        if character_set_validator.Character_set_validator().is_oid_string(oid_string) is False:
            oid_string_configured = self.mib_storage.get_oid_by_mib_name(oid_string)
            if  oid_string_configured is not None:
                oid_string = oid_string_configured
        print("mib: ", oid_string, ", ", value_type, ", ", value)
        
        oid_bytes = self.generate_oid_arraybyte_by_oid_string(oid_string)
        object_id = np.int64(sub_cfgs.Sub_cfgs().get_object_id_by_object_name(object_name))
        print("object id for snmpmib: ", object_id)
        object_id_bytes = bytearray(struct.pack('<q', object_id))
        
        oid_length = len(oid_bytes)
        oid_length_bytes = bytearray(struct.pack('B', oid_length))
        
        length = len(oid_length_bytes) + len(oid_bytes) + len(type_bytes) + len(value_bytes)
        length_bytes = bytearray(struct.pack('<q', length))
        
        
        
        ret = object_id_bytes + length_bytes + oid_length_bytes + oid_bytes + type_bytes + value_bytes
        print("snmpmib encode:")
        for i in range(len(ret)):
            print("", hex(ret[i]), end="")   

        return ret
    
def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    mib_parser = Mib_parser();
    mib_object = general_object.general_object("snmpmib")
    mib_object.push_cfg_data("   1.2.999.999  string \"mok\"")
    mib_parser.generate_bin_data(mib_object)
    
if __name__ == "__main__":
    main()