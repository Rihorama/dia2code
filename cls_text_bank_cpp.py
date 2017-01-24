#!/usr/bin/python3

class TextBank:  
    #TODO: deal with possibility of wrong parameter coming...?
    
    def __init__(self):
        
        self.indent = "    " #four spaces
        self.class_format = "class {} {{\n{}\n}}\n"
        self.private_format = "{}private:\n{}\n"      #formatted string for private elements
        self.protected_format = "{}protected:\n{}\n"  #formatted string for protected elements
        self.public_format = "{}public:\n{}\n"        #formatted string for public elements
        
        self.cls = None                 #current class
        self.cls_string = ""            #filled with wrapUpClass()
        
        self.private_attr_string = ""       #for private attributes
        self.protected_attr_string = ""     #for protected attrbitues
        self.public_attr_string = ""        #for public attributes
        
        self.private_mtd_string = ""       #for private methods
        self.protected_mtd_string = ""     #for protected methods
        self.public_mtd_string = ""        #for public methods

        
        
        
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
        

            
        return



    def addAttribute(self,attr):
        """Parses the info of given Attribute instance so all neccessary info
        is included in the final string in the way that this language
        requests. Creates needed strings and appends them to their respective
        self.x_string variables.
        
        Args:
            attr (cls_attribute.Attribute): Attribute instance to parse into text.
        """
        
        # "data_type name"
        s = "{} {}".format(attr.d_type, attr.name)
        
        #assigning a value if present: "data_type name = value"
        if not attr.value == None:
            s = "{} = {}".format(s, attr.value)
        
        #adds 2x indent, semicolon and newline
        s = "{}{}{};\n".format(self.indent,self.indent,s)
        
        
        #picking the right access modifier string
        #NOTE: So far "Implementation" variant fall under "Public"
        if attr.visibility == "private":
            self.private_attr_string = "{}{}".format(self.private_attr_string,s)
            
        elif attr.visibility == "protected":
            self.protected_attr_string = "{}{}".format(self.protected_attr_string,s)
            
        else:
            self.public_attr_string = "{}{}".format(self.public_attr_string,s)



    def wrapUpClass(self):
        """Puts together all stored strings to create a complete class declaration.
        Saves the string in self.table_string and returns it.
            
        Returns:
            Final Class string.
        """
        
        #private, protected and public access modifiers and their content
        private = self.wrapUpPrivate()
        protected = self.wrapUpProtected()
        public = self.wrapUpPublic()
        
        declarations = "{}{}{}".format(private,protected,public)
        
        self.cls_string = self.class_format.format(self.cls.name,declarations)
        
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
        
        #formates with the format string, adds indent and returns it
        return self.private_format.format(self.indent,private)
    
    
    
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
        
        #formates with the format string, adds indent and returns it
        return self.protected_format.format(self.indent,protected)
    
    
    
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
        
        ##formates with the format string, adds indent and returns it
        return self.public_format.format(self.indent,public)

    
    
 