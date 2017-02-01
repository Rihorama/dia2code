#!/usr/bin/python3

import db_text_bank_mysql

class DatabaseGenerator:
    
    supported_language_dict = { "mysql" : "db_text_bank_mysql"}
    
    saving_options_dict = { "t"  : "on_terminal",
                            "f"  : "in_file",
                            "ff" : "in_file"}

    def __init__(self,dest_path,file_name,db_type,saving_type):
        self.dest_path = dest_path
        self.file_name = file_name
        self.db_type = db_type                   #MySQL etc.
        self.saving_type = self.saving_options_dict[saving_type]
        self.txt = db_text_bank_mysql.TextBank()
        
        
    def generate(self,table_dict):
        """Takes dictionary of tables and turns them into a proper generating code
        in chosen language. Then either saves them in given file or prints them
        on terminal. If file option is chosen, adds an extention that equals
        to used language name.
        
        Args:
            table_dict (Dictionary): Dictionary of Table instances.
        """
        
        #IN FILE
        if self.saving_type == "in_file":
            
            #puts together file path + name
            file_name = "{}{}.{}".format(self.dest_path,self.file_name,self.db_type)
            
            #Opens destination file
            f = open(file_name, 'w')
            
            
            #Cycles over tables and adds them to the file
            for i in sorted(table_dict):
                
                table = table_dict[i]
                self.txt.startTable(table)
                
                #adding individual rows
                for attr in table.attr_list: 
                    
                    self.txt.addAttribute(attr)
                    
                s = self.txt.wrapUpTable()
        
                f.write(s)
                
            f.close()
            
            
        #ON TERMINAL
        else:
            #Cycles over tables and adds them to the file
            for i in sorted(table_dict):
                
                table = table_dict[i]
                self.txt.startTable(table)
                
                #adding individual rows
                for attr in table.attr_list: 
                    
                    self.txt.addAttribute(attr)
                    
                s = self.txt.wrapUpTable()
        
                print(s)
                
        return
            
