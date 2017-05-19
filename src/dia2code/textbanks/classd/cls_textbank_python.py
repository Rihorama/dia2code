#!/usr/bin/python3
from parents.cls_textbank import ClassTextBank

class TextBankPython(ClassTextBank):  

    def __init__(self):
        
        self.cls = None                 #current class
        self.cls_string = ""            #filled with wrapUpEntity ()
                
        self.static_attributes = ""
        self.attributes = ""
        self.methods = ""               #definitions of methods with empty body
        
        self.param_comments = ""        #help variable to store parameter comments
        
        self.abstract_flag = False
        self.init_present_flag = False  #is the __init__ method present in the diagram
        
        self.assoc_index = 1               #incremented to secure unique names of
                                           #association variables

         
        
        #--------- FORMAT STRING PATTERNS -----------
        
        # INDENT - set indent for this bank is four spaces
        self.indent = "    "
        
        
        # CLASS PATTERN - main pattern to wrap up the whole class definition
        #               - "{[import]}\n
        #                  class {class_name}:\n{comment}{static_attributes}{method_definitions}\n\n"
        self.class_format = "{}\nclass {}:\n{}{}{}\n\n"
        

        # DERIVED CLASS PATTERN -pattern to wrap up derived classes (inherits or implements an interface)
        #                       - "{[import]}\n
        #                          {indent}class {class_name}({parent_class}):\n{comment}{static_attributes}{method_definitions}\n\n"
        self.derived_format = "{}\nclass {}({}):\n{}{}{}\n\n"  
        
        
        # ATTRIBUTE PATTERN - for attributes, default value always present, None if not provided
        #                   - "{indent}self.{attr_name} = {value}{line_comment}\n"
        self.attribute_format = "{}self.{} = {}{}\n"   
        
        
        # STATIC ATTRIBUTE PATTERN - static for attributes defined in class body but not in any method
        #                   - "{indent}{attr_name} = {value}{line_comment}\n"
        self.static_attribute_format = "{}{} = {}{}\n"
        
        
        # __init__ PATTERN - for defining a method inside class body
        #                           - "\n{indent}def __init__(self):\n\n{object_attributes}\n\n"
        self.init_format = "{}def __init__(self):\n\n{}\n\n"
        
        
        # METHOD PATTERN - for defining a method inside class body
        #                           - "{indent}def {method_name}({parameters}):\n{[multiline_comment]}{body}\n\n"
        self.mtd_format = "{}def {}({}):\n{}{}\n\n"
        
        
        # STATIC METHOD PATTERN - for defining a static method with a decorator
        #                       - "{indent}@staticmethod\n
        #                       -  {indent}def {method_name}({parameters}):\n{[multiline_comment]}{body}\n\n"
        self.static_mtd_format = "{}@staticmethod\n{}def {}({}):\n{}{}\n\n"
        
        
        # ABSTRACT METHOD PATTERN - for declaring abstract methods with a decorator
        #                            - "{indent}@abstractmethod\n
        #                               {indent}def {method_name}({parameters}):\n{multiline_comment}\n{indent*2}pass\n"
        self.abstract_mtd_format = "{}@abstractmethod\n{}def {}({}):\n{}{}pass\n"
        
        
        # PARAMETER PATTERN - method parameter without default value
        #                            - "{name},"
        self.param_format = "{},"
        
        
        # DEFAULT PARAMETER VALUE PATTERN - to set a default value for a method parameter
        #                            - "{name} = {default_value},"
        self.default_param_format = "{} = {},"
        

        # ABSTRACT MODULE IMPORT - in case abstract methods are present we need to import this
        self.abstract_import = "from abc import ABCMeta, abstractmethod\n"
        
        
        # ABSTRACT STATIC VARIABLE - needs to be present in abstract class as static variable
        #                         - "{indent}__metaclass__ = ABCMeta\n"
        self.abstract_var = "{}__metaclass__ = ABCMeta\n\n"
        
        
        # LIST PATTERN - for defining a list
        #              - {indent}self.{name} = []\n
        self.list_format = "{}self.{} = []\n"
        
        
        # INSERT CODE COMMENT - to be put inside empty method definition body
        #                     - "\n{indent}# YOUR CODE HERE\n\n"
        self.your_code_here = "\n{}# YOUR CODE HERE\n\n"
        
        
        #LINE COMMENT - hash and the text
        #                - "#{comment}"
        self.line_comment = "#{}"
        
        
        #MULTI-LINE COMMENT - for class comments, possibly method comments if used in definition part
        #                   - "{indent}\"\"\"\n{comment}\n{indent}\"\"\"\n\n"
        self.multiline_comment = "{}\"\"\"\n{}\n{}\"\"\"\n"
        
        
        #PARAMETER COMMENT - for individual method parameter comments so they can be added in method description.
        #                   - "{indent}{name} - {comment}\n"
        self.parameter_comment = "{}{} - {}\n"

        
                
    def startEntity(self,cls):
        """
        Method that prepares this instance attributes to work on a new
        class. Sets variable strings to empty strings again.
        
        Args:
            cls (cls_class.Class): Class instance to work with.
        """
        self.cls = cls
        self.cls_string = ""
        
        self.static_attributes = ""
        self.attributes = ""
        self.methods = ""
        
        self.param_comments = ""
        
        self.abstract_flag = False
        self.assoc_index = 1
            
        return



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests. Creates needed strings and appends them to their respective
        string variables.
        
        Args:
            attr (cls_attribute.Attribute): Attribute instance to parse into text.
        """
        
        s = ""
        value = None        
        
        #VALUE
        #determining attribute value, if not present, default is None
        if not attr.value == "":
            value = attr.value
            
        
        #COMMENT
        #formating comment if present and adding two indents
        if not attr.comment == "":
            comment = self.line_comment.format(attr.comment)
            comment = "{}{}".format(self.indent * 2,comment)
        
        else:
            comment = ""
            
               
        #STATIC ATTRIBUTE
        #static variables go separate           
        if attr.static_flag:
            
            #creates the attr string
            s = self.static_attribute_format.format(self.indent,attr.name,
                                                    value,comment)
            #concatenates it to the rest of static attributes
            self.static_attributes = "{}{}".format(self.static_attributes,s)
        
        #CLASSIC ATTRIBUTE
        #gonna go to __init__
        else:
            indent = self.indent * 2
            
            #creates the attr string
            s = self.attribute_format.format(indent,attr.name,value,comment)
            
            #concatenates it to the rest of classic attributes
            self.attributes = "{}{}".format(self.attributes,s)
        
        return



    def addMethod(self,mtd):
        """Using parameters of given method, creates a string
        with this method definition with empty body."
        
        Args:
            mtd (cls_method.Method): Method instance to parse into text.
        """
        
        #PARAMETERS
        #first we generate string with all parameters
        param_str = self.getParameters(mtd)
        
        #COMMENT
        #formating comment if present and adding two indents, uses line comment format
        #abstract method will just take the classic comment
        comment = ""
        
        #classic method comment
        if not mtd.comment == "":
            comment = "{}{}\n".format(self.indent * 2,mtd.comment)
        
        #parameter comments
        if not self.param_comments == "":
            comment = "{}{}".format(comment,self.param_comments)
        
        #if there is any comment of the two above
        if not comment == "":
            indent = self.indent * 2
            comment = self.multiline_comment.format(indent,comment,indent)
        
        
        #YOUR CODE HERE    
        your_code_here = self.your_code_here.format(self.indent * 2)
  

        #ABSTRACT
        if mtd.abstract_flag:
            s = self.abstract_mtd_format.format(self.indent,self.indent,mtd.name,
                                                param_str,comment,self.indent*2)
            self.abstract_flag = True
            #formats the abstract static var and adds it to the other static vars
            abstract_var = self.abstract_var.format(self.indent)
            self.static_attributes = "{}{}".format(self.static_attributes,abstract_var)
            
        #STATIC
        elif mtd.static_flag:
            s = self.static_mtd_format.format(self.indent,mtd.name,param_str,
                                              comment,your_code_here)

        #__INIT__ METHOD - will be filled with instancial attributes
        elif mtd.name == "__init__":
            combined = "{}{}".format(self.attributes,your_code_here)
            s = self.mtd_format.format(self.indent,mtd.name,param_str,
                                              comment,combined)
            self.init_present_flag = True
        
        #CLASSIC
        else:
            s = self.mtd_format.format(self.indent,mtd.name,param_str,
                                       comment,your_code_here)
        
        
        #adds to the rest
        self.methods = "{}{}".format(self.methods,s)        
        
        return
            
            
            
    def addAssociation(self,assoc):
        """Gets an instance of Association and turns it into a proper
        attribute (single value if multiplicity is 1, list for
        variable count of values). Adds the attribute to other class
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
            role = role.replace(" ","_") #precaution in cae white spaces present, replaces with _
            
            name = "{}_{}_association".format(role,other_dict["class"].name)
            
        else: #we must manage with format: "othername_association"
            name = "{}_association{}".format(other_dict["class"].name,self.assoc_index)
            self.assoc_index = self.assoc_index + 1 #increasing the counter, this number is taken        
        
        
        #this class is the "member" class and it will have attribute referencing the "other" class
        #thus the multiplicity of the other class matters
        s = ""
        
        if assoc.isSingleMultiplicity(other):
            s = self.attribute_format.format(self.indent * 2,name,
                                      "None","")   #value set as None and no comment
            
        else: #multiple or variable amount of values => list
            s = self.list_format.format(self.indent * 2, name)
        
        #adding to the rest
        self.attributes = "{}{}".format(self.attributes,s)
        
        return
    
    
        
    def getParentString(self,cls):
        """Goes through all classes this class inherits from and puts them
        in one string that is to be inserted in the class header.
        
        Returns:
            String with all parents and their access modifiers.
        """
        
        parent_string = ""
        
        #first going through classic inheritance
        for i in cls.inherits_list:
            parent_string = "{}{},".format(parent_string,i.name)
        
        #then the same for interfaces that are realized by this class
        for i in cls.realizes_list:
            parent_string = "{}{},".format(parent_string,i.name)
        
        #removing the last comma
        parent_string = parent_string[:-1]        
        
        return parent_string
    
    
    
    def getParameters(self,mtd):
        """Generates a string of all parameters of method mtd so they can be
        used in that method's signature. Also stores comments of individual
        parameters in self.param_comments allowing those to be later added
        in the method comment.
        
        Args:
            mtd (cls_method.Method) - method whose parameters should be parsed here.
            
        Returns:
            A string containing all parameters of the given method separated with comma.
        """
        
        param_str = ""     #self is always present
        default_param_str = ""
        self.param_comments = "" 
        
        for param in mtd.param_list:
            
            if param.value == None:
                s = self.param_format.format(param.name)
                param_str = "{}{}".format(param_str,s)
                
            else:
                #the string with default value is saved in default_param_string
                s = self.default_param_format.format(param.name, param.value)
                default_param_str = "{}{}".format(default_param_str,s)
            
            if not param.comment == "":
                c = self.parameter_comment.format(self.indent * 2, param.name,
                                                  param.comment)
                self.param_comments = "{}{}".format(self.param_comments,c)
        
        
        #putting the two together
        param_str = "{}{}".format(param_str,default_param_str)
        
        #removing the final comma
        param_str = param_str[:-1]   
        
        #removing the last newline from comments
        self.param_comments = self.param_comments[:-1] 
            
        return param_str
    
    
   
    def wrapUpEntity(self):
        """Puts together all stored strings to create a complete class declaration.
        Saves the string in self.class_string and returns it.
            
        Returns:
            Final Class string.
        """       
        
        #COMMENT (no indent)
        if not self.cls.comment == "":
            cls_comment = "{}{}".format(self.indent,self.cls.comment)
            comment = self.multiline_comment.format(self.indent,cls_comment,self.indent)
        
        else:
            comment = ""            
            
        #INIT METHOD
        if not self.attributes == "" and not self.init_present_flag:
            init = self.init_format.format(self.indent, self.attributes)
            self.methods = "{}{}".format(init,self.methods)
        
        
        #IMPORT - if we have abstract methods, we need to import required module
        if self.abstract_flag:
            imp = self.abstract_import
            
        else:
            imp = ""
        
        
        #DEPENDING CLASS
        if self.cls.inherits_flag or self.cls.realizes_flag:
            
            #string of classes the current class inherits from/realizes an interface
            parent_string = self.getParentString(self.cls)
            self.cls_string = self.derived_format.format(imp, self.cls.name, parent_string, comment,
                                                         self.static_attributes,self.methods)
        
        #NORMAL CLASS
        else:
            self.cls_string = self.class_format.format(imp, self.cls.name, comment,
                                                       self.static_attributes,self.methods)
        
        return self.cls_string
    