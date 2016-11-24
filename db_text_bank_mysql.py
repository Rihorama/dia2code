#!/usr/bin/python

class TextBank:  
    #TODO: deal with possibility of wrong parameter coming...?
    
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
    
    
    def getAttributeString(self,name,d_type,nullable):
        '''
        Uses elements stored in attribute dictionary to create
        a string defining one column of the table.
        
        NOTE:Does not include either comma or \n at the end. Must be added
        manually if needed.
        '''
  
        s = self.indent + name + " " + d_type
        
        if not nullable:
            s = s + " " + "NOT NULL"
            
        return s
    
    
    def getPrimaryString(self,p_key):
        '''
        Creates a primary key definition for the row of given name.
        No comma or \n at the end.
        '''

        names = p_key[0].name #one will 
        
        #if primary key consists of more rows
        for i in p_key[1:]:
            names = "{},{}".format(names,i.name)
        
        s = self.indent + "PRIMARY KEY ({})".format(names)
        
        return s
    
    
    def getConstraintString(self,constraint,name):
        '''
        Creates a constraint string for row of the given name.
        '''
        
        constraint_name = "{}_{}".format(name,constraint.lower())
        s = "{}CREATE CONSTRAINT {} {} ({})"
        s = s.format(self.indent,constraint_name,constraint.upper(),name)
        
        return s
    
    
    def getForeignString(self,for_table, for_attr):
        '''
        Creates a string for a foreign key of name referencing
        for_attr attribute in table for_table.
        '''
        
        name = "fk_{}".format(for_table) #the foreign key will be named "fk_FKTableName"
        s = "{}FOREIGN KEY ({}) REFERENCES {}({})".format(self.indent,name,for_table,for_attr)
        
        return s
            
        
        
        