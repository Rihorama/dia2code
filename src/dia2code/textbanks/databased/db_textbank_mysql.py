#!/usr/bin/python3
from parents.db_textbank import DatabaseTextBank

class TextBankMysql(DatabaseTextBank):  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
                
        self.table = None
        self.fk_cnt = 0                 #counter of foreign keys to ensure unique fk name
        self.table_string = ""          #filled with wrapUpTable()
        
        self.attr_string = ""           #to accumulate attribute definitions
        self.constraint_string = ""     #for constraints
        self.foreign_string = ""        #for foreign keys
        self.primary_string = ""        #for primary key
        self.fk_attributes = ""         #attributes to accomodate foreign key connection
        
        
        #--------- FORMAT STRING PATTERNS -----------
        
        # INDENT - set indent for this bank is four spaces
        self.indent = "    " #four spaces
        
        
        # TABLE PATTERN - main pattern to wrap up the whole table
        #               - "CREATE TABLE {name} (\n{comment}{body}\n);\n"
        self.table_format = "CREATE TABLE {} (\n{}{});\n\n"
        
        
        # ATTRIBUTE - not_null and comment might not be present -> ""
        #           - "{name} {data_type}{not_null}{comment}"
        self.attribute_format = "{} {}{}{},\n"
        
        
        # PRIMARY KEY PATTERN - for the primary key defining, comes last so no comma
        #                     - "PRIMARY KEY ({name})"
        self.primary_format = "PRIMARY KEY ({})\n"
        
        
        # CONSTRAINT FORMAT - for constraints defining
        #                   - "CONSTRAINT {constraint_name} {constraint_type} ({constrained_attribute_name})"           - 
        self.constraint_format = "CONSTRAINT {} {} ({}),\n"
        
        
        # FOREIGN KEY PATTERN - for foreign key defining
        #                     - "FOREIGN KEY {unique_fk_name} ({attr_that_is_fk}) REFERENCES {referenced_table}({referenced_attr})"
        self.foreign_format = "FOREIGN KEY {} ({}) REFERENCES {}({}),\n"
        
        
        # UNIQUE PATTERN - for UNIQUE constraints
        #                - "UNIQUE ({attr_that_is_fk})"
        self.unique_format = "UNIQUE ({}),\n"
        
        
        # FOREIGN KEY PATTERN - for foreign key defining
        #                     - "FOREIGN KEY {unique_fk_name} ({attr_that_is_fk}) REFERENCES {referenced_table}({referenced_attr})"
        self.foreign_format = "FOREIGN KEY {} ({}) REFERENCES {}({}),\n"
        
        
        # NOT NULL
        self.not_null = " NOT NULL"
        
        
        # ATTRIBUTE COMMENT - built in attribute comment
        #                   - "COMMENT '{comment}'"
        self.attr_comment_format = " COMMENT '{}'"
        
        
        # MULTILINE COMMENT - for comments of tables
        #                   - "/*\n{comment}\n*/\n"
        self.multiline_comment_format = "/*\n{}\n*/\n"
        
        
        
        
    def startEntity(self,table):
        """
        Method that prepares the instance attributes to work on a new
        table and begins the process. Sets variable strings to empty
        strings again, then also parses primary key.
        
        Args:
            table (db_table.Table): Table instance to work with.
        """
        self.table = table
        self.fk_cnt = 0
        
        self.attr_string = ""           
        self.constraint_string = ""     
        self.foreign_string = ""        
        self.primary_string = ""
        self.fk_attributes = ""
        
        
        #primary key
        if (len(table.p_key) != 0): #TODO: deal with primary key absence, either error or fix
            self.primary_string = self.getPrimaryString(table.p_key)
            
        
        return        



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests. Creates needed strings and adds them to their respective
        self.x_string variables.
        
        Args:
            attr (db_attribute.Attribute): Attribute instance to parse into text.
        """
        
        #ROW DECLARATION (name, data type, not null if neccessary - provided by getAttributeString)
        s = self.getAttributeString(attr.name,attr.d_type,attr.nullable,attr.comment)
        self.attr_string = "{}{}".format(self.attr_string,s)
        
        
        #UNIQUE CONSTRAINT if present and not for primary key (included in being primary key)
        if attr.unique and not attr.p_key_flag:
            #s = self.getConstraintString("UNIQUE",attr.name)
            #self.constraint_string = "{}{}".format(self.constraint_string,s)
            
            #rather using pure UNIQUE () format
            s = self.unique_format.format(attr.name)
            s = "{}{}".format(self.indent,s)
            self.constraint_string = "{}{}".format(self.constraint_string,s)
            
            
            
    def addForeignKey(self,f_key_list):
        """Takes the given list that contains one or more foreign attributes that are the primary
        key of the referenced table. Creates the requested number of new attributes to hold
        the reference and adds them to already parsed attributes. Generates an in-class unique name
        for the new foreign key and then uses it to generate the foreign key definition string.
        Adds it to other fk strings we have so far concatenated in self.foreign_string. 
        
        Args:
            f_key_list (List): List of db_attribute.Attribute instances that are to be referenced.
        """
        
        self.fk_cnt += 1     #increments the counter
        here_names = ""      #string for all foreign collumn names to be put together for one FK
        foreign_names = ""   #string for names of attributes that are referenced by this FK
        reffed_table_name = f_key_list[0].my_table.name      #name of the referenced table   
        
        
        #referenced table can have a multiple-column primary keys
        #f_key_list is now a list of them, we loop over it
        for f_key in f_key_list:            
            
            #first we add a new attribute that will serve as the foreign key
            #based on the name of the referenced table and its primary key
            #also adds the counter to ensure unique attributes
            new_name = "{}_{}_fk{}".format(f_key.my_table.name,f_key.name,self.fk_cnt)
            here_names = "{},{}".format(here_names,new_name)          #attributes in child table
            foreign_names = "{},{}".format(foreign_names,f_key.name)  #referenced attributes            
            
            #we use the new name we created and data type from the reffed one,
            #true for nullable (since we can't determine) and no comment
            nullable = True
            s = self.getAttributeString(new_name,f_key.d_type,nullable,"")
            self.fk_attributes = "{}{}".format(self.fk_attributes,s)  
        
        
        #now we'll also add the FOREIGN KEY statement, add it to foreign_string
        #to be printed later
        here_names = here_names[1:]    #it always starts with a comma, we cut it off
        foreign_names = foreign_names[1:] #same story
        s = self.getForeignString(here_names,reffed_table_name,foreign_names)
        self.foreign_string = "{}{}".format(self.foreign_string,s)
        
        
        return



    def wrapUpEntity(self):
        """Puts together all stored strings to create a CREATE statement for the whole
        table. Saves the string in self.table_string and returns it.
            
        Returns:
            Final CREATE TABLE string.
        """
        
        comment = ""
        
        #COMMENT
        if not self.table.comment == "":
            comment = self.multiline_comment_format.format(self.table.comment)
        
        #ALL TOGETHER
        self.attr_string = "{}{}".format(self.attr_string,self.fk_attributes)
        s = "{}{}{}{}".format(self.attr_string,self.constraint_string,self. \
                              foreign_string,self.primary_string)
        
        #check if s doesn't end with ",\n" (it means no primary key but let everyone get
        #what they want)
        if s[-2:] == ",\n":
            s = "{}\n".format(s[:-2])
        
        self.table_string = self.table_format.format(self.table.name,comment,s)
        
        return self.table_string

    
    
    def getAttributeString(self,name,d_type,nullable,comment):
        """Uses elements stored in attribute dictionary to create
        a string defining one column of the table.
        
        Args:
            name     (String):  Attribute name.
            d_type   (String):  Attribute data type.
            nullable (Boolean): Can-be-null flag.
            comment  (String): Comment of the given attribute
            
        Returns:
            Formated string.
        """
        
        not_null = ""
        new_comment = ""
        
        #NOT NULL
        if not nullable:
            not_null = self.not_null            
            
        #COMMENT
        if not comment == "":
            new_comment = self.attr_comment_format.format(comment)    
            
        
        
        s = self.attribute_format.format(name,d_type,not_null,new_comment)
        s = "{}{}".format(self.indent,s)

            
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
        
        s = self.primary_format.format(names)
        s = "{}{}".format(self.indent,s)
        
        return s
    
    
    def getConstraintString(self,constraint_type,attr_name):
        """Creates a constraint string for row of the given name.
        
        Args:
            constraint_type (String): Constraint type.
            attr_name       (String): Name of the constrained attribute.
            
        Returns:
            Formated string.
        """
        
        constraint_name = "{}_{}".format(attr_name,constraint_type.lower())
        s = self.constraint_format.format(constraint_name,constraint_type,attr_name)
        
        #adding indent
        s = "{}{}".format(self.indent,s)
        
        return s
    
    
    def getForeignString(self,here_attr, for_table, for_attr):
        """Creates a string for a foreign key of name referencing
        for_attr attribute in table for_table.
        
        Args:
            here_attr (db_attrbitue.Attribute): Attribute becoming a foreign key.
            for_table (db_table.Table):         Referenced table.
            for_attr  (db_attribute.Attribute): PK of the referenced table.            
            
        Returns:
            Formated string.
        """
        
        #the foreign key will be named "fk{unique number}__{ThisTableName}_{FKTableName}"
        name = "fk{}__{}_{}".format(self.fk_cnt,self.table.name,for_table)
        
        s = self.foreign_format.format(name,here_attr,for_table,for_attr)
        
        #adding indent
        s = "{}{}".format(self.indent,s)
        
        
        return s
            
        
        
        