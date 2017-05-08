#!/usr/bin/python3
from parents.cls_textbank import ClassTextBank

class TextBankJava(ClassTextBank):  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
        
        self.cls = None                 #current class
        self.cls_string = ""            #filled with wrapUpEntity()
        
        self.attributes = ""            #for class attributes
        self.methods = ""               #for class methods
        self.param_comments = ""        #help variable to store parameter comments
        
        self.abstract_flag = False
        self.assoc_index = 1               #incremented to secure unique names of
                                           #association variables

         
        
        #--------- FORMAT STRING PATTERNS -----------
        
        # INDENT - set indent for this bank is four spaces
        self.indent = "    "
        
        
        # CLASS PATTERN - main pattern to wrap up the whole class definition
        #               - "{comment}{[abstract ]}public class {class_name} {{\n\n{attributes}\n{methods}}}\n\n\n"
        self.class_format = "{}{}public class {} {{\n\n{}\n{}}}\n\n\n"
        

        # DERIVED CLASS PATTERN -pattern to wrap up derived classes (inherits or implements an interface)
        #                       - "{comment}{[abstract ]}public class {class_name} {parents (both extends and implements)}
        #                           {{\n\n{attributes}{methods}}}\n\n\n"
        self.derived_format = "{}{}public class {} {} {{\n\n{}{}}}\n\n\n"
        
        
        # ATTRIBUTE PATTERN - for attributes without default value
        #                   - "{indent}{access_modifier} {[static ]}{data_type} {attr_name};{line_comment}\n"
        self.attribute_format = "{}{} {}{} {};{}\n"
        
        
        # ATTRIBUTE PATTERN WITH DEFAULT VALUE - attributes with default value
        #                                      - "{indent}{access_modifier} {[static ]}{data_type}
        #                                         {attr_name} = {default_value};{line_comment}\n"
        self.attribute_with_default_format = "{}{} {}{} {} = {};{}\n"

        
        # METHOD DEFINITION PATTERN - for defining a method.
        #                           - "\n{[multiline_comment]}{indent}{access modifier} {[static/abstract] }{data_type} {method_name}
        #                              ({parameters}){{\n{body}\n{indent}}}"
        self.mtd_definition_format = "\n{}{}{} {}{} {}({}) {{\n{}\n{}}}\n"
        
        
        # VECTOR PATTERN - for defining vector variables
        #                - "Vector {name} = new Vector();\n"
        self.vector_format = "Vector {} = new Vector();\n"
        
        
        # INSERT CODE COMMENT - to be put inside empty method definition body
        #                     - "\n{indent}// YOUR CODE HERE\n"
        self.your_code_here_format = "\n{}// YOUR CODE HERE\n"
        
        
        #LINE COMMENT - two indents, then two slashes and the text
        #                - "{indent * 2}// {comment}"
        self.line_comment = "{}// {}"
        
        
        #MULTI-LINE COMMENT - for class comments, possibly method comments if used in definition part
        #                   - "{indent}/*\n{indent} *{comment}\n{indent} */\n"
        self.multiline_comment = "{}/**\n{} * {}{} */\n"
        
        #PARAMETER COMMENT - for individual javadoc parameter comments so they can be added in method description.
        #                   - "{indent} * @param {name} {comment}\n"
        self.parameter_comment = "{} * @param {} {}\n"
        
        #JAVADOC RETURN VALUE - To be added in the method description if the function doesn|t return void.
        #                   - "{indent} * @return {data_type}\n"
        self.return_value_comment = "{} * @return {}\n"

        
                
    def startEntity(self,cls):
        """
        Method that prepares this instance attributes to work on a new
        class. Sets variable strings to empty strings again.
        
        Args:
            cls (cls_class.Class): Class instance to work with.
        """
        self.cls = cls
        self.cls_string = ""
        
        self.attributes = "" 
        self.methods = ""
        self.param_comments = "" 
        
        self.abstract_flag = False
            
        return



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests.
        
        Args:
            attr (cls_attribute.Attribute): Attribute instance to parse into text.
        """
        
        #COMMENT
        #formating comment if present and adding two indents
        comment = ""
        if not attr.comment == "":
            comment = self.line_comment.format(self.indent * 2, attr.comment)


        #STATIC prefix
        static = ""
            
        if attr.static_flag:
            static = "static "
        
        
        #ATTRIBUTE ITSELF
        if attr.value == None:
            s = self.attribute_format.format(self.indent,attr.visibility,static,attr.d_type,
                                             attr.name, comment)
        
        #assigning a value if present: "data_type name = value"
        else:
            s = self.attribute_with_default_format.format(self.indent,attr.visibility,static,
                                                          attr.d_type,attr.name,attr.value,comment)        

        #concatenates it with the rest
        self.attributes = "{}{}".format(self.attributes,s)            
        
        return



    def addMethod(self,mtd):
        """Using parameters of given method, generates two strings: declaration of
        the method which will be added under the proper access modifier
        and the definition of the method with empty body, each stored
        in their respective "group string".
        
        Args:
            mtd (cls_method.Method): Method instance to parse into text.
        """
        
        #PARAMETERS
        #first we generate string with all parameters
        param_str = self.getParameters(mtd)
        
        
        #COMMENT
        #formating comment if present and adding two indents, uses line comment format
        comment = ""
        if not mtd.comment == "":
            comment = "{}\n".format(mtd.comment)

        #were any parameter comments present?
        if not self.param_comments == "":
            comment = "{}{}".format(comment,self.param_comments)
            
        #is there a return value?
        if not mtd.d_type == "void":
            ret = self.return_value_comment.format(self.indent,mtd.d_type)
            comment = "{}{}".format(comment,ret)
        
        #wrapping it with a multiline comment
        comment = self.multiline_comment.format(self.indent,self.indent,comment,self.indent)
        
        
        #YOUR CODE HERE
        your_code_here = self.your_code_here_format.format(self.indent)
  
  
        #STATIC / ABSTRACT
        modifier = ""
        
        if mtd.abstract_flag:   #abstract given priority if collission
            modifier = "abstract "
            self.abstract_flag = True
        
        elif mtd.static_flag:
            modifier = "static "


        s = self.mtd_definition_format.format(comment,self.indent,mtd.visibility,
                                              modifier,mtd.d_type,mtd.name,param_str,
                                              your_code_here,self.indent)        
        
        self.methods = "{}{}".format(self.methods,s)
        
        return
            
            
            
    def addAssociation(self,assoc):
        """Gets an instance of Association and turns it into a proper
        attribute (single value if multiplicity is 1, vector for
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
            
        
        #NEW ATTRIBUTE NAME        
        name = None
        
        #using the other table's role if it was named in the association
        if not other_dict["role"] == "": #format: "rolename_othername_association"
            
            role = other_dict["role"]
            role = role.replace(" ","_") #precaution in case white spaces present, replaces with _
            
            name = "{}_{}_association".format(role,other_dict["class"].name)
            
        else: #we must manage with format: "othername_association"
            name = "{}_association{}".format(other_dict["class"].name,self.assoc_index)
            self.assoc_index = self.assoc_index + 1 #increasing the counter, this number is taken
            
        
        
        #this class is the "member" class and it will have attribute referencing the "other" class
        #thus the multiplicity of the other class matters
        s = ""
        
        if assoc.isSingleMultiplicity(other): #new attribute, public with no static modifier and no comment
            s = self.attribute_format.format(self.indent,"public","",other_dict["class"].name,
                                             name,"")            
        else: #multiple or variable amount of values => vector
            s = self.vector_format.format(name)        
        
        #adds 2x indent
        s = "{}{}".format(self.indent * 2,s)        

        return
        
        
        
    def getParentString(self,cls):
        """Goes through all classes this class inherits from and all interfaces this
        class implements, puts them after "extends" or "implements" modifier respectively,
        and then concatenates all that in one string that is to be inserted in the class header.
        
        Returns:
            String with all parents and implemented interfaces.
        """

        extends = ""
        implements = ""
        
        #first going through classic inheritance
        for i in cls.inherits_list:
             extends = "{}{},".format(extends,i.name)
        
        #then the same for interfaces that are implemented by this class
        for i in cls.realizes_list:
            implements = "{}{},".format(implements,i.name)
        
        #removing the last comma
        extends = extends[:-1]
        implements = implements[:-1]
        
        if not extends == "":
            extends = "extends {}".format(extends)
        if not implements == "":
            implements = "implements {}".format(implements)
            
        #adding a white space for "implements" to follow
        if not extends == "" and not implements == "":
            extends == "{} ".format(extends) 
        
        return "{}{}".format(extends,implements)
    
    
    
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
                c = self.parameter_comment.format(self.indent, param.name, param.comment)
                self.param_comments = "{}{}".format(self.param_comments,c)
                
        #else removing the final comma
        else:
            param_str = param_str[:-1]            
            
        return param_str
    


    def wrapUpEntity(self):
        """Puts together all stored strings to create a complete class declaration.
        Saves the string in self.class_string and returns it.
            
        Returns:
            Final Class string.
        """

        #COMMENT (no indent)
        comment = ""
        if not self.cls.comment == "":
            c = "{}\n".format(self.cls.comment)
            comment = self.multiline_comment.format("","",c,"")

        #ABSTRACT?
        abstract = ""
        if self.cls.abstract_flag:
            abstract = "abstract "
        
        
        #SUBCLASS
        if self.cls.inherits_flag or self.cls.realizes_flag:
            
            #string of classes the current class inherits from/realizes an interface
            parent_string = self.getParentString(self.cls)  
            self.cls_string = self.derived_format.format(comment,abstract,self.cls.name,
                                                         parent_string,self.attributes,self.methods)
        
        #NORMAL
        else:
            self.cls_string = self.class_format.format(comment,abstract,self.cls.name,self.attributes,
                                                       self.methods)
        
        return self.cls_string
    
