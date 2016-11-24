#!/usr/bin/python

class TextBank:  
    
    def __init__(self):
        
        self.indent = "    " #four spaces
        
    def getTableString(self,name, attr_string):
        '''
        Uses given strings to create a formated string, wrapping the whole
        table creation:
        
        CREATE TABLE name (
        attr_string
        )
        '''
        
        s = "CREATE TABLE {} (\n{})\n".format(name, attr_string)
        
        return s
    
    
    def getAttributeString(self,attribute):
        '''
        Uses elements stored in attribute dictionary to create
        a string defining one column of the table.
        
        NOTE:Does not include either comma or \n at the end. Must be added
        manually if needed.
        '''
  
        s = self.indent + attribute.name + " " + attribute.d_type
        
        if not attribute.nullable:
            s = s + " " + "NOT NULL"
            
        return s
    
    
    def getPrimaryString(self,name):
        '''
        Creates a primary key definition for the row of given name.
        No comma or \n at the end.
        '''
        
        s = self.indent + "PRIMARY KEY ({})".format(name)
        
        return s
        
        
            
        
        
        