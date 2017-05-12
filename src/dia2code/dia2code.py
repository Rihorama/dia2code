#!/usr/bin/env python3

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
    dict_name = ParserFactory.get_dict_name(mode)
    dict_full = "parser.{}".format(dict_name)
    
    generator = GeneratorFactory.pick(mode,dst,file_name,language,print_option)
    
    parser.parse()
    
    if mode == "database":
        generator.generate(parser.table_dict)
        
    elif mode == "class":
        generator.generate(parser.class_dict)
        
    print("Code generating sucessful!")
        

if __name__ == "__main__":
    
    main()