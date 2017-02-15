#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter

import error_handler
import os.path

import er_diagram.db_uml_parser      as db_uml_parser
import er_diagram.db_generator       as db_generator

import class_diagram.cls_uml_parser  as cls_uml_parser
import class_diagram.cls_generator   as cls_generator




def main():
    

    args = parseArguments()
    err = error_handler.ErrorHandler()
    
    mode = None
    src = None
    dst = None
    file_name = None
    language = None
    print_option = None

    
    #MODE
    if args.mode == "d":
        mode = "database"
        
    elif args.mode == "c":
        mode = "class"
        
    else:
        err.print_error_onevar("parameter:wrong_mode",args.mode)
        e_code = err.exit_code["parameter"]
        
        exit(e_code)
    
    
    #SOURCE PATH
    src = args.src
    
    if not os.path.exists(src):
    
        err.print_error_onevar("parameter:bad_source",src)        
        e_code = err.exit_code["parameter"]
        
        exit(e_code)
    
    
    #DESTINATION FOLDER
    dst = args.dst
    
    if not os.path.isdir(dst):
    
        err.print_error_onevar("parameter:bad_destination",dst)        
        exit(err.exit_code["parameter"])
    
    if not dst[-1] == "/":
        dst = "{}/".format(dst)
        
    
    #LANGUAGE
    language = args.language
    
    flag_db =  language not in db_generator.DatabaseGenerator.supported_language_dict.keys()
    flag_cls = language not in cls_generator.ClassGenerator.supported_language_dict.keys()    
    
    
    #default database target language
    if language == None and mode == "database":
        language = "mysql"        
        
    #default class target language  
    elif language == None and mode == "class":        
        language = "c++"        
        
    #language given but not supported
    elif (mode == "database" and flag_db) or (mode == "class" and flag_cls):        
        err.print_error_twovar("parameter:unsupported_language",language,mode)
        e_code = err.exit_code["parameter"]
        
        exit(e_code)
    
    
    #RESULT FILE NAME (if not given, uses source file name)
    if args.name == None:
        file_name = os.path.basename(args.src)  #name with extension
        file_name = file_name.split(".")[0]     #all prior to first comma
        
    else:
        file_name = args.name 
        
        
    #PRINTING OPTIONS
    valid_options = ["t","f","ff"]
    
    if args.print == None:
        print_option = "f"
        
    elif not args.print == None and args.print in valid_options:
        print_option = args.print
        
    else:
        err.print_error_onevar("parameter:wrong_print",args.print)
        e_code = err.exit_code["parameter"]
        
        exit(e_code)
        
    
    
    #------------------------
    #BRANCHING BEWTEEN DATABASE AND CLASS PARSERS AND GENERATORS
    #------------------------
    if mode == "database":
        
        parser = db_uml_parser.UmlParser(src)
        parser.parse()
        
        generator = db_generator.DatabaseGenerator(dst,file_name,language,print_option)
        generator.generate(parser.table_dict)
        
        
    elif mode == "class":
        
        parser = cls_uml_parser.UmlParser(src)
        parser.parse()
        
        generator = cls_generator.ClassGenerator(dst,file_name,language,print_option)
        generator.generate(parser.class_dict)
        


def parseArguments():
    """Wrapping up argparse functionality in a separate function to make the code
    more well-aranged.
    
    Returns:
        Arguments from argparse.
    """
    
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='''\
...                     DIA 2 CODE
...         ----------------------------------
...         Written by: Alice Minarova
...                     Brno 2016/2017
...         As: Diploma thesis for Faculty
...             of Mechanical Enegeneering,
...             Brno University of Technology.


This program's purpose is to convert UML diagrams created in
the diagramming software Dia to a valid code, focusing on
database and class diagrams.

The idea behind dia2code is to provide both these conversions
within one program, offering more than just one target language,
all under OpenGL licence. 

Dia2Code was designed to be modular, allowing users to quite
easily add more target languages or modify the output to their
liking.


...         ''') 
    
    arg_parser.add_argument("mode", help="\"d\" - UML to database | \"c\" - UML to classes.")
    arg_parser.add_argument("src", help="Source DIA xml file path. Note: The Dia diagram must be saved without compression.")
    arg_parser.add_argument("dst", help="Destination folder path.")
    
       
    arg_parser.add_argument("-l", "--language", help="Language of the final code [DEFAULT: mysql|c++].\n")    
    arg_parser.add_argument("-n", "--name", help="Result file name (without extension) [DEFAULT: source file name].") 
    arg_parser.add_argument("-p", "--print", help="\"t\" - terminal | \"f\" - file [DEFAULT] | \"ff\" - one class per file [classes only]\
                            (File names composed of given file name and class names.)")

    
    return arg_parser.parse_args()

        

if __name__ == "__main__":
    
    main()