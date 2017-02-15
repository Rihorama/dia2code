#!/usr/bin/python3
import xml.etree.ElementTree as ET
import class_diagram.cls_class        as cls_class
import class_diagram.cls_attribute    as cls_attribute
import class_diagram.cls_method       as cls_method
import class_diagram.cls_parameter    as cls_parameter
import class_diagram.cls_association  as cls_association
import class_diagram.cls_generator    as cls_generator
import error_handler

class UmlParser:
    
    def __init__(self, xml_path):
        
        self.class_dict = {}
        self.error_handler = error_handler.ErrorHandler()
        
        self.xml_tree = ET.parse(xml_path) 
            
            
        
        
    
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
            if child.attrib['type'] == "UML - Class":
                self.add_class(child)
                
        #if class_dict empty -> wrong type of dia diagram
        if self.class_dict == {}:
            self.error_handler.print_error("parser:class_wrong_dia")    ###
            e_code = self.error_handler.exit_code["parser"]                ###
                                                                        ###
            exit(e_code)
                
        #run for creating connections
        for child in root[1]:
            if child.attrib['type'] == "UML - Association":
                self.add_connection(child,"association")
            
            elif child.attrib['type'] == "UML - Generalization":
                self.add_connection(child,"generalization")
                
            elif child.attrib['type'] == "UML - Dependency":
                self.add_connection(child,"dependency")
                
            elif child.attrib['type'] == "UML - Realizes":
                self.add_connection(child,"realizes")
                
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
        stereotype = ""
        comment = ""
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
                
            elif child.attrib['name'] == 'comment':
                comment = self.stripHashtags(child[0].text)
                        
                
        
        #check if class name found, if yes, we create a class instance
        if not name == None:
            new_class = cls_class.Class(name,class_id,stereotype,comment)
            
        else:                                                           ###
            self.error_handler.print_error("dia:class_name_missing")    ###
            e_code = self.error_handler.exit_code["xml"]                ###
                                                                        ###
            exit(e_code)                                                ###
            
        
        #then cycles again to find the other relevant child elements
        for child in cls:
            
            if child.attrib['name'] == 'attributes':                
                new_root = child
                
                #parses new attribute and appends it to the list of this class's attributes
                for child in new_root:
                    new_attr = self.parse_child(child,new_class,"attribute")
                    new_class.attr_list.append(new_attr)
            
            
            elif child.attrib['name'] == 'operations':                
                new_root = child
                
                #parses new method and appends it to the list of this class's methods
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
                
            #else it's string stored as text (for data type, comments etc)
            else:
                attr_dict[name] = self.stripHashtags(sub[0].text)
        
        #now initializing instance of the chosen class
        if child_type == "attribute":
            ret = cls_attribute.ClsAttribute(parent,attr_dict)
        elif child_type == "method":
            ret = cls_method.Method(parent,attr_dict)
        else:
            ret = cls_parameter.Parameter(parent,attr_dict)
        
        return ret
    
    
    
    def add_connection(self,connection,name):
        """This method finds classes on both sides of the given connection
        arrow element and updates them.
        
        Args:
            connection  (XML Element): XML structure holding info of the connection.
            name        (String):      Type of the connection (e.g.: generalization, interface)
        """
        
        master = None  #class that is "superior" in the connection (is inherited from etc.)
        slave = None   #for the table that is dependent
        new_root = None
        
        for child in connection:
            local_tag = child.tag.split("}")[1] #gets the local part of the tag
            if local_tag == 'connections':
                new_root = child
                break
        
        #new_root == None means the connection exists but is not properly
        #connected to either class in the diagram
        if new_root == None:
            self.error_handler.print_error("dia:ref_not_closed")   ###
            e_code = self.error_handler.exit_code["diagram"]       ###
                                                                   ###
            exit(e_code)                                           ###
            
                
        for child in new_root: 
            #master class
            if child.attrib['handle'] == "0":
                master_id = child.attrib['to']  #gets the master id
                master = self.class_dict[master_id] 
            
            #slave class
            elif child.attrib['handle'] == "1":
                slave_id = child.attrib['to']  #gets the slave id
                slave = self.class_dict[slave_id] 
                
                
        #error check if either table not found
        if master == None or slave == None:                        ###
            self.error_handler.print_error("dia:ref_not_closed")   ###
            e_code = self.error_handler.exit_code["diagram"]       ###
                                                                   ###
            exit(e_code)                                           ###
        
        
        #updating what's neccessary
        if name == "association":
            self.parseAssociation(connection,master,slave)
        
        elif name == "generalization":
            slave.inherits_flag = True
            slave.inherits_list.append(master)
            
        elif name == "dependency":
            slave.depends_flag = True
            slave.depends_on_list.append(master)
            
        elif name == "realizes":
            slave.realizes_flag = True
            slave.realizes_list.append(master)
        
        
        return
    
    
    
    def parseAssociation(self,connection,A_class,B_class):
        """Performs additional operations and parsing over a connection of association
        needed to properly initialize or update respective class instances.
        This method creates an instance of Assoctiation class and updated one or both
        classes participating in this connection, depending on its parameters.
        
        Args:
            connection   (XML Element): XML structure holding info of the connection.
            A_class      (Class):       Class on the A side of the connection.
            B_class      (Class):       Class on the B side of the connection.
        """

        new_assoc = cls_association.Association()  #new Association instance
        new_assoc.A_dict["class"] = A_class
        new_assoc.B_dict["class"] = B_class
        
        
        #filling the attributes
        for child in connection:
            #local_tag = child.tag.split("}")[1] #gets the local part of the tag
            if "name" in child.attrib.keys():
                name = child.attrib["name"]
            else:
                continue
            
            
            if name == "name":
                new_assoc.name = self.stripHashtags(child[0].text) #getting the name, can be empty
            
            elif name == "direction":
                i = int(child[0].attrib["val"])          #direction index
                new_assoc.direction = new_assoc.direction_dict[i]
                
            elif name == "assoc_type":
                i = int(child[0].attrib["val"])          #type index
                new_assoc.assoc_type = new_assoc.assoc_type_dict[i]
            
            
            #A CLASS
            elif name == "role_a":
                new_assoc.A_dict["role"] = self.stripHashtags(child[0].text)
                
            elif name == "multipicity_a":
                new_assoc.A_dict["multiplicity"] = self.stripHashtags(child[0].text)
                
            elif name == "visibility_a":
                new_assoc.A_dict["visibility"] = int(child[0].attrib["val"])
                
            elif name == "show_arrow_a" and child[0].attrib["val"] == "true":
                new_assoc.A_dict["arrow_visible"] = True
            
            
            #B CLASS
            elif name == "role_b":
                new_assoc.B_dict["role"] = self.stripHashtags(child[0].text)
                
            elif name == "multipicity_b":
                new_assoc.B_dict["multiplicity"] = self.stripHashtags(child[0].text)
                
            elif name == "visibility_b":
                new_assoc.B_dict["visibility"] = child[0].attrib["val"]
                
            elif name == "show_arrow_b" and child[0].attrib["val"] == "true":
                new_assoc.B_dict["arrow_visible"] = True
            
            
            #last but not least, analyzes if given direction and displayed arrows don't
            #collide:
            flag = new_assoc.correctDirection()
            
            #if yes, we rather print error than choose either variant
            if not flag:
                self.error_handler.print_error_twovar("dia:direction_collision",A_class.name,B_class.name)   ###
                e_code = self.error_handler.exit_code["diagram"]                                             ###
                                                                                                             ###
                exit(e_code)                                                                                 ###
                
        
        #no direction means that both sides know about each other
        if new_assoc.direction == "none":
            A_class.association_list.append(new_assoc)
            B_class.association_list.append(new_assoc)
        
        #A knows about B
        elif new_assoc.direction == "A to B":
            A_class.association_list.append(new_assoc)
        
        #B knows about A
        elif new_assoc.direction == "B to A":
            B_class.association_list.append(new_assoc)            
        
        
        return
    
    
    
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
    
    parser = UmlParser('./Class1.dia')
    parser.parse()
    
    cls_type = "cpp"
    saving_type = 2
    file_name = "pokus"
    dest_path = "./pokus/"
    
    generator = cls_generator.ClassGenerator(dest_path,file_name,cls_type,saving_type)
    generator.generate(parser.class_dict)

    
if __name__ == "__main__":
    
    run()
