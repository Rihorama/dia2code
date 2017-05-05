#!/usr/bin/python3
from parents.cls_textbank import ClassTextBank

class TextBankCpp(ClassTextBank):  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
        
        self.cls = None                 #current class
        self.cls_string = ""            #filled with wrapUpEntity()
        
        self.private_attr_string = ""      #for private attributes
        self.protected_attr_string = ""    #for protected attrbitues
        self.public_attr_string = ""       #for public attributes
        
        self.private_mtd_string = ""       #for private methods
        self.protected_mtd_string = ""     #for protected methods
        self.public_mtd_string = ""        #for public methods
        
        self.definitions = ""              #definitions of methods with empty body
        
        self.param_comments = ""           #help variable to store parameter comments

         
        
        #--------- FORMAT STRING PATTERNS -----------
        
        # INDENT - set indent for this bank is four spaces
        self.indent = "    "
        
        
        # CLASS PATTERN - main pattern to wrap up the whole class definition
        #               - "class {class_name} {{\n{comment}{class_body}}};\n{method_definitions}\n"
        self.class_format = "class {} {{\n{}{}}};\n{}\n"
        

        # DERIVED CLASS PATTERN -pattern to wrap up derived classes (inherits or implements an interface)
        #                       - "class {class_name}: {parent_names} {{\n{comment}{class_body}}};\n{method_definitions}\n"
        self.derived_format = "class {}:{} {{\n{}{}}};\n{}\n"
        
        
        # PRIVATE PATTERN - for private access modifier
        self.private_format = "private:\n{}\n"
        
        
        # PROTECTED PATTERN - for protected access modifier
        self.protected_format = "protected:\n{}\n"
        
        
        # PUBLIC PATTERN - for public access modifier
        self.public_format = "public:\n{}\n" 
        
        
        # ATTRIBUTE PATTERN - for attributes without default value
        #                   - "{[static]}{data_type} {attr_name};{line_comment}\n"
        self.attribute_format = "{}{} {};{}\n"
        
        
        # ATTRIBUTE PATTERN WITH DEFAULT VALUE - attributes with default value
        #                   - "{[static]}{data_type} {attr_name} = {default_value};{line_comment}\n"
        self.attribute_with_default_format = "{}{} {} = {};{}\n"
        
        
        # METHOD DECLARATION PATTERN - for declaring methods withing a c++ class body
        #                            - "{[static]}{data_type }{method_name}({parameters}){[const]};{line_comment}\n"
        self.mtd_declaration_format = "{}{}{}({}){};{}\n"
        
        
        # METHOD DEFINITION PATTERN - for defining the declared class outside the class body
        #                           - "{data_type }{class_name}::{method_name}({parameters}){{\n{[multiline_comment]}\n{body}\n}}"
        self.mtd_definition_format = "\n{}{}::{}({}) {{\n{}{}\n}}\n\n"
        
        
        # VIRTUAL METHOD DECLARATION PATTERN - for declaring pure virtual methods
        #                            - "{[virtual]}{data_type }{method_name}({parameters}){[const]} = 0;{line_comment}\n"
        self.virtual_mtd_declaration_format = "{}{}{}({}){} = 0;{}\n"
        
        
        # STD::VECTOR PATTERN - for defining vector variables
        #                     - "std::vector<{data_type}> {name};\n"
        self.vector_format = "std::vector<{}> {};\n"
        
        
        # INSERT CODE COMMENT - to be put inside empty method definition body
        self.your_code_here_str = "\n// YOUR CODE HERE\n\n"
        
        
        #LINE COMMENT - two indents, then two slashes and the text
        #                - "// {comment}"
        self.line_comment = "// {}"
        
        
        #MULTI-LINE COMMENT - for class comments, possibly method comments if used in definition part
        #                   - "/* {comment} */\n"
        self.multiline_comment = "/* {} */\n\n"
        
        #PARAMETER COMMENT - for individual method parameter comments so they can be added in method description.
        #                   - "{data_type} {name} - {comment}\n"
        self.parameter_comment = "{} {} - {}\n"

        
                
    def startEntity(self,cls):
        """
        Method that prepares this instance attributes to work on a new
        class. Sets variable strings to empty strings again.
        
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
        
        indent_lvl = 2
        indent_here = self.indent * indent_lvl
         
        
        
        #COMMENT
        #formating comment if present and adding two indents
        if not attr.comment == "":
            comment = self.line_comment.format(attr.comment)
            comment = "{}{}".format(indent_here,comment)
        
        else:
            comment = ""
            
        
        #STATIC prefix
        static = ""
            
        if attr.static_flag:
            static = "static "
        
        
        #ATTRIBUTE ITSELF
        if attr.value == None:
            s = self.attribute_format.format(static,attr.d_type, attr.name, comment)
        
        #assigning a value if present: "data_type name = value"
        else:
            s = self.attribute_with_default_format.format(static,attr.d_type, attr.name, attr.value, comment)
        
        
        #adds 2x indent
        s = "{}{}".format(indent_here,s)        
        
        
        #ACCESS MODIFIER
        #and put it under the right access modifier with "attr" = attribute switch
        self.sortUnderAccessModifier(attr.visibility,"attr",s)
            
        
        return



    def addMethod(self,mtd):
        """Using parameters of given method, generates two strings: declaration of
        the method which will be added under the proper access modifier
        and the definition of the method with empty body, each stored
        in their respective "group string".
        
        Args:
            mtd (cls_method.Method): Method instance to parse into text.
        """
        
        #INDENT LEVEL
        indent_lvl = 2
        indent_here = self.indent * indent_lvl        
        
        
        #PARAMETERS
        #first we generate string with all parameters
        param_str = self.getParameters(mtd)
        
        #were any parameter comments present?
        if not self.param_comments == "":
            #wrapping it with a multiline comment
            self.param_comments = self.multiline_comment.format(self.param_comments)
        
        
        
        #COMMENT
        #formating comment if present and adding two indents, uses line comment format
        if not mtd.comment == "":
            comment = self.line_comment.format(mtd.comment)
            comment = "{}{}".format(self.indent,comment)  #adds one indentation
        
        else:
            comment = ""        
  
  
        #STATIC and CONST
        static = ""
        
        if mtd.static_flag:
            static = "static "
             
        const = ""
        
        if mtd.const_flag:
            const = " const"
        
        
        #DATA TYPE - adding a space if present
        d_type = ""
        
        if mtd.d_type:
            d_type = mtd.d_type + " "
            
        
        #DECLARATION STRING  
        s = ""             #for the final string
        
        #VIRTUAL (if present together with static, virtual has priority)
        if mtd.abstract_flag:
            virtual = "virtual "
            s = self.virtual_mtd_declaration_format.format(virtual,d_type,mtd.name,
                                                           param_str,const,comment)            
        #OR NOT
        else:
            s = self.mtd_declaration_format.format(static,d_type,mtd.name,
                                                   param_str,const,comment)
        
        
        #adds 2x indent
        s = "{}{}".format(indent_here,s)
        
        
        #ACCESS MODIFIER
        #and put it under the right access modifier with "mtd" = method switch
        self.sortUnderAccessModifier(mtd.visibility,"mtd",s)
            
            
        #DEFINITION STRING (only for non virtual methods)
        if not mtd.abstract_flag:
            
            s = self.mtd_definition_format.format(d_type,self.cls.name,mtd.name,param_str,
                                                    self.param_comments, self.your_code_here_str)            
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
        
        #INDENT LEVEL
        indent_lvl = 2
        indent_here = self.indent * indent_lvl
        
        
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
            
        
        #NEW ATTRIBUTE NAME        
        name = None
        
        #using the other table's role if it was named in the association
        if not other_dict["role"] == "": #format: "rolename_othername_association"
            
            role = other_dict["role"]
            role = role.replace(" ","_") #precaution in cae white spaces present, replaces with _
            
            name = "{}_{}_association".format(role,other_dict["class"].name)
            
        else: #we must manage with format: "othername_association"
            name = "{}_association".format(other_dict["class"].name)
            
        
        
        #this class is the "member" class and it will have attribute referencing the "other" class
        #thus the multiplicity of the other class matters
        s = ""
        
        if assoc.isSingleMultiplicity(other): #new attribute with no static prefix and no comment
            s = self.attribute_format.format("",other_dict["class"].name,
                                             name,"")
            #s = "{} {}".format(other_dict["class"].name, name)
            
        else: #multiple or variable amount of values => vector
            s = self.vector_format.format(other_dict["class"].name, name)
        
        
        
        #adds 2x indent, semicolon and newline
        s = "{}{}".format(indent_here,s)        
        
        
        #these go under private access modifier by default
        self.private_attr_string = "{}{}".format(self.private_attr_string,s)
        
        
        
        #TODO: potentially add these in a separated string and divide by extra \n 
        #      so it looks better in the code
        
        
        
    def getParentString(self,cls):
        """Goes through all classes this class inherits from and puts them
        in one string that is to be inserted in the class header.
        
        Returns:
            String with all parents and their access modifiers.
        """
        
        parent_string = ""
        
        #first going through classic inheritance
        for i in cls.inherits_list:
            new_parent = " public {},".format(i.name)
            parent_string = "{}{}".format(parent_string,new_parent)
        
        #then the same for interfaces that are realized by this class
        for i in cls.realizes_list:
            new_parent = " public {},".format(i.name)
            parent_string = "{}{}".format(parent_string,new_parent)
        
        #removing the last comma
        parent_string = parent_string[:-1] 
        
        
        return parent_string
    
    
    
    def getParameters(self,mtd):
        """Generates a string of all parameters of method mtd and their
        data types so they can be used in that method's signature. Also stores
        comments of individual parameters in self.param_comments allowing those
        to be later added in the method comment.
        
        Args:
            mtd (cls_method.Method) - method whose parameters should be parsed here.
            
        Returns:
            A string containing all parameters of the given method and their data types,
            separated with comma.
        """
        
        param_str = ""
        self.param_comments = ""
        
        for param in mtd.param_list:
            s = "{} {},".format(param.d_type,param.name)
            param_str = "{}{}".format(param_str,s)
            
            if not param.comment == "":
                c = self.parameter_comment.format(param.d_type,param.name,param.comment)
                self.param_comments = "{}{}".format(self.param_comments,c)
                
        
        #if no parameters, we insert void
        if param_str == "":
            param_str = "void"
        
        #else removing the final comma
        else:
            param_str = param_str[:-1]
            
            
        return param_str
    
    
    
    def sortUnderAccessModifier(self,visibility,str_type,s):
        """Takes the given string "s" (can represent either attribute
        or method) and based on "visibility" concatenates
        this string with the right access modifier string of the right type
        (either for attributes or methods, based on "str_type").
        
        Args:
            visibility (String) - "private","protected" or "public"
            str_type (String) - "attr" or "mtd" - which string we concatenate to.
            s (String) - string of attribute or method definition
        """
        
        #ATTRIBUTES
        if str_type == "attr":
            if visibility == "private":
                self.private_attr_string = "{}{}".format(self.private_attr_string,s)
                
            elif visibility == "protected":
                self.protected_attr_string = "{}{}".format(self.protected_attr_string,s)
                
            else:
                self.public_attr_string = "{}{}".format(self.public_attr_string,s)
        
        #METHODS
        else:
            if visibility == "private":
                self.private_mtd_string = "{}{}".format(self.private_mtd_string,s)
                
            elif visibility == "protected":
                self.protected_mtd_string = "{}{}".format(self.protected_mtd_string,s)
                
            else:
                self.public_mtd_string = "{}{}".format(self.public_mtd_string,s)
            
        #NOTE: Implementation variant not dealed with so it falls under
        #      public by default. 
         
         
        return



    def wrapUpEntity(self):
        """Puts together all stored strings to create a complete class declaration.
        Saves the string in self.class_string and returns it.
            
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
        
        #class inherits / realizes
        if self.cls.inherits_flag or self.cls.realizes_flag:
            
            parent_string = self.getParentString(self.cls)   #string of classes the current class inherits from/realizes an interface
            self.cls_string = self.derived_format.format(self.cls.name,parent_string,
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

    
    
 