#!/usr/bin/python3
import xml.etree.ElementTree as ET
import cls_class
import cls_attribute
import cls_method
import cls_parameter
import error_handler

class umlParser:
    
    def __init__(self, xml_path):
        
        self.xml_tree = ET.parse(xml_path)
        self.class_dict = {}
        self.error_handler = error_handler.ErrorHandler()
        
        
    
    def parse(self):
        """
        Core method of this class. Organizes the whole process
        of XML parsing and turning the acquired info into instances
        of Class, Attribute and Method.

        Parses the XML structure given during initialization.
        """
    
        root = self.xml_tree.getroot()
        
        #run for creating classes
        for child in root[1]:
            if child.attrib['type'] == 'UML - Class':
                self.add_class(child)
                
                
        for class_id in self.class_dict:
            cls = self.class_dict[class_id]
            print("Class name: {}, id: {}, stereotype: {}".format(cls.name,cls.id,cls.stereotype))
            
            #for attr in cls.attr_list:
            #    attr.print_me()
                
            #for method in cls.method_list:
            #    method.print_me()
                
        return
      
                
                
    def add_class(self,cls):
        """Takes an element reprezenting a dia table
        and creates a db_table object based on it.
        
        Args:
            table (XML Element): XML structure holding info of one table.
        """
        
        attr_list = []
        method_list = []
        name = None
        stereotype = None
        new_class = None
        class_id = cls.attrib['id']
        
        
        #first cycles the child elements to find class name
        #and creates a class object
        for child in cls:
            #table name
            if child.attrib['name'] == 'name':
                name = self.stripHashtags(child[0].text)
            
            elif child.attrib['name'] == 'stereotype':
                stereotype = self.stripHashtags(child[0].text)
                new_class = cls_class.Class(name,class_id,stereotype)
        
                
        
        #check if table name found and table created
        if new_class == None:                                           ###
            self.error_handler.print_error("dia:class_name_missing")    ###
            e_code = self.error_handler.exit_code["xml"]                ###
                                                                        ###
            exit(e_code)                                                ###
            
        
        #then cycles again to find the other relevant child elements
        for child in cls:
            
            if child.attrib['name'] == 'attributes':                
                new_root = child
                
                for child in new_root:
                    new_attr = self.parse_child(child,new_class,"attribute")
                    new_class.attr_list.append(new_attr)
                    
            elif child.attrib['name'] == 'operations':                
                new_root = child
                
                for child in new_root:
                    new_method = self.parse_child(child,new_class,"method")
                    new_class.method_list.append(new_method)

        
        self.class_dict[class_id] = new_class
                
        
    
    def parse_child(self,child,parent,child_type):
        """Method receives an element representing a single attribute
        or operation of a class. It parses its info into a dictionary,
        which is returned.
        
        Args:
            child      (XML Element):  XML structure with one child info.
            parent     (Class/None):   "Parent" instance to be connected with
                                       the new instance of chosen class. Parent to
                                       Attribute and Method instances is Class. Parent
                                       to Parameter instance is None (not needed).
            child_type (String):       Name of the class whose instance shall be created.
                                       Knows: Attribute, Method and Parameter
            
        Returns:
            Properly initialized instance of chosen class.
        """
        
        attr_dict = {}

        for sub in child:
            name = sub.attrib["name"]
            
            
            #method parameters need to get special treatment
            #which uses this very method once again (lvl 1 recursion)
            if name == "parameters":
                new_root = sub
                param_list = []
                
                for param in new_root:
                    #sending None 
                    new_param = self.parse_child(param,None,"parameter")
                    param_list.append(new_param)
                    
                attr_dict["parameters"] = param_list
            
            #checking for boolean
            elif 'val' in sub[0].attrib:
                val = sub[0].attrib['val']
                
                if val == 'true':
                    x = True
                
                elif val == "false":
                    x = False
                    
                else:
                    x = int(val)
                    
                attr_dict[name] = x
                
            #else it's string stroed as text
            else:
                attr_dict[name] = self.stripHashtags(sub[0].text)
        
        #now initializing instance of the chosen class
        if child_type == "attribute":
            ret = cls_attribute.Attribute(parent,attr_dict)
        elif child_type == "method":
            ret = cls_method.Method(parent,attr_dict)
        else:
            ret = cls_parameter.Parameter(parent,attr_dict)
        
        return ret
    
    
    
    def stripHashtags(self,string):
        """A simple method that strips the and last character
        of the given string. Used to strip hashtags from Dia strings.
        
        Example: "#I'm a nice string#" to "I'm a nice string".
        
        Args:
            string (String): The string to be parsed.
            
        Returns:
            The parsed string, stripped of the hashtags, if used properly.
        """
        return string[1:-1]
        
            
def run():    
    
    parser = umlParser('./Class1.dia')
    parser.parse()

    
if __name__ == "__main__":
    
    run()
