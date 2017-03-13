#!/usr/bin/python3

from textbanks.databased.db_textbank_mysql      import TextBankMysql
from textbanks.databased.db_textbank_postgresql import TextBankPostgresql

from parents.generator                          import Generator

class DatabaseGenerator(Generator):
    
    supported_language_dict = { "mysql"      : "TextBankMysql()",
                                "postgresql" : "TextBankPostgresql()"}
    
    saving_options_dict = { "t"  : "on_terminal",
                            "f"  : "in_file",
                            "ff" : "in_file"}

    def __init__(self,dest_path,file_name,language,saving_type):
        self.dest_path = dest_path
        self.file_name = file_name
        self.language = language                   #mysql etc.
        self.saving_type = self.saving_options_dict[saving_type]
        
        #instantiating the correct text bank
        self.txt = eval(self.supported_language_dict[language])
        
        
        
    def generate(self,table_dict):
        """Takes dictionary of tables and turns them into a proper generating code
        in chosen language. Then either saves them in given file or prints them
        on terminal. If file option is chosen, adds an extention that equals
        to used language name.
        
        Args:
            table_dict (Dictionary): Dictionary of Table instances.
        """
        
        #gets properly sorted list of tables
        table_list = self.sortTables(table_dict)
        
        #IN FILE
        if self.saving_type == "in_file":
            
            #puts together file path + name
            file_name = "{}{}.{}".format(self.dest_path,self.file_name,self.language)
            
            #Opens destination file
            f = open(file_name, 'w')
            
            
            #Cycles over tables and adds them to the file
            for table in table_list:                
                s = self.generateTable(table)        
                f.write(s)
                
            f.close()            
            
        #ON TERMINAL
        else:
            #Cycles over tables and adds them to the file
            for table in table_list:                
                s = self.generateTable(table)        
                print(s)
                
        return
    
    
    
    def generateTable(self,table):
        """Calls all text_bank methods needed for proper generating
        of one table.
        
        Args:
            table (db_table.Table) - Instance of Table to be generated into code string.
        
        Returns:
            s (String) - Generated code string representing the given table in chosen language.
        """
        
        self.txt.startEntity(table)
                
        #ATTRIBUTES / ROWS
        for attr in table.attr_list: 
            
            self.txt.addAttribute(attr)
            
        
        #FOREIGN KEYS
        for f_key_list in table.f_key_attr_list: 
            
            self.txt.addForeignKey(f_key_list)
        
        
        s = self.txt.wrapUpEntity()
        
        return s
    
    
    
    def sortTables(self,table_dict):
        """Cycles over the table dict (over its hard copy) and in each cycle
        moves specific tables to a newly created list until the dictionary
        is empty. The moved tables are always those that reference
        tables alrady present in the new list (or have no foreign keys).
        This is done to sort the tables in the order that will
        be then valid in the database dump since table x can't reference
        another table y that hasn|t been declared yet.
        
        Args:
            dict (Dictionary): Dictionary of Table instances.
            
        Returns:
            table_list (List): List of Table instances, desirably sorted.
        """
        
        table_list = []
        table_dict = dict(table_dict)
        table_dict_temp = dict(table_dict)
        max_iter = 100
        
        
        for i in range(max_iter):
            
            for t_id in table_dict:
                
                table = table_dict[t_id]
                
                #not referencing tables can be moved right away
                if len(table.f_key_attr_list) == 0:                    
                    table_list.append(table)
                    del table_dict_temp[t_id]
                
                #referencing tables must be checked if their references
                #already present in table_list. If not => ignore for now
                else:
                    flag = True
                    
                    for fk in table.f_key_attr_list:
                        referenced_table = fk[0].my_table
                        
                        if referenced_table not in table_list:
                            flag = False
                            break
                    
                    #all refs in table_list, we can add this table too
                    if flag == True:
                        table_list.append(table)
                        del table_dict_temp[t_id]
                        
            #updating the table_dict
            table_dict = dict(table_dict_temp)
            
            #if the distionary has been emptied => all sorted in list, we finish
            if len(table_dict) == 0:
                break
            
        return table_list
                    
            
