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
      #cur_obj
      while True:
         if pos >= file_len:
            break
         elif self.file_content[pos].isspace():
            pos = pos + 1
            continue
         elif self.file_content[pos] == '\n':
            pos = pos + 1
            line_number = line_number + 1
            continue
         elif self.file_content[pos] == '{':
            if curly_braces.empty() is True:
               cur_obj = g.general_object("biggest_object")
               cur_obj.set_look_for_object_content(True)
               cur_obj.set_look_for_object_name(False)
               pos = pos + 1
               curly_braces.put('{')
               continue
            else:
               new_obj = g.general_object('-')
               cur_obj.push_child(new_obj)
               obj_queue.put(cur_obj)
               cur_obj = new_obj
               pos = pos + 1
               cur_obj.set_look_for_object_content(False)
               cur_obj.set_look_for_object_name(True)
               continue
         elif self.file_content[pos] == '}':
            if curly_braces.empty() is True:
               error_msg = "unmatched }\n"
               raise ValueError(error_msg)
            else:
               curly_braces.get()
               cur_obj = obj_queue.get()
               pos = pos + 1
               continue
         elif cur_obj.get_look_for_object_name is True and self.object_name_character_set.find(self.file_content[pos]) == -1:
            error_msg = "invalid object name in line" + line_number + "\n"
            raise ValueError(error_msg)
            
         elif self.object_name_character_set.find(self.file_content[pos]) 
            
         
         
      



def main():
   parser = Parser()
   parser.parse("cfg_example1.sscfg")

if __name__ == "__main__":
    main()