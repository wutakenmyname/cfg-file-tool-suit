
import threading


class Character_set_validator(object):
    _instance = None
    def __new__(Character_set_validator, *args, **kw):
        if Character_set_validator._instance is None:
            Character_set_validator._instance = object.__new__(Character_set_validator, *args, **kw)
            Character_set_validator._instance.lock = threading.Lock()
        return Character_set_validator._instance

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
    def is_oid_string(input):
        if input == "":
            error_msg = "empty string\n"
            raise ValueError(error_msg)
        input = input.strip()
        if len(input) == 0:
            error_msg = "empty string\n"
            raise ValueError(error_msg)
        if input[0] == '.' or input[-1] == '.':
            error_msg = "can not start with . or end with .\n"
            raise ValueError(error_msg)
        for i in range(len(input)):
            if input[i] != '.' or input.isalpha() is False:
                return False
        return True