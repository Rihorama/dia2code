#!/usr/bin/python
import db_text_bank_mysql

class DatabaseGenerator:

    def __init__(self,db_type):
        self.dest_file_name = "mysql1"
        self.txt = db_text_bank_mysql.TextBank()
        self.db_type = db_type                   #MySQL etc.
        
        
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
            
            self.txt.startTable(table)
            #attr_string = ""            
            #constraint_string = ""      #used if needed, e.g. for mysql
            #foreign_string = ""         #for foreign keys if present
            
            
            
            #adding individual rows
            for attr in table.attr_list: 
                
                self.txt.addAttribute(attr)
                
            print self.txt.wrapUpTable()
                
            '''
                s = self.txt.getAttributeString(attr.name,attr.d_type,attr.nullable)
                attr_string = "{}{},\n".format(attr_string,s)            
            
            
                
            #foreign key loop
            for f_key_list in table.f_key_attr_list:  #if there is any
                all_names = ""   #string for all foreign collumn names to be put together for one FK
                FK_table_name = f_key_list[0].my_table.name                
                
                #referenced table can have a multiple-column primary keys
                #f_key_list is now a list of them, we loop over it
                for f_key in f_key_list:
                    
                    #first we add a new attribute that will serve as the foreign key
                    #based on the name of the referenced table and its primary key
                    new_name = "{}_{}".format(f_key.my_table.name,f_key.name)
                    all_names = "{},{}".format(all_names,new_name)
                    
                    #we use the new name we created and data type and nullable flag from the reffed one
                    s = self.txt.getAttributeString(new_name,f_key.d_type,f_key.nullable)
                    attr_string = "{}{},\n".format(attr_string,s)  
                
                #now we'll also add the FOREIGN KEY statement, add it to foreign_string
                #to be printed later
                all_names = all_names[1:] #it always starts with a comma, we cut it off
                f = self.txt.getForeignString(FK_table_name,all_names)
                foreign_string = "{}{},\n".format(foreign_string,f)                
                
            attr_string = attr_string + foreign_string
            
            
            
            #if the db_type requires it (mysql), runs the cycle again to find UNIQUE
            #constraints
            if self.db_type == "mysql":
                for attr in table.attr_list:
                    if attr.unique:
                        c = self.txt.getConstraintString("UNIQUE",attr.name)
                        constraint_string = "{}{},\n".format(constraint_string,c)
                        
                attr_string = attr_string + constraint_string
            
            
            
            #defining primary key
            if (len(table.p_key) != 0): #TODO: deal with primary key absence, either error or fix
                s = self.txt.getPrimaryString(table.p_key)
                attr_string = attr_string + s + "\n"
            '''
            
            
            #wrapping it all together in one table
            #fin = self.txt.getTableString(table.name,attr_string)
            #print fin
        
        
    