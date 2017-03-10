#!/usr/bin/python3

from textbanks.classd.cls_textbank_cpp    import TextBankCpp
from textbanks.classd.cls_textbank_python import TextBankPython

class ClassGenerator:
    
    supported_language_dict = {"c++"    : "TextBankCpp()",
                               "python" : "TextBankPython()"}
    
    extension_dict = {"c++"    : "cpp",
                      "python" : "py"}
    
    saving_options_dict = { "t"  : "on_terminal",
                            "f"  : "in_one_file",
                            "ff" : "one_class_per_file"}

    def __init__(self,dest_path,file_name,language,saving_type):
        
        self.dest_path = dest_path
        self.file_name = file_name
        self.language = language  #file extension - equals to programming language used
        self.cls_extension = self.extension_dict[language]
        self.saving_type = self.saving_options_dict[saving_type]
        
        #instantiating the correct text bank
        self.txt = eval(self.supported_language_dict[language])
        
        
        
    def generate(self,class_dict):
        """Takes a dictionary of classes and turns them into a proper generating code
        in chosen language. Those are then processed as chosen by the user: either
        printed on terminal, saved in one file or each class is saved in its own file.
        
        Args:
            class_dict (Dictionary): Dictionary of Class instances.
        """
    
        #Opens destination file
        #f = open(self.dest_file_name, 'w')
        
        #ONE CLASS PER FILE
        if self.saving_type == "one_class_per_file":
            
            #Cycles over tables and each of them goes in its own file
            for i in sorted(class_dict):
                
                cls = class_dict[i]
                file_name = "{}{}_{}.{}".format(self.dest_path,self.file_name,
                                                cls.name,self.cls_extension)                
                #creates the file
                f = open(file_name, 'w')
                               
                s = self.generateClass(cls)
                
                f.write(s)
                f.close()
                
                #print(s)
                
        
        #ALL IN ONE FILE
        elif self.saving_type == "in_one_file":  
            
            file_name = "{}{}.{}".format(self.dest_path,self.file_name,self.cls_extension)
            
            #creates the file
            f = open(file_name, 'w')
        
            #Cycles over tables and adds them to the file
            for i in sorted(class_dict):
                
                cls = class_dict[i]
                s = self.generateClass(cls)
                
                f.write(s)
 
            f.close()
         
        #PRINT ON TERMINAL
        else:             
            #Cycles over tables and prints them in the terminal
            for i in sorted(class_dict):
                
                cls = class_dict[i]                
                s = self.generateClass(cls)

                print(s)
                
                
                
    def generateClass(self,cls):
        """Calls all text_bank methods needed for proper generating
        of one class.
        
        Args:
            cls (cls_class.Class) - Instance of Class to be generated into code string.
        
        Returns:
            s (String) - Generated code string representing the given class in chosen language.
        """
        
        #initiates string generating
        self.txt.startEntity(cls)
        
        #generates attributes
        for attr in cls.attr_list:
            self.txt.addAttribute(attr)
            
        #generates attributes from associations
        for assoc in cls.association_list:
            self.txt.addAssociation(assoc)
        
        #generates methods
        for mtd in cls.method_list:
            self.txt.addMethod(mtd)
        
        #gets the final string
        s = self.txt.wrapUpEntity()
        
        
        return s
                
