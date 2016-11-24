#!/usr/bin/python
import db_text_bank_mysql

class DatabaseGenerator:

    def __init__(self):
        self.dest_file_name = "mysql1"
        self.txt = db_text_bank_mysql.TextBank()
        
        
    def generate(self,table_dict):
        '''
        Takes dictionary of tables and turns them into a proper generating code
        in chosen language.
        '''
    
        #Opens destination file
        #f = open(self.dest_file_name, 'w')
        
        
        #Cycles over tables and adds them to the file
        for i in sorted(table_dict):
            
            table = table_dict[i]            
            attr_string = ""
            
            #adding individual rows
            for attr in table.attr_list:                
                s = self.txt.getAttributeString(attr)
                attr_string = attr_string + s + ",\n"
            
            #defining primary key
            if (table.p_key != None): #TODO: deal with primary key absence, either error or fix
                s = self.txt.getPrimaryString(table.p_key.name)
                attr_string = attr_string + s + "\n"
            
            #wrapping it all together in one table
            fin = self.txt.getTableString(table.name,attr_string)
            print fin
        
        
    