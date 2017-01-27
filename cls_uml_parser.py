#!/usr/bin/python3
import xml.etree.ElementTree as ET
import cls_class
import cls_attribute
import cls_method
import cls_parameter
import cls_association
import cls_generator
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
            if child.attrib['type'] == "UML - Class":
                self.add_class(child)
                
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
            slave.inherits =  master    #NOTE> We suppose a 1:1 relation
            
        elif name == "dependency":
            slave.depends_flag = True
            slave.depends_on_list.append(master)
            
        elif name == "realizes":
            slave.realizes_flag = True
            slave.realizes = master     #NOTE> We suppose a 1:1 relation
        
        
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

        direction = None
        
        new_assoc = cls_association.Association()  #new Association instance
        new_assoc.A_class = A_class
        new_assoc.B_class = B_class
        
        
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
                direction = new_assoc.direction_dict[i]
                
            elif name == "assoc_type":
                i = int(child[0].attrib["val"])          #type index
                new_assoc.assoc_type = new_assoc.assoc_type_dict[i]
            
            
            #A CLASS
            elif name == "role_a":
                new_assoc.A_role = self.stripHashtags(child[0].text)
                
            elif name == "multiplicity_a":
                new_assoc.A_multiplicity = self.stripHashtags(child[0].text)
                
            elif name == "visibility_a":
                new_assoc.A_visibility = int(child[0].attrib["val"])
            
            
            #B CLASS
            elif name == "role_b":
                new_assoc.B_role = self.stripHashtags(child[0].text)
                
            elif name == "multiplicity_b":
                new_assoc.B_multiplicity = self.stripHashtags(child[0].text)
                
            elif name == "visibility_b":
                new_assoc.B_visibility = int(child[0].attrib["val"])
                
        
        #NOTE: Dia 0.97.2 arrows are probably bugged because they always initially
        #      point from left to right with default direction set to "A to B"
        #      but this happens even if the A table is on the right and B on the left.
        #      If the user swaps arrows to make it visually right, the XML structure
        #      might actually say exactly the opposite, leading to the opposite
        #      outcome than intended (class X knows about class Y instead of the opposite).
        
        #no direction means that both sides know about each other
        if direction == "none":
            A_class.association_list.append(new_assoc)
            B_class.assoctiation_list.append(new_assoc)
        
        #A knows about B
        elif direction == "A to B":
            A_class.association_list.append(new_assoc)
        
        #B knows about A
        elif direction == "B to A":
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
    
    parser = umlParser('./Class1.dia')
    parser.parse()
    
    cls_type = "cpp"
    saving_type = 2
    file_name = "pokus"
    dest_path = "./pokus/"
    
    generator = cls_generator.ClassGenerator(dest_path,file_name,cls_type,saving_type)
    generator.generate(parser.class_dict)

    
if __name__ == "__main__":
    
    run()
