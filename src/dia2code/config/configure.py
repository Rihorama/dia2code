#!/usr/bin/python3

import argparse

def parse_arguments():
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
...
...
...    This program's purpose is to convert UML diagrams created in
...   the diagramming software Dia to a valid code, focusing on
...    database and class diagrams.
...
...    The idea behind dia2code is to provide both these conversions
...    within one program, offering more than just one target language,
...   all under OpenGL licence. 
...
...    Dia2Code was designed to be modular, allowing users to quite
...    easily add more target languages or modify the output to their
...    liking.
...
...         ''') 
    
    arg_parser.add_argument("mode", help="\"d\" - UML to database | \"c\" - UML to classes.")
    arg_parser.add_argument("src", help="Source DIA xml file path.")
    #arg_parser.add_argument("dst", help="Destination folder path.")
    
    arg_parser.add_argument("-dst", "--destination", help="Destination folder path [DEFAULT: current folder.]\n")   
    arg_parser.add_argument("-l", "--language", help="Language of the final code [DEFAULT: mysql|c++].\n")    
    arg_parser.add_argument("-n", "--name", help="Result file name (without extension) [DEFAULT: source file name].") 
    arg_parser.add_argument("-p", "--print", help="\"t\" - terminal | \"f\" - file [DEFAULT] | \"ff\" - one class per file [classes only]\
                            (File names composed of given file name and class names.)")

    
    return arg_parser.parse_args()