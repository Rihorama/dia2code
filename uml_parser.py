#!/usr/bin/python
import xml.etree.ElementTree as ET
import tempfile
import db_attribute
import db_table
import error_handler
import db_generator

class umlParser:
    
    def __init__(self, xml_path):
        
        self.xml_tree = ET.parse(xml_path)
        self.table_dict = {}
        self.error_handler = error_handler.ErrorHandler()
        
        
    
    def parse(self):
    
        root = self.xml_tree.getroot()
        
        #run for creating tables
        for child in root[1]:
            if child.attrib['type'] == 'Database - Table':
                self.add_table(child)
                
        #run for adding references
        for child in root[1]:
            if child.attrib['type'] == 'Database - Reference':
                self.add_reference(child)
      
                
                
    def add_table(self,table):
        '''
        Takes an element reprezenting a dia table
        and creates a db_table object based on it.
        '''
        
        attr_list = []
        name = None
        new_table = None
        t_id = table.attrib['id']
        
        
        #first cycles the child elements to find table name
        #and creates a table object
        for child in table:
            #table name
            if child.attrib['name'] == 'name':
                name = self.stripHashtags(child[0].text)
                new_table = db_table.Table(name,t_id)
                
        
        #check if table name found and table created
        if new_table == None:                                           ###
            self.error_handler.print_error("dia:table_name_missing")    ###
            e_code = self.error_handler.exit_code["xml"]                ###
                                                                        ###
            exit(e_code)                                                ###
                
        
        #then cycles again to find the other relevant child elements
        for child in table:
            
            if child.attrib['name'] == 'attributes':                
                new_root = child
                
                for child in new_root:
                    new_attr = self.parse_attribute(child,new_table)
                    attr_list.append(new_attr)
                    
                    if new_attr.p_key_flag:
                        new_table.p_key.append(new_attr)
                    
        new_table.attr_list = attr_list
        self.table_dict[t_id] = new_table
                
        
        
    def parse_attribute(self,attr,table):
        '''
        Method receives an element representing a single attribute
        of a table. It parses the attribute's info into a dictionary,
        which is returned.
        '''
        
        attr_dict = {}
        
        for child in attr:
            name = child.attrib['name']
            
            #attributes can either have string or bool as the value we need
            #checking for boolean
            if 'val' in child[0].attrib:
                val = child[0].attrib['val']
                
                if val == 'true':
                    flag = True
                else:
                    flag = False
                    
                attr_dict[name] = flag
                
            #else it's string stroed as text
            else:
                attr_dict[name] = self.stripHashtags(child[0].text)
        
        attr = db_attribute.Attribute(table,attr_dict)
        
        return attr
    
    
    
    def add_reference(self,ref):
        '''
        This method finds tables on both side of the given reference
        arrow element and updates them.
        '''
        
        master = None  #for the table that is referenced
        slave = None   #for the table that uses the reference
        new_root = None
        
        for child in ref:
            local_tag = child.tag.split("}")[1] #gets the local part of the tag
            if local_tag == 'connections':
                new_root = child
                break
        
        #new_root == None means the connection exists but is not properly
        #connected to either table in the diagram
        if new_root == None:
            self.error_handler.print_error("dia:ref_not_closed")   ###
            e_code = self.error_handler.exit_code["diagram"]       ###
                                                                   ###
            exit(e_code)                                           ###
            
                
        for child in new_root: 
            #master table
            if child.attrib['handle'] == "0":
                master_id = child.attrib['to']  #gets the master id
                master = self.table_dict[master_id] 
            
            #slave table
            elif child.attrib['handle'] == "1":
                slave_id = child.attrib['to']  #gets the slave id
                slave = self.table_dict[slave_id] 
                
                
        #error check if either table not found
        if master == None or slave == None:                        ###
            self.error_handler.print_error("dia:ref_not_closed")   ###
            e_code = self.error_handler.exit_code["diagram"]       ###
                                                                   ###
            exit(e_code)                                           ###
        
        
        #updating both tables
        master.add_slave(slave)
        slave.add_foreign_key(master)
            
        
        
    
    
    def stripHashtags(self,string):
        '''
        A simple method that strips first and last character
        of the given string. Used to strip hashtags from Dia strings.
        
        Example: "#I'm a nice string#" to "I'm a nice string".
        '''
        return string[1:-1]
        
            
    
    
parser = umlParser('./Diagram_firma.dia')
parser.parse()

db_type = "mysql"
generator = db_generator.DatabaseGenerator(db_type)
generator.generate(parser.table_dict)