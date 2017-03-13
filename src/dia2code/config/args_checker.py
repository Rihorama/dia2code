#!/usr/bin/python3

import os.path
import databased.db_generator           as db_generator
import classd.cls_generator             as cls_generator

from error_handler import ErrorHandler

err = ErrorHandler()


def check_mode(mode):
    """Takes argument passed as mandatory "mode" argument and
    checks if it's either "d" for database or "c" for class.
    Returns string representing the mode as full word ("database"
    or "class". Prints error message and exits if wrong mode.
    
    Args:
        mode (string) - Argument passed as "mode".
        
    Returns:
        String, either "database" or "class" based on the mode.
    """
    
    if mode == "d":
        s = "database"
        
    elif mode == "c":
        s = "class"
        
    else:                                                           ###
        err.print_error_onevar("parameter:wrong_mode",mode)         ###
        e_code = err.exit_code["parameter"]                         ###
                                                                    ###
        exit(e_code)                                                ###
        
    return s
    

def check_src(src): 
    """Takes argument passed as mandatory "src" argument and checks
    if the given path exists. If yes, returns the path as it is.
    Else prints an error message.
    
    Args:
        src (string) - Argument passed as "src".
        
    Returns:
        Unchanged src if file exists.
    """
    
    if not os.path.exists(src):                                     ###    
        err.print_error_onevar("parameter:bad_source",src)          ###
        e_code = err.exit_code["parameter"]                         ###
                                                                    ###
        exit(e_code)                                                ###
        
    return src
    
def check_dst(dst):
    """Takes argument passed as optional "dst" argument
    (empty string if argument not present). If empty, sets
    the default destination path to the current folder ("./").
    Else checks if the given path exists, eventually adds "/"
    at the end of the string to unify the format for future usage.
    Prints error if the path does not exist."
    
    Args:
        dst (string) - Argument passed as "mode". Empty if not used.
        
    Returns:
        String with path of the destination folder.
    """    
    
    #Default: current folder "./"
    if dst == None:
        dst = "./"
    
    if not dst[-1] == "/":
        dst = "{}/".format(dst)
        
    if not os.path.exists(dst):                                     ###    
        err.print_error_onevar("parameter:bad_destination",dst)     ###
        e_code = err.exit_code["parameter"]                         ###
                                                                    ###
        exit(e_code)                                                ###
        
    return dst
        

def check_language(language,mode):
    """Takes argument passed as optional "language" argument
    (empty string if argument not present). If empty, sets
    the default language to either "c++" or "mysql" depending on
    the given mode. If the given language is among supported
    languages, returns the string unchanged. Prints error if
    the language not supported."
    
    Args:
        language (string) - Argument passed as "language". 
                            Empty if not used.
        mode (string) - "database" or "class"
        
    Returns:
        String with chosen language.
    """ 

    flag_db =  language not in db_generator.DatabaseGenerator.supported_language_dict.keys()
    flag_cls = language not in cls_generator.ClassGenerator.supported_language_dict.keys()    
    
    
    #default database target language
    if language == None and mode == "database":
        language = "mysql"        
        
    #default class target language  
    elif language == None and mode == "class":        
        language = "c++"        
        
    #language given but not supported
    elif (mode == "database" and flag_db) or (mode == "class" and flag_cls):    ###        
        err.print_error_twovar("parameter:unsupported_language",language,mode)  ###
        e_code = err.exit_code["parameter"]                                     ###
                                                                                ###
        exit(e_code)                                                            ###
        
    return language
    

def check_filename(name,src):
    """Takes argument passed as optional "name" argument
    (empty string if argument not present). If empty, sets
    the default result file name to the source file name.
    If present, returns the file_name unchanged.
    
    Args:
        name (string) - Argument passed as "name". Empty if not used.
        
    Returns:
        String with source file name.
    """ 

    file_name = ""

    if name == None:
        file_name = os.path.basename(src)       #name with extension
        file_name = file_name.split(".")[0]     #all prior to first comma
        
    else:
        file_name = name 
        
    return file_name
        
 
def check_print(prnt):
    """Takes argument passed as optional "print" argument
    (empty string if argument not present). If empty, sets
    the default option to "f" - print to one file. Other valid
    options for this argument are "t" - terminal and 
    "ff" - one class per file (class mode only). Prints error
    message if unsupported print option given.
    
    Args:
        language (prnt) - Argument passed as "print". 
                          Empty if not used.
        
    Returns:
        String with chosen print option.
    """

    valid_options = ["t","f","ff"]
    print_option = None
    
    if prnt == None:
        print_option = "f"
        
    elif not prnt == None and prnt in valid_options:
        print_option = prnt
        
    else:                                                               ###
        err.print_error_onevar("parameter:wrong_print",args.print)      ###
        e_code = err.exit_code["parameter"]                             ###
                                                                        ###
        exit(e_code)                                                    ###
        
    return print_option