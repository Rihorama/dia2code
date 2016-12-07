#!/usr/bin/python3


class Class:
    #aList = attributeList
    def __init__(self, class_name, class_id, stereotype):
                        
        self.name = class_name  
        self.id = class_id
        self.stereotype = stereotype                 #empty if no stereotype
        
        self.attr_list = []
        self.method_list = []
