#!/usr/bin/python3

class DbAttribute:
    
    def __init__(self, table, attr_dict):
                
        self.my_table = table       
        self.name = attr_dict['name']
        self.d_type = attr_dict['type']
        
        self.nullable = attr_dict['nullable']    #bool
        self.unique = attr_dict['unique']        #bool
        
        self.comment = attr_dict['comment']
        
        self.p_key_flag = attr_dict['primary_key']    #is primary key flag



    def print_me(self):
        """A simple print method for debugging purposes.
        """
        
        print("  DB ATTRIBUTE {}".format(self))
        print("  My Table: {}".format(self.my.table.name))
        print("  Name: {}".format(self.name))
        print("  Type: {}".format(self.assoc_type))
        print("  Nullable: {}".format(self.nullable))
        print("  Unique: {}".format(self.unique))
        print("  Comment: {}".format(self.comment))
        print("  Primary Key Flag: {}".format(self.p_key_flag))