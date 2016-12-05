#!/usr/bin/python
import db_text_bank_mysql

class DatabaseGenerator:

    def __init__(self,db_type):
        self.dest_file_name = "mysql1"
        self.txt = db_text_bank_mysql.TextBank()
        self.db_type = db_type                   #MySQL etc.
        
        
    def generate(self,table_dict):
        """Takes dictionary of tables and turns them into a proper generating code
        in chosen language.
        
        Args:
            table_dict (Dictionary): Dictionary of Table instances.
        """
    
        #Opens destination file
        #f = open(self.dest_file_name, 'w')
        
        
        #Cycles over tables and adds them to the file
        for i in sorted(table_dict):
            
            table = table_dict[i]  
            
            self.txt.startTable(table)
            #attr_string = ""            
            #constraint_string = ""      #used if needed, e.g. for mysql
            #foreign_string = ""         #for foreign keys if present
            
            
            
            #adding individual rows
            for attr in table.attr_list: 
                
                self.txt.addAttribute(attr)
                
            print self.txt.wrapUpTable()
