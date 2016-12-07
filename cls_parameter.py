#!/usr/bin/python3

class Parameter:
    
    def __init__(self, _, attr_dict):
                
        #self.my_method = method       #must be added manualy, if decided that it's neccessary
        self.name = attr_dict["name"]
        self.d_type = attr_dict["type"]        
        
        self.comment = attr_dict["comment"]
        self.value = None
        
        #if value present
        if attr_dict["value"] != "":
            self.value = attr_dict["value"]
        
        

            
    def print_me(self):

        print(self.name)
        print(self.d_type)
        print(self.value)

            
