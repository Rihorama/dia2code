#!/usr/bin/python3

from databased.db_uml_parser import DatabaseUmlParser
from databased.db_generator  import DatabaseGenerator

from classd.cls_uml_parser import ClassUmlParser
from classd.cls_generator  import ClassGenerator


class ParserFactory:
    
    def pick(mode,src):        
        """Factory method for choosing the proper
        Uml Parser based on given mode.
        
        Args:
            mode (String) - To choose which Uml Parser to instantiate.
            src (String) - Uml Parser init parameter.
            
        Returns:
            New instance of the selected Uml Parser.
        """
        
        if mode == "database":
            return DatabaseUmlParser(src)
        
        else:    # mode == "class"
            return ClassUmlParser(src)
    
    
    def getDictName(mode):
        """Provides correct dictionary name based on given mode.
        
        Args:
            mode (String) - To choose correct dictionary name.
            
        Returns:
            Correct dictionary name.
        """
        
        if mode == "database":
            return "table_dict"
        
        else:    # mode == "class"
            return "class_dict"
        
        
    pick = staticmethod(pick)
        
        
        
class GeneratorFactory:
    
    def pick(mode,dst,file_name,language,print_option):
        """Factory method for choosing the proper
        Generator based on given mode.
        
        Args:
            mode (String) - To choose which Generator to instantiate.
            dst (String) - Generator init parameter. Dest. file path.
            language (String) - Generator init parameter. Target language.
            print_option (String) - Generator init parameter. Print option.
            
        Returns:
            New instance of the selected Generator.
        """
        
        if mode == "database":
            return DatabaseGenerator(dst,file_name,language,print_option)
        
        else:    # mode == "class"
            return ClassGenerator(dst,file_name,language,print_option)
        
    pick = staticmethod(pick)