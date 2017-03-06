#!/usr/bin/python3

class ClsAttribute:
    
    visibility_dict = {0 : "public",
                       1 : "private",
                       2 : "protected",
                       3 : "implementation"}
    
    
    def __init__(self, cls, attr_dict):
        #attr_dict keys are equal to element names in the dia XML
                
        self.my_class = cls       
        self.name = attr_dict["name"]
        self.d_type = attr_dict["type"]        
        self.visibility = self.visibility_dict[attr_dict["visibility"]] 
        self.abstract_flag = attr_dict["abstract"]
        self.static_flag = attr_dict["class_scope"]   #static is marked as "class_scope" in dia
        
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
            
