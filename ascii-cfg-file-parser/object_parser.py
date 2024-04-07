import binascii
import struct
import base_parser
import general_object as g
import parser_collection as p
import sub_cfgs 
import general_object
import sub_cfgs_parser


class Object_parser(base_parser.Base_parser):
    def generate_bin_data(self, object_to_parse):
        object_name = object_to_parse.get_object_name()
        print("name of object going to be parsed: ", object_to_parse.get_object_name())
        if (object_to_parse.is_child_empty()):
            return bytearray()
        else:
            child_list = object_to_parse.get_child_list()
            ret = bytearray()
            for child in child_list:
                parser_name = sub_cfgs.Sub_cfgs().get_parser_name_by_object_name(child.get_object_name())
                if parser_name is None:
                    error_msg = "object " + child.get_object_name() + " is not registered, can not find a parser for it\n"
                    raise ValueError(error_msg)
                parser = p.Parser_collection().retrieve_parser_by_parser_name(parser_name)
                ret = ret + parser.generate_bin_data(child)

            print(binascii.hexlify(ret).decode('utf-8'))   
            return ret



def main():
    sub_cfgs_parser.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
    sub_cfgs.Sub_cfgs().dump()
    pc = p.Parser_collection()
    pc.load_all()
    test_object = g.general_object("misc")
    name_object = g.general_object("name")
    name_object.push_cfg_data("\"mok\"")
    test_object.push_child(name_object)
    object_parser = Object_parser()
    print(object_parser.generate_bin_data(test_object))
    
    
if __name__ == "__main__":
    main()