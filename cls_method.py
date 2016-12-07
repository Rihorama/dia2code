#!/usr/bin/python3

class Method:
    
    visibility_dict = {0 : "public",
                       1 : "private",
                       2 : "protected",
                       3 : "implementation"}
    
    
    def __init__(self, cls, attr_dict):
                
        self.my_class = cls       
        self.name = attr_dict["name"]
        self.d_type = attr_dict["type"]        
        self.visibility = attr_dict["visibility"]  
        
        self.param_list = attr_dict["parameters"]
        
        self.comment = attr_dict["comment"]
        
        

            
    def print_me(self):

        print(self.name)
        print(self.d_type)
        print(self.visibility_dict[self.visibility])
        
        for i in self.param_list:
            i.print_me()

            
