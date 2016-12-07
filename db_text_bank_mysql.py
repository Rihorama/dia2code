#!/usr/bin/python3

class TextBank:  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
        
        self.indent = "    " #four spaces
        self.table_format = "CREATE TABLE {} (\n{}\n)\n"
        self.primary_format = self.indent + "PRIMARY KEY ({})"
        self.constraint_format = self.indent + "CREATE CONSTRAINT {} {} ({})"
        self.foreign_format = self.indent + "FOREIGN KEY {} ({}) REFERENCES {}({})"
        
        self.table = None
        self.table_string = ""          #filled with wrapUpTable()
        
        self.attr_string = ""           #to accumulate attribute definitions
        self.constraint_string = ""     #for constraints
        self.foreign_string = ""        #for foreign keys
        self.primary_string = ""        #for primary key
        self.fk_attributes = ""         #attributes to accomodate foreign key connection
        
        
        
    def startTable(self,table):
        """
        Method that prepares the instance attributes to work on a new
        table and begins the process. Sets variable strings to empty
        strings again, then parses primary key and foreign keys.
        
        Args:
            table (Table): Table instance to work with.
        """
        self.table = table
        
        self.attr_string = ""           
        self.constraint_string = ""     
        self.foreign_string = ""        
        self.primary_string = ""
        self.fk_attributes = ""
        
        
        #primary key
        if (len(table.p_key) != 0): #TODO: deal with primary key absence, either error or fix
            self.primary_string = self.getPrimaryString(table.p_key)
            
            
        #foreign keys
        for f_key_list in table.f_key_attr_list:  #if there is any
            here_names = ""       #string for all foreign collumn names to be put together for one FK
            foreign_names = ""   #string for names of attributes that are referenced by this FK
            reffed_table_name = f_key_list[0].my_table.name                
            
            #referenced table can have a multiple-column primary keys
            #f_key_list is now a list of them, we loop over it
            for f_key in f_key_list:
                
                #first we add a new attribute that will serve as the foreign key
                #based on the name of the referenced table and its primary key
                new_name = "{}_{}".format(f_key.my_table.name,f_key.name)
                here_names = "{},{}".format(here_names,new_name)          #attributes in child table
                foreign_names = "{},{}".format(foreign_names,f_key.name) #referenced attributes
                
                #we use the new name we created and data type and nullable flag from the reffed one
                s = self.getAttributeString(new_name,f_key.d_type,f_key.nullable)
                self.fk_attributes = "{}{},\n".format(self.fk_attributes,s)  
            
            #now we'll also add the FOREIGN KEY statement, add it to foreign_string
            #to be printed later
            here_names = here_names[1:]    #it always starts with a comma, we cut it off
            foreign_names = foreign_names[1:] #same story
            s = self.getForeignString(here_names,reffed_table_name,foreign_names)
            self.foreign_string = "{}{},\n".format(self.foreign_string,s)
            
        return



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests. Creates needed strings and adds them to their respective
        self.x_string variables.
        
        Args:
            attr (Attribute): Attribute instance to parse into text.
        """
        
        #ROW DECLARATION (name, data type, not null if neccessary - provided by getAttributeString)
        s = self.getAttributeString(attr.name,attr.d_type,attr.nullable)
        self.attr_string = "{}{},\n".format(self.attr_string,s)
        
        
        #UNIQUE CONSTRAINT if present and not for primary key (included in being primary key)
        if attr.unique and not attr.p_key_flag:
            s = self.getConstraintString("UNIQUE",attr.name)
            self.constraint_string = "{}{},\n".format(self.constraint_string,s)



    def wrapUpTable(self):
        """Puts together all stored strings to create a CREATE statement for the whole
        table. Saves the string in self.table_string and returns it.
            
        Returns:
            Final CREATE TABLE string.
        """
        self.attr_string = "{}{}".format(self.attr_string,self.fk_attributes)
        s = "{}{}{}{}".format(self.attr_string,self.constraint_string,self. \
                              foreign_string,self.primary_string)
        self.table_string = self.table_format.format(self.table.name,s)
        
        return self.table_string

    
    
    def getAttributeString(self,name,d_type,nullable):
        """Uses elements stored in attribute dictionary to create
        a string defining one column of the table.
        
        NOTE: Does not include either comma or \n at the end. Must be added
        manually if needed.
        
        Args:
            name     (String):  Attribute name.
            d_type   (String):  Attribute data type.
            nullable (Boolean): Can-be-null flag.
            
        Returns:
            Formated string.
        """
  
        s = self.indent + name + " " + d_type
        
        if not nullable:
            s = s + " " + "NOT NULL"
            
        return s
    
    
    def getPrimaryString(self,p_key):
        """Creates a primary key definition for the row of given name.
        No comma or \n at the end.
        
        Args:
            p_key (List): List of primary key attributes. 
            
        Returns:
            Formated string.
        """

        names = p_key[0].name #one will 
        
        #if primary key consists of more rows
        for i in p_key[1:]:
            names = "{},{}".format(names,i.name)
        
        s = self.indent + "PRIMARY KEY ({})".format(names)
        
        return s
    
    
    def getConstraintString(self,constraint,name):
        """Creates a constraint string for row of the given name.
        
        Args:
            constraint (String): Constraint type.
            name       (String): Name of the constrained attribute.
            
        Returns:
            Formated string.
        """
        
        constraint_name = "{}_{}".format(name,constraint.lower())
        s = self.constraint_format.format(constraint_name,constraint,name)
        
        return s
    
    
    def getForeignString(self,here_attr, for_table, for_attr):
        """Creates a string for a foreign key of name referencing
        for_attr attribute in table for_table.
        
        Args:
            here_attr (Attribute): Attribute becoming a foreign key.
            for_table (Table):     Referenced table.
            for_attr  (Attribute): PK of the referenced table.            
            
        Returns:
            Formated string.
        """
        
        name = "fk_{}".format(for_table) #the foreign key will be named "fk_FKTableName"
        s = self.foreign_format.format(name,here_attr,for_table,for_attr)
        
        return s
            
        
        
        