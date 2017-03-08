#!/usr/bin/python3


import databased.db_uml_parser        as db_uml_parser
import databased.db_generator         as db_generator

import classd.cls_uml_parser  as cls_uml_parser
import classd.cls_generator   as cls_generator

from config.configure         import parse_arguments
import config.args_checker    as checker
from factory.factories        import ParserFactory,GeneratorFactory


def main():
    
    #setting argparse and parsing arguments
    args = parse_arguments()
    
    mode         =  checker.check_mode(args.mode)
    src          =  checker.check_src(args.src)
    dst          =  checker.check_dst(args.destination)
    language     =  checker.check_language(args.language,mode)
    file_name    =  checker.check_filename(args.name,src)
    print_option =  checker.check_print(args.print) 
    
    
    parser = ParserFactory.pick(mode,src)
    generator = GeneratorFactory.pick(mode,dst,file_name,language,print_option)
    
    parser.parse()
    generator.generate(parser.table_dict)

        

if __name__ == "__main__":
    
    main()