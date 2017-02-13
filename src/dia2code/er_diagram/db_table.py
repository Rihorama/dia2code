#!/usr/bin/python3

import er_diagram.db_attribute


class Table:
    #aList = attributeList
    def __init__(self, table_name, table_id, comment):
                        
        self.name = table_name  
        self.id = table_id
        self.comment = comment
        
        self.p_key = []                 #primary key attribute
        
        self.is_f_key_cnt = 0           #is foreign key flag (cnt)
        self.referenced_by = []         #list for tables that reference
                                        #this table
        
        self.f_key_cnt = 0              #how many foreign keys does this table have
                                        #NOTE: one foreign key can consist of more columns
                                        #of the referenced table!
        self.f_key_attr_list = []       #list of links to foreign key attrs
        
        self.attr_list = []

        
        
        
    def add_slave(self, by_table):
        """Adds info that this table is referenced by
        another table. Updates is_f_key_cnt and
        referenced_by attributes.
        
        Args:
            by_table (Table): Table that references this table.
        """
        
        self.is_f_key_cnt =+ 1 
        self.referenced_by.append(by_table)
        
        return
        
        
        
    def add_foreign_key(self, master):
        """Creates a foreign key referencing the given master table.
        Updates this table's attr_list with the new attribute
        and updates f_key_cnt and f_key_attr_list variables.
        
        Args:
            master (Table): Table that is referenced by this table.
        """
        
        #NOTE: appends a LIST of primary key collumns
        self.f_key_attr_list.append(master.p_key)
        self.f_key_cnt =+ 1
        
        return
