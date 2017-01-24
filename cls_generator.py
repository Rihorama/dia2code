#!/usr/bin/python3

import cls_text_bank_cpp

class ClassGenerator:
    
    saving_options_dict = { 0 : "all_in_one_file",
                            1 : "one_file_per_class"}

    def __init__(self,cls_type,saving_type):
        self.dest_file_name = "cpp"
        self.txt = cls_text_bank_cpp.TextBank()
        self.cls_type = cls_type         #programming language used.
        self.saving_type = self.saving_options_dict[saving_type]
        
        
    def generate(self,class_dict):
        """Takes dictionary of classes and turns them into a proper generating code
        in chosen language.
        
        Args:
            class_dict (Dictionary): Dictionary of Class instances.
        """
    
        #Opens destination file
        #f = open(self.dest_file_name, 'w')
        
        
        #Cycles over tables and adds them to the file
        for i in sorted(class_dict):
            
            cls = class_dict[i]
            
            self.txt.startClass(cls)
            
            for attr in cls.attr_list:
                self.txt.addAttribute(attr)
                
            s = self.txt.wrapUpClass()
            
            print(s)
            
            
