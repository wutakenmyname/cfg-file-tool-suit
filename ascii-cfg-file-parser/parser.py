import os
import queue
import sub_cfgs
import sub_cfgs_parser
import general_object as g
import sub_cfgs_parser as sub
from sub_cfgs import Sub_cfgs as sub_cfg_storage
import parser_collection as p
import hashlib

class Parser():
   object_name_character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
   def __init__(self):
      self.file_content = ""
      self.biggest_object = g.general_object("biggest_object")
      sub.Sub_cfgs_parser.parse_file("sub_cfgs.conf")
      sub_cfg_storage().dump()
      pc = p.Parser_collection()
      pc.load_all()
   def read_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                file_content = file.read()  # 读取文件的所有内容
                file.close()
                return file_content
        except FileNotFoundError:
            print("File not found:", file_name)
            return None
   
   def parse(self, file_name):
      self.file_content = self.read_file(file_name)
      if self.file_content is None:
         error_msg = "parse file " + file_name + " failed\n"
         raise ValueError(error_msg)
      file_len = len(self.file_content)
      #print("file content: ", self.file_content)
      all_failed = True
      pos = 0
      line_number = 1
      obj_queue = queue.LifoQueue()
      cur_obj = ""
      temp_object_name = ""
      while True:
         if pos >= file_len:
            break
         elif self.file_content[pos].isspace() and self.file_content[pos] != '\n':
            print("goes here, space character, line:" + str(line_number))
            pos = pos + 1
            continue
         elif self.file_content[pos] == '\n':
            print("goes here, line break, line number:" + str(line_number))
            pos = pos + 1
            line_number = line_number + 1
            continue
         elif self.file_content[pos] == '{':
            print("goes here, {, line number: " + str(line_number))
            if obj_queue.empty() is True and cur_obj == "":
               print("goes here, biggest object, line number: " + str(line_number))
               cur_obj = g.general_object("biggest_object")
               print("biggest object: object name: ", str(cur_obj.get_object_name()))
               cur_obj.set_look_for_object_content(True)
               cur_obj.set_look_for_object_name(False)
               pos = pos + 1
               continue
            else:
               print("temp object name: ", temp_object_name)
               print("goes here, new object, line number: " + str(line_number))

               new_obj = g.general_object('_')
               cur_obj.push_child(new_obj)
               cur_obj.set_look_for_object_content(True)
               cur_obj.set_look_for_object_name(False)
               print("push object: ", cur_obj.get_object_name() + " into obj.queue")
               obj_queue.put(cur_obj)
               cur_obj = new_obj
               pos = pos + 1
               #cur_obj.set_look_for_object_content(False)
               #cur_obj.set_look_for_object_name(True)
               continue
         elif self.file_content[pos] == '}':
            print("goes here, }, line number: " + str(line_number))
            if obj_queue.empty() is True and cur_obj == "":
               error_msg = "line[" + str(line_number) + "] unpexected extra '}'\n"
               raise ValueError(error_msg)
            elif obj_queue.empty() is True and cur_obj.get_object_name() == "biggest_object":
               print("finish this parse process")
               if pos + 1 < file_len:
                  error_msg = "line[" + str(line_number) + "] file should end, but there is unpexected extra data '}'\n"
                  raise ValueError(error_msg)
               else:
                  all_failed = False
                  break
            elif obj_queue.empty() is True and cur_obj.get_object_name() != "biggest_object":
               error_msg = "line[" + str(line_number) + "] invalid parse process, something wrong happened2\n"
               raise ValueError(error_msg)
            else:
               print("line }, obj queue not empty")
               cur_obj.set_look_for_object_content(False)
               cur_obj.set_look_for_object_name(False)
               cur_obj = obj_queue.get()
               print("pop obj name:", cur_obj.get_object_name())
               pos = pos + 1
               continue
         elif cur_obj.get_look_for_object_name() is True and self.object_name_character_set.find(self.file_content[pos]) == -1:
            print("goes here, invalid object name, line number:" + str(line_number))
            error_msg = "invalid object name in line[" + str(line_number) + "]\n"
            raise ValueError(error_msg)
         elif cur_obj.get_look_for_object_name() is True and self.object_name_character_set.find(self.file_content[pos]) != -1:
            print("goes here, get a character'",str((self.file_content[pos])) + "' of object name, line number:" + str(line_number))
            if cur_obj == "":
               error_msg = "[" + str(line_number) + "] no object but there is object content \n"
               raise ValueError(error_msg)
            if cur_obj.get_object_name() == "biggest_object":
               error_msg = "line [" + str(line_number) + "] biggest object should not configure object name for it by you\n"
               raise ValueError(error_msg)
            
            temp_object_name = ""
            temp_object_name = temp_object_name + self.file_content[pos]
            failed = True
            pos = pos + 1
            while pos < file_len:
               if self.object_name_character_set.find(self.file_content[pos]) != -1:
                  temp_object_name = temp_object_name + self.file_content[pos]
                  pos = pos + 1
                  continue
               elif self.file_content[pos] == '\n':
                  cur_obj.set_look_for_object_content(True)
                  cur_obj.set_look_for_object_name(False)
                  cur_obj.set_object_name(temp_object_name)
                  temp_object_name = ""
                  line_number = line_number + 1
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos].isspace() is True and self.file_content[pos] != '\n':
                  cur_obj.set_look_for_object_content(True)
                  cur_obj.set_look_for_object_name(False)
                  cur_obj.set_object_name(temp_object_name)
                  print("2cur_obj name: ", cur_obj.get_object_name())
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '{':
                  new_obj = g.general_object('_')
                  cur_obj.push_child(new_obj)
                  cur_obj.set_object_name(temp_object_name)
                  temp_object_name = ""
                  cur_obj.set_look_for_object_content(True)
                  cur_obj.set_look_for_object_name(False)
                  obj_queue.put(cur_obj)
                  cur_obj = new_obj
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '}':
                  if obj_queue.empty is True and cur_obj == "":
                     error_msg = "line [" + str(line_number) + "] unmatched }\n"
                     raise ValueError(error_msg)
                  elif obj_queue.empty is True and cur_obj.get_object_name() == "biggest_object":
                     error_msg = "line [" + str(line_number) + "] unmatched }\n"
                     raise ValueError(error_msg)
                  elif obj_queue.empty is True and cur_obj.get_object_name() != "biggest_object":
                     error_msg = "line [" + str(line_number) + "] something wrong happened in this parse process\n"
                     raise ValueError(error_msg)
                  else:
                     cur_obj.set_object_name(temp_object_name)
                     temp_object_name = ""
                     cur_obj.set_look_for_object_content(False)
                     cur_obj.set_look_for_object_name(False)
                     cur_obj = obj_queue.get()
                     print("3pop obj name: ", cur_obj.get_object_name())
                     pos = pos + 1
                     failed = False
                     break
               else:
                  error_msg = "line [" + str(line_number) + "] invalid object character in object name\n"
                  raise ValueError(error_msg)
            if failed is True:
               error_msg = "line [" + str(line_number) + "] unexpected end of file2\n"
               raise ValueError(error_msg)
         elif cur_obj.get_look_for_object_content() is True:
            print("looking for object content of object ", cur_obj.get_object_name())
            temp_cfg_data = ""
            temp_cfg_data = temp_cfg_data + self.file_content[pos]
            failed = True
            pos = pos + 1
            while pos < file_len:
               if self.file_content[pos].isspace() is True and self.file_content[pos] != '\n':
                  temp_cfg_data = temp_cfg_data + self.file_content[pos]
                  pos = pos + 1
                  continue
               elif self.file_content[pos] == '{':
                  error_msg = "line [" + str(line_number) + "] unexpected '{' when parsing object content, if the object is composed of other objects then it should not contain real cfg data on that\n"
                  raise ValueError(error_msg)
               elif self.file_content[pos] == '}':
                  cur_obj.push_cfg_data(temp_cfg_data)
                  print("object name: " + str((cur_obj.get_object_name())) + ", cfg data: " + cur_obj.get_cfg_data())
                  cur_obj.set_look_for_object_content(False)
                  cur_obj.set_look_for_object_name(False)
                  cur_obj = obj_queue.get()
                  print("1pop obj name: ", cur_obj.get_object_name())
                  print("temp_object_name:", temp_object_name)
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '\n':
                  ascii_list = [ord(c) for c in temp_cfg_data]
                  print("code of content: ", temp_cfg_data)
                  print(ascii_list)
                  print("code of content: ")
                  if len(temp_cfg_data.strip()) != 0:
                     print("not in same line")
                     error_msg = "line [" + str(line_number) + "] unexpected line break, cfg data should be same line\n"
                     raise ValueError(error_msg)
                  else:
                     line_number = line_number + 1
                     pos = pos + 1
                     continue
               else:
                  temp_cfg_data = temp_cfg_data + self.file_content[pos]
                  pos = pos + 1
                  continue
            if failed is True:
               error_msg = "line [" + str(line_number) + "] unexpected end of file1\n"
               raise ValueError(error_msg)    
                  
                      
         #elif self.object_name_character_set.find(self.file_content[pos]):
            #return 
      if all_failed is True:
         print("obj_queue is empty? ", obj_queue.empty())
         print("obj name: ", cur_obj.get_object_name())
         if cur_obj != "" and obj_queue.empty() is True and cur_obj.get_object_name == "biggest_object":
            print("all things is done")
         else:
            error_msg = "line [" + str(line_number) + "] unexpected end of file3\n"
            raise ValueError(error_msg)
      else:
         if cur_obj != "":
            print("cur obj name: ", cur_obj.get_object_name())
            cur_obj.show_child()
            parser_name = sub_cfgs.Sub_cfgs().get_parser_name_by_object_name(cur_obj.get_object_name())
            if parser_name is None:
               error_msg = "object " + cur_obj.get_object_name() + " is not registered, can not find a parser for it\n"
               raise ValueError(error_msg)
            parser = p.Parser_collection().retrieve_parser_by_parser_name(parser_name)
            bin_data = parser.generate_bin_data(cur_obj)
            byte_array = bytes(bin_data)

            # 使用 sha256 进行哈希计算
            hash_obj = hashlib.sha256(byte_array)
            hash_result = hash_obj.hexdigest()
            hash_bytes = bytearray.fromhex(hash_result)
            print("SHA256 hash:", hash_result)
            for i in range(len(hash_bytes)):
               print("", hex(hash_bytes[i]), end="")
               
            output_file_name = file_name.split(".")[0] + ".bin"
            if os.path.exists(output_file_name):
               os.remove(output_file_name)
            with open(output_file_name, 'wb') as file:
               file.write((hash_bytes + bin_data))
            return 
         else:
            error_msg = "line [" + str(line_number) + "]lost connection to biggest_object\n"
            raise ValueError(error_msg)
               
         
         
      



def main():
   parser = Parser()
   parser.parse("cfg_example1.sscfg")

if __name__ == "__main__":
    main()