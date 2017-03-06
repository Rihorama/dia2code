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
        self.visibility = self.visibility_dict[attr_dict["visibility"]]  
        self.abstract_flag = attr_dict["abstract"]
        self.const_flag = attr_dict["query"]          #apparently "const" is marked as query in dia
        self.static_flag = attr_dict["class_scope"]   #same story, long live logic and self-explanation
        
        self.param_list = attr_dict["parameters"]
        
        self.comment = attr_dict["comment"]

            
    def print_me(self):
        """A simple print method for debugging purposes.
        """

        for i in self.param_list:
            i.print_me()
            
        print("  METHOD {}".format(self))
        print("  Name: {}".format(self.name))
        print("  Data type: {}".format(self.d_type))
        print("  Visibility: {}".format(self.visibility))
        print("  Parameters: {}")
        for i in self.param_list:
            i.print_me()
        print("  ###############")

            
