#!/usr/bin/python3

class DbAttribute:
    
    def __init__(self, table, attr_dict):
                
        self.my_table = table       
        self.name = attr_dict['name']
        self.d_type = attr_dict['type']
        
        self.nullable = attr_dict['nullable']    #bool
        self.unique = attr_dict['unique']        #bool
        
        self.comment = attr_dict['comment']
        
        self.p_key_flag = attr_dict['primary_key']    #primary key flag
