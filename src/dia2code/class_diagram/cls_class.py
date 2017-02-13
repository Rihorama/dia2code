#!/usr/bin/python3


class Class:
    #aList = attributeList
    def __init__(self, class_name, class_id, stereotype, comment):
                        
        self.name = class_name  
        self.id = class_id
        self.stereotype = stereotype           #"" if no stereotype
        
        self.comments_enabled = True
        self.comment = comment                 #"" if no comment
        
        self.attr_list = []
        self.method_list = []
        
        self.association_list = []             #list of Asociation instances this class participates in
        
        #inherits from another class
        self.inherits_flag = False
        self.inherits = None
        
        #depends on another class/classes
        self.depends_flag = False
        self.depends_on_list = []
        
        #realizes an interface
        self.realizes_flag = False
        self.realizes = None
        
        
    def print_me(self):
        """A simple print method for debugging purposes.
        Prints the class name, stereotype, inheritance, dependency
        and realization flags, attributes, methods and also associations
        it participates in.
        """
        
        print("CLASS {}".format(self))
        print("Name: {}".format(self.name))
        print("Class ID: {}".format(self.id))
        print("Stereotype: {}".format(self.stereotype))
        print("Inherits flag: {}".format(self.inherits_flag))
        print("Depends flag: {}".format(self.depends_flag))
        print("Inherits flag: {}".format(self.inherits_flag))
        print("Realizes flag: {}".format(self.realizes_flag))
        print("Atributes:")        
        for attr in self.attr_list:
            attr.print_me()
            
        print("Methods:")        
        for mtd in self.method_list:
            mtd.print_me()
            
        print("Associations:")
        print(self.association_list)
        for assoc in self.association_list:
            assoc.print_me()
            
        print("###########################\n\n")

