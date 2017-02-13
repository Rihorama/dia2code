#!/usr/bin/python3

class TextBank:  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
        
        self.cls = None                 #current class
        self.cls_string = ""            #filled with wrapUpClass()
        
        self.private_attr_string = ""      #for private attributes
        self.protected_attr_string = ""    #for protected attrbitues
        self.public_attr_string = ""       #for public attributes
        
        self.private_mtd_string = ""       #for private methods
        self.protected_mtd_string = ""     #for protected methods
        self.public_mtd_string = ""        #for public methods
        
        self.definitions = ""              #definitions of methods with empty body        
         
        
        #--------- FORMAT STRING PATTERNS -----------
        
        # INDENT - set indent for this bank is four spaces
        self.indent = "    "
        
        
        # CLASS PATTERN - main pattern to wrap up the whole class definition
        #               - "class {class_name} {{\n{class_body}}};\n{comment}{method_definitions}\n"
        self.class_format = "class {} {{\n{}{}}};\n{}\n"
        

        # DERIVED CLASS PATTERN -pattern to wrap up derived classes (inherits or implements an interface)
        #                       - "class {class_name}: public {parent_name} {{\n{comment}{class_body}}};\n{method_definitions}\n"
        self.derived_format = "class {}: public {} {{\n{}{}}};\n{}\n"
        
        
        # PRIVATE PATTERN - for private access modifier
        self.private_format = "private:\n{}\n"
        
        
        # PROTECTED PATTERN - for protected access modifier
        self.protected_format = "protected:\n{}\n"
        
        
        # PUBLIC PATTERN - for public access modifier
        self.public_format = "public:\n{}\n" 
        
        
        # ATTRIBUTE PATTERN - for attributes without default value
        #                   - "{data_type} {attr_name};{line_comment}\n"
        self.attribute_format = "{} {};{}\n"
        
        
        # ATTRIBUTE PATTERN WITH DEFAULT VALUE - attributes with default value
        #                   - "{data_type} {attr_name} = {default_value};{line_comment}\n"
        self.attribute_with_default_format = "{} {} = {};{}\n"
        
        
        # METHOD DECLARATION PATTERN - for declaring methods withing a c++ class body
        #                            - "{data_type} {method_name}({parameters});\n"
        self.mtd_declaration_format = "{} {} ({});\n"
        
        # METHOD DEFINITION PATTERN - for defining the declared class outside the class body
        #                           - "{data_type} {class_name}::{method_name}({parameters}){{\n{comment}{body}\n}}"
        self.mtd_definition_format = "\n{} {}::{} ({}) {{\n{}{}\n}}\n\n"
        
        
        # STD::VECTOR PATTERN - for defining vector variables
        #                     - "std::vector<{data_type}> {name}"
        self.vector_format = "std::vector<{}> {}"
        
        
        # INSERT CODE COMMENT - to be put inside empty method definition body
        self.your_code_here_str = "\n// YOUR CODE HERE\n"
        
        
        #LINE COMMENT - two indents, then two slashes and the text
        #                - "// {comment}"
        self.line_comment = "// {}"
        
        
        #MULTI-LINE COMMENT - for class comments, possibly method comments if used in definition part
        #                   - "/* {comment} */\n"
        self.multiline_comment = "/* {} */\n\n"

        
                
    def startClass(self,cls):
        """
        Method that prepares the instance attributes to work on a new
        table and begins the process. Sets variable strings to empty
        strings again, then parses primary key and foreign keys.
        
        Args:
            cls (cls_class.Class): Class instance to work with.
        """
        self.cls = cls
        self.cls_string = ""
        
        self.private_attr_string = ""           
        self.protected_attr_string = ""     
        self.public_attr_string = ""
        
        self.private_mtd_string = ""
        self.protected_mtd_string = ""
        self.public_mtd_string = ""
        
        self.definitions = ""
            
            
        return



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests. Creates needed strings and appends them to their respective
        self.x_string variables.
        
        Args:
            attr (cls_attribute.Attribute): Attribute instance to parse into text.
        """
        
        #COMMENT
        #formating comment if present and adding two indents
        if not attr.comment == "":
            comment = self.line_comment.format(attr.comment)
            comment = "{}{}{}".format(self.indent,self.indent,comment)
        
        else:
            comment = ""
            
            
        
        #ATTRIBUTE ITSELF
        if attr.value == None:
            s = self.attribute_format.format(attr.d_type, attr.name, comment)
        
        #assigning a value if present: "data_type name = value"
        else:
            s = self.attribute_with_default_format.format(attr.d_type, attr.name, attr.value, comment)
        
        
        #adds 2x indent, semicolon and newline
        s = "{}{}{}".format(self.indent,self.indent,s)
        
        
        
        #ACCESS MODIFIER
        #picking the right access modifier string
        #NOTE: So far "Implementation" variant fall under "Public"
        if attr.visibility == "private":
            self.private_attr_string = "{}{}".format(self.private_attr_string,s)
            
        elif attr.visibility == "protected":
            self.protected_attr_string = "{}{}".format(self.protected_attr_string,s)
            
        else:
            self.public_attr_string = "{}{}".format(self.public_attr_string,s)
            
        
        return



    def addMethod(self,mtd):
            """Using attributes of given method, generates two strings: declaration of
            the method which will be added under the proper access modifier
            and the definition of the method with empty body, each stored
            in their respective "group string".
            
            Args:
                mtd (cls_method.Method): Method instance to parse into text.
            """
            
            #PARAMETERS
            #first we generate string with all parameters
            param_str = ""
            
            for param in mtd.param_list:
                s = "{} {},".format(param.d_type,param.name)
                param_str = "{}{}".format(param_str,s)
            
            #removing comma if needed
            if not param_str == "":
                param_str = param_str[:-1]
            
            
            
            #COMMENT
            #formating comment if present and adding two indents
            if not mtd.comment == "":
                comment = self.multiline_comment.format(mtd.comment)
            
            else:
                comment = ""
            
            
            
            #DECLARATION STRING
            s = self.mtd_declaration_format.format(mtd.d_type,mtd.name,param_str)
            
            #adds 2x indent
            s = "{}{}{}".format(self.indent,self.indent,s)
            
            #and put it under the right access modifier
            #NOTE: So far "Implementation" variant fall under "Public"
            if mtd.visibility == "private":
                self.private_mtd_string = "{}{}".format(self.private_mtd_string,s)
                
            elif mtd.visibility == "protected":
                self.protected_mtd_string = "{}{}".format(self.protected_mtd_string,s)
                
            else:
                self.public_mtd_string = "{}{}".format(self.public_mtd_string,s)
                
                
            #DEFINITION STRING
            s = self.mtd_definition_format.format(mtd.d_type,self.cls.name,mtd.name,param_str,
                                                  comment,self.your_code_here_str)
            
            self.definitions = "{}{}".format(self.definitions,s)
            
            
            return
            
            
            
    def addAssociation(self,assoc):
        """Gets an instance of Association and turns it into a proper
        attribute (single value if multiplicity is 1, vector/list for
        variable count of values). Adds the attribute to other private
        attributes.
        
        Args:
            assoc (cls_association.Association) - Association to parse.
        """
        
        #first we determine which member of the association is this class
        #and which member is the other class
        member = assoc.whichMemberIs(self.cls)
        member_dict = None
        
        other = None
        other_dict = None

        
        if member == "A":
            member_dict = assoc.A_dict
            other_dict = assoc.B_dict
            other = "B"
            
        else:
            member_dict = assoc.B_dict
            other_dict = assoc.A_dict
            other = "A"
            
        
        #determining the new attribute name        
        name = None

        if not other_dict["role"] == "": #format: "rolename_othername_association"
            
            role = other_dict["role"]
            role = role.replace(" ","_") #precaution in cae white spaces present, replaces with _
            
            name = "{}_{}_association".format(role,other_dict["class"].name)
            
        else: #we must manage with format: "othername_association"
            name = "{}_association".format(other_dict["class"].name)
            
        
        #this class is "member" and it will have attribute referencing the "other" class
        #thus the multiplicity of the other class matters
        s = ""
        
        if assoc.isSingleMultiplicity(other):
            s = "{} {}".format(other_dict["class"].name, name)
            
        else: #multiple or variable amount of values => vector
            s = self.vector_format.format(other_dict["class"].name, name)
            
        #adds 2x indent, semicolon and newline
        s = "{}{}{};\n".format(self.indent,self.indent,s)
        
        self.private_attr_string = "{}{}".format(self.private_attr_string,s)
        
        #TODO: potentially add these in a separated string and divide by extra \n 
        #      so it looks better in the code


    def wrapUpClass(self):
        """Puts together all stored strings to create a complete class declaration.
        Saves the string in self.table_string and returns it.
            
        Returns:
            Final Class string.
        """
        
        #ACCESS MODIFIERS AND THEIR CONTENT
        private = self.wrapUpPrivate()
        protected = self.wrapUpProtected()
        public = self.wrapUpPublic()
        
        declarations = "{}{}{}".format(private,protected,public)
        
        
        #COMMENT (no indent)
        if not self.cls.comment == "":
            comment = self.multiline_comment.format(self.cls.comment)
        
        else:
            comment = ""
        
        #class inherits from another class
        if self.cls.inherits_flag:
            self.cls_string = self.derived_format.format(self.cls.name,self.cls.inherits.name,
                                                          comment,declarations,self.definitions)
        #class realizes an interface
        elif self.cls.realizes_flag:
            self.cls_string = self.derived_format.format(self.cls.name,self.cls.realizes.name,
                                                          comment,declarations,self.definitions)
        
        #normal class
        else:
            self.cls_string = self.class_format.format(self.cls.name,comment,declarations,self.definitions)
        
        return self.cls_string
    
    
    
    def wrapUpPrivate(self):
        """Puts together private attributes and methods under the
        'private:' label.
            
        Returns:
            Formated self.private_format string with private attributes
            and private method declarations.
        """
        
        private = "{}{}".format(self.private_attr_string,self.private_mtd_string)
        
        #no member under this access modifier
        if private == "":
            return ""
        
        
        #adds indent, formates with the pattern string and returns it
        s = self.private_format.format(private)
        s = "{}{}".format(self.indent,s)
        
        
        return s
    
    
    
    def wrapUpProtected(self):
        """Puts together protected attributes and methods under the
        'protected:' label.
            
        Returns:
            Formated self.protected_format string with protected attributes
            and protected method declarations.
        """
        
        protected = "{}{}".format(self.protected_attr_string,self.protected_mtd_string)
        
        #no member under this access modifier
        if protected == "":
            return ""
        
        
        #adds indent, formates with the pattern string and returns it
        s = self.protected_format.format(protected)
        s = "{}{}".format(self.indent,s)
        
        
        return s
    
    
    
    def wrapUpPublic(self):
        """Puts together public attributes and methods under the
        'public:' label.
            
        Returns:
            Formated self.public_format string with public attributes
            and public method declarations.
        """
        
        public = "{}{}".format(self.public_attr_string,self.public_mtd_string)
        
        #no member under this access modifier
        if public == "":
            return ""
        
        
        #adds indent, formates with the pattern string and returns it
        s = self.public_format.format(public)
        s = "{}{}".format(self.indent,s)
        
        
        return s

    
    
 