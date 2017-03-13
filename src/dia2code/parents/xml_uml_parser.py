#!/usr/bin/python3

from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET
import gzip
from parents.uml_parser import UmlParser
from error_handler import ErrorHandler

err = ErrorHandler()


class XmlUmlParser(UmlParser):
    #Abstract class to be parent to both Databse and Class uml parsers
    
    __metaclass__ = ABCMeta 
    
    
    @abstractmethod
    def parse(self): pass


    def parse_into_etree(self,xml_path):
        """ Calls self.opener() on the given xml_path, parses the opened file
        with ElementTree parser and returns the result ElementTree object.
        
        Args:
            xml_path (String) - Path to the source Dia XML.
            
        Returns:
            Element Tree object representing the source Dia XML.
        """
        
        f = self.opener(xml_path)
        xml_tree = None
        
        #PARSING XML
        try:
            xml_tree = ET.parse(f) 
            
        except ET.ParseError:                                      ###
            err.print_error_onevar("parameter:not_xml",xml_path)   ###
            e_code = err.exit_code["parameter"]                    ###
                                                                   ###
            exit(e_code)            
        
        f.close()        
        
        return xml_tree


    def opener(self,xml_path):
        """Provides opening the source Dia XML file, deals with gzip compression
        if needed since Dia uses gzip to compress its XML.
        
        Args:
            xml_path (String) - Path to the source Dia XML.
            
        Returns:
            File object for the source Dia XML.
        """        

        try:
            f = open(xml_path,'rb')
            
        except (OSError, IOError):                                            ###
            err.print_error_onevar("parameter:trouble_opening_file",xml_path) ###
            e_code = err.exit_code["parameter"]                               ###
                                                                              ###
            exit(e_code)                                                      ###
            
        
        #getting magical sequence to find out if gzipped
        magical = f.read(2)

        
        #if magical sequence equals to what gzip should have
        if (magical == b'\x1f\x8b'):
            f.seek(0)            
            f = gzip.GzipFile(xml_path)    #goes through gzip
            
        else:
            f.seek(0) 
            
        return f
    
    
    def stripHashtags(self,string):
        """A simple method that strips the and last character
        of the given string. Used to strip hashtags from Dia strings.
        
        Example: "#I'm a nice string#" to "I'm a nice string".
        
        Args:
            string (String): The string to be parsed.
            
        Returns:
            The parsed string, stripped of the hashtags, if used properly.
        """
        #print("<hash>{}</hash>".format(string))
        #print("<nohash>{}</nohash>".format(string[1:-1]))
        
        return string[1:-1]
    