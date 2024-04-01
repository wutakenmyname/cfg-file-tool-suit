import os

class Sub_cfgs_parser(object):
    _instance = None
    type_name_start_middle_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    type_name_character_middle_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_."
    type_name_character_end_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    def __new__(Sub_cfgs_parser, *args, **kw):
        if Sub_cfgs_parser._instance is None:
            Sub_cfgs_parser._instance = object.__new__(Sub_cfgs_parser, *args, **kw)
        return Sub_cfgs_parser._instance
    
    @staticmethod
    def read_file(file_name):
        try:
            with open(file_name, 'r') as file:
                file_content = file.read()  # 读取文件的所有内容
                file.close()
                return file_content
        except FileNotFoundError:
            print("File not found:", file_name)
            return None
    
    @staticmethod
    def is_comment_line(line):
        if len(line) < 2:
            print("line lenght short than 2")
            return False;
        else:
            line.strip()
            if line[0] == '/' and line[1] == '/':
                return True;
            else:
                return False
            
    @staticmethod
    def in_character_set(string, start_character_set, middle_character_set, end_character_set):
        if not start_character_set and not middle_character_set and not end_character_set:
            print("all characters are empty")
            return True;
        if not string :
            print("you have use a empty string as param")
            return False
        if start_character_set:
            if start_character_set.find(string[0]) == -1:
                return False
                
        if middle_character_set:
            for c in string[1:-1]:
                if middle_character_set.find(c) == -1:
                    return False
        
        if end_character_set:
            if end_character_set.find(string[-1]) == -1:
                return False
        
        return True
    
    @staticmethod
    def convert_to_int(str_number):
        try:
            int_number = int(str_number)
            return int_number
        except ValueError:
            print("Error: Unable to convert string to int.")
            return None
        
    @staticmethod
    def good_type_name(type_name):
        n = type_name.strip()
        if len(n) == 0:
            return False;
        else:
            return Sub_cfgs_parser.in_character_set(n, Sub_cfgs_parser.type_name_start_character_set, Sub_cfgs_parser.type_name_start_middle_set, Sub_cfgs_parser.type_name_character_end_set)
        
    @staticmethod
    def good_type_type(type_name):
        n = type_name.strip()
        if len(n) == 0:
            return False;
        else:
            num = Sub_cfgs_parser.convert_to_int(n)
            if num is None:
                return False;
            else:
                if num <= 0 or num > 128:
                    return False
                return True

    @staticmethod
    def good_type_id(type_name):
        n = type_name.strip()
        if len(n) == 0:
            return False;
        else:
            num = Sub_cfgs_parser.convert_to_int(n)
            if num is None:
                return False;
            else:
                if num <= 0 or num > 2147483647:
                    return False
                return True
    
    @staticmethod
    def parse_file(file_name):
        if not os.path.exists(file_name) :
            print(file_name, " not exist")
            return -1
        else :
            file_content = Sub_cfgs_parser.read_file(file_name)
            if file_content is None:
                print("cannot read file ", file_name)
                return -1
            else:
                lines = file_content.splitlines()
                line_number = 0
                for line in lines:
                    line_number = line_number + 1
                    stripped_line = line.strip()
                    if len(stripped_line) == 0:
                        print("line [", line_number, "] empty line")
                        continue
                    elif len(stripped_line) < 2:
                        print("line [", line_number, "] \"", line, "\" broken line")
                        continue
                    elif len(stripped_line) == 2 and Sub_cfgs_parser.is_comment_line(stripped_line) is True:
                        print("line [", line_number, "] \"", line, "\" empty comment line")
                        continue
                    elif len(stripped_line) < 7:
                        if Sub_cfgs_parser.is_comment_line(stripped_line) is True:
                            print("line [", line_number, "] \"", line, "\" comment line")
                            continue
                        else:
                            print("line [", line_number, "] \"", line, "\" broken line")
                    else:
                        line_length = len(stripped_line)
                        if Sub_cfgs_parser.is_comment_line(stripped_line) is True:
                            print("line [", line_number, "] \"", line, "\" comment line")
                            continue
                        else:
                            if stripped_line[0] != '(' or stripped_line[line_length - 1] != ')':
                                print("line [", line_number, "] \"", line, "\" broken line")
                                continue
                            else:
                                temp = stripped_line
                                temp = temp[1:]
                                no_brackets_stripped_line = temp[:-1]
                                if no_brackets_stripped_line.count(',') != 2:
                                    print("line [", line_number, "] \"", line, "\" broken line")
                                    continue
                                else:
                                    c = no_brackets_stripped_line.split(',');
                                    for i in range(len(c)):
                                        c[i] = c[i].strip()
                                        c1 = c[i]
                                        if not c1:
                                            print("line [", line_number, "] \"", line, "\" broken line")
                                    
                                    if Sub_cfgs_parser.good_type_name(c[0]) is not True or \
                                        Sub_cfgs_parser.good_type_type(c[1], Sub):
                                        print("line [", line_number, "] \"", line, "\" broken line")
                                    
                                            
                                            
                                        

                                    





