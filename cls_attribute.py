#!/usr/bin/python3

class ClsAttribute:
    
    visibility_dict = {0 : "public",
                       1 : "private",
                       2 : "protected",
                       3 : "implementation"}
    
    
    def __init__(self, cls, attr_dict):
                
        self.my_class = cls       
        self.name = attr_dict["name"]
        self.d_type = attr_dict["type"]        
        self.visibility = self.visibility_dict[attr_dict["visibility"]]  
        
        self.comment = attr_dict["comment"]
        self.value = None
        
        #if value present
        if attr_dict["value"] != "":
            self.value = attr_dict["value"]
            
            
    def print_me(self):
        """A simple print method for debugging purposes.
        """

        print("  ATTRIBUTE {}".format(self))
        print("  Name: {}".format(self.name))
        print("  Data type: {}".format(self.d_type))
        print("  Visibility: {}".format(self.visibility))
        print("  Value: {}".format(self.value))
        print("  ###############")
            
