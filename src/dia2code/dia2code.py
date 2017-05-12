#!/usr/bin/env python3

from config.configure         import parseArguments
import config.args_checker    as checker
from factory.factories        import ParserFactory,GeneratorFactory


def main():
    
    #setting argparse and parsing arguments
    args = parseArguments()
    
    mode         =  checker.checkMode(args.mode)
    src          =  checker.checkSrc(args.src)
    dst          =  checker.checkDst(args.destination)
    language     =  checker.checkLanguage(args.language, mode)
    file_name    =  checker.checkFilename(args.name, src)
    print_option =  checker.checkPrint(args.print)
    
    
    parser = ParserFactory.pick(mode,src)
    dict_name = ParserFactory.getDictName(mode)
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