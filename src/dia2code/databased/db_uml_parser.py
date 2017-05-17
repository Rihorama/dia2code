#!/usr/bin/python3
import xml.etree.ElementTree as ET
import gzip

import databased.db_attribute  as db_attribute
import databased.db_table      as db_table
import databased.db_generator  as db_generator

from parents.xml_uml_parser import XmlUmlParser
import error_handler


class DatabaseUmlParser(XmlUmlParser):
    
    def __init__(self, xml_path):
        
        self.table_dict = {}
        self.err = error_handler.ErrorHandler()
        
        #using parent class method to check, open and parse the dia xml
        self.xml_tree = super(DatabaseUmlParser,self).parse_into_etree(xml_path)
        
        return
        
    
    def parse(self):
        """
        Core method of this class. Organizes the whole process
        of XML parsing and turning the acquired info into instances
        of Table and Attribute.

        Parses the XML structure given during initialization.
        """
    
        root = self.xml_tree.getroot()
        
        #run for creating tables
        for child in root[1]:
            if child.attrib['type'] == 'Database - Table':
                self.addTable(child)
        
        
        #if table_dict empty -> wrong type of dia diagram
        if self.table_dict == {}:                                ###
            self.err.printError("parser:database_wrong_dia")    ###
            e_code = self.err.exit_code["parser"]                ###
                                                                 ###
            exit(e_code)                                         ###
         
         
        #run for adding references
        for child in root[1]:
            if child.attrib['type'] == 'Database - Reference':
                self.addReference(child)
                
        return
      
                
                
    def addTable(self, table):
        """Takes an element reprezenting a dia table
        and creates a db_table object based on it.
        
        Args:
            table (XML Element): XML structure holding info of one table.
        """
        
        attr_list = []
        name = None
        comment = ""
        new_table = None
        t_id = table.attrib['id']
        
        
        #first cycles the child elements to find table name
        #and creates a table object
        for child in table:
            #table name
            if child.attrib['name'] == 'name':
                name = super(DatabaseUmlParser,self).stripHashtags(child[0].text)
                
            elif child.attrib['name'] == 'comment':
                comment = super(DatabaseUmlParser,self).stripHashtags(child[0].text)
                                
        
        #check if table name found and table created
        if not name == None:
            new_table = db_table.Table(name,t_id,comment)
            
        else:                                                 ###
            self.err.printError("dia:table_name_missing")    ###
            e_code = self.err.exit_code["xml"]                ###
                                                              ###
            exit(e_code)                                      ###
                
        
        #then cycles again to find the other relevant child elements
        for child in table:
            
            if child.attrib['name'] == 'attributes':                
                new_root = child
                
                for child in new_root:
                    new_attr = self.parseAttribute(child, new_table)
                    attr_list.append(new_attr)
                    
                    if new_attr.p_key_flag:
                        new_table.p_key.append(new_attr)
                    
        new_table.attr_list = attr_list
        self.table_dict[t_id] = new_table
        
        return
                
        
        
    def parseAttribute(self, attr, table):
        """Method receives an element representing a single attribute
        of a table. It parses the attribute's info into a dictionary,
        which is returned.
        
        Args:
            attr  (XML Element): XML structure with one attribute info.
            table (Table): Table instance to be connected with the new Attribute instance.
            
        Returns:
            Properly initialized Attribute instance.
        """
        
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
                attr_dict[name] = super(DatabaseUmlParser,self).stripHashtags(child[0].text)
        
        attr = db_attribute.DbAttribute(table,attr_dict)
        
        return attr
    
    
    
    def addReference(self, ref):
        """This method finds tables on both sides of the given reference
        arrow element and updates them.
        
        Args:
            ref (XML Element): XML structure holding info of the reference.
        """
        
        master = None  #for the table that is referenced
        slave = None   #for the table that uses the reference
        new_root = None
        
        for child in ref:
            local_tag = child.tag.split("}")[1] #gets the local part of the tag
            if local_tag == 'connections':
                new_root = child
                break
        
        #new_root == None means the connection exists but is not properly
        #connected to any table in the diagram
        if new_root == None:                             ###
            self.err.printError("dia:ref_not_closed")   ###
            e_code = self.err.exit_code["diagram"]       ###
                                                         ###
            exit(e_code)                                 ###
            
                
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
        if master == None or slave == None:              ###
            self.err.printError("dia:ref_not_closed")   ###
            e_code = self.err.exit_code["diagram"]       ###
                                                         ###
            exit(e_code)                                 ###
        
        
        #updating both tables
        master.addSlave(slave)
        slave.addForeignKey(master)
        
        return
