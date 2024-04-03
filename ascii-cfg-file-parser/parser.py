import queue
import sub_cfgs
import sub_cfgs_parser
import general_object as g


class Parser():
   object_name_character_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
   def __init__(self):
      self.file_content = ""
      self.biggest_object = g.general_object("biggest_object")
      
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
      pos = 0
      line_number = 1
      obj_queue = queue.Queue()
      curly_braces = queue.Queue()
      #cur_obj = ""
      while True:
         if pos >= file_len:
            break
         elif self.file_content[pos].isspace():
            print("goes here, space character, line:" + str(line_number))
            pos = pos + 1
            continue
         elif self.file_content[pos] == '\n':
            print("goes here, line break, line number:" + str(line_number))
            pos = pos + 1
            line_number = line_number + 1
            continue
         elif self.file_content[pos] == '{':
            if curly_braces.empty() is True:
               print("goes here, biggest object, line number: " + str(line_number))
               cur_obj = g.general_object("biggest_object")
               cur_obj.set_look_for_object_content(True)
               cur_obj.set_look_for_object_name(False)
               pos = pos + 1
               curly_braces.put('{')
               continue
            else:
               print("goes here, new object, line number: " + str(line_number))
               new_obj = g.general_object('-')
               cur_obj.push_child(new_obj)
               cur_obj.set_look_for_object_content(True)
               cur_obj.set_look_for_object_name(False)
               obj_queue.put(cur_obj)
               cur_obj = new_obj
               pos = pos + 1
               #cur_obj.set_look_for_object_content(False)
               #cur_obj.set_look_for_object_name(True)
               continue
         elif self.file_content[pos] == '}':
            print("goes here, }, line number: " + str(line_number))
            if curly_braces.empty() is True:
               error_msg = "line [" + str(line_number) + "] unmatched }\n"
               raise ValueError(error_msg)
            else:
               cur_obj.set_look_for_object_content(False)
               cur_obj.set_look_for_object_name(False)
               curly_braces.get()
               cur_obj = obj_queue.get()
               pos = pos + 1
               continue
         elif cur_obj.get_look_for_object_name() is True and self.object_name_character_set.find(self.file_content[pos]) == -1:
            print("goes here, invalid object name, line number:" + str(line_number))
            error_msg = "invalid object name in line[" + str(line_number) + "]\n"
            raise ValueError(error_msg)
         elif cur_obj.get_look_for_object_name() is True and self.object_name_character_set.find(self.file_content[pos]) != -1:
            print("goes here, get a character of object name, line number:" + str(line_number))
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
                  line_number = line_number + 1
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos].isspace() is True:
                  cur_obj.set_look_for_object_content(True)
                  cur_obj.set_look_for_object_name(False)
                  cur_obj.set_object_name(temp_object_name)
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '{':
                  new_obj = g.general_object('-')
                  cur_obj.push_child(new_obj)
                  cur_obj.set_object_name(temp_object_name)
                  cur_obj.set_look_for_object_content(True)
                  cur_obj.set_look_for_object_name(False)
                  obj_queue.put(cur_obj)
                  cur_obj = new_obj
                  curly_braces.put('{')
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '}':
                  if curly_braces.empty is True:
                     error_msg = "line [" + str(line_number) + "] unmatched }\n"
                     raise ValueError(error_msg)
                  else:
                     curly_braces.get()
                     cur_obj.set_object_name(temp_object_name)
                     cur_obj.set_look_for_object_content(False)
                     cur_obj.set_look_for_object_name(False)
                     pos = pos + 1
                     failed = False
                     break
               else:
                  error_msg = "line [" + str(line_number) + "] invalid object character in object name\n"
                  raise ValueError(error_msg)
            if failed is True:
               error_msg = "line [" + str(line_number) + "] unexpected end of file\n"
               raise ValueError(error_msg)
         elif cur_obj.get_look_for_object_content() is True:
            temp_cfg_data = ""
            temp_cfg_data = temp_cfg_data + self.file_content[pos]
            failed = True
            pos = pos + 1
            while pos < file_len:
               if self.file_content[pos].isspace() is True:
                  temp_cfg_data = temp_cfg_data + self.file_content[pos]
                  pos = pos + 1
                  continue
               elif self.file_content[pos] == '{':
                  error_msg = "line [" + str(line_number) + "] unexpected '{' when parsing object content, if the object is composed of other objects then it should not contain real cfg data on that\n"
                  raise ValueError(error_msg)
               elif self.file_content[pos] == '}':
                  cur_obj.push_cfg_data(temp_cfg_data)
                  print("object name: "+cur_obj.get_object_name() + ", cfg data: " + cur_obj.get_cfg_data())
                  cur_obj.set_look_for_object_content(False)
                  cur_obj.set_look_for_object_name(False)
                  cur_obj = obj_queue.get()
                  pos = pos + 1
                  failed = False
                  break
               elif self.file_content[pos] == '\n':
                  error_msg = "line [" + str(line_number) + "] unexpected line break, cfg data should be same line\n"
                  raise ValueError(error_msg)
            if failed is True:
               error_msg = "line [" + str(line_number) + "] unexpected end of file\n"
               raise ValueError(error_msg)    
                  
                      
         #elif self.object_name_character_set.find(self.file_content[pos]):
            #return 
            
         
         
      



def main():
   parser = Parser()
   parser.parse("cfg_example1.sscfg")

if __name__ == "__main__":
    main()