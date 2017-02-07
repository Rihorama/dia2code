import sys

class ErrorHandler:
    
    def __init__(self):
        
        #dictionary for exit codes
        self.exit_code = {}
        
        self.exit_code["parameter"] = 1
        self.exit_code["xml"] = 2
        self.exit_code["parser"] = 3
        self.exit_code["generator"] = 4
        
        
        #dictionary for error print quotes
        self.err_dict = {}
        
        self.err_dict["parameter:wrong_mode"] = "Wrong \"mode\" parameter (\"{}\"). Accepted parameters: \"d\" for Database, \"c\" for Class. Type -h,--help for help."
        self.err_dict["parameter:bad_source"] = "Given source file (\"{}\") does not exist."
        self.err_dict["parameter:bad_destination"] = "Given destination folder path (\"{}\") is not valid."
        self.err_dict["parameter:unsupported_language"] = "Given target language (\"{}\") is not supported in chosen mode (\"{}\")."
        self.err_dict["parameter:wrong_print"] = "Given printing option (\"{}\") not recognized. Accepted options: \"t\" for Terminal, \"f\" for File, \"ff\" for one file per class.\
        Type -h,--help for help."
        
        self.err_dict["dia:ref_not_closed"] = "In dia xml file: reference not connected on one or both sides. \nCheck your diagram for connections not properly connected to their tables."
        self.err_dict["dia:table_name_missing"] = "In dia xml file: incomplete table element. Name attribute missing."
        self.err_dict["dia:class_name_missing"] = "In dia xml file: incomplete class element. Name attribute missing."
        
        self.err_dict["parser:class_wrong_dia"] = "In class diagram parser: Your dia xml file does not contain elements required for dia2code to work in the class mode (\"UML - Class\"). Did you perhaps mean to work in the database mode? Type -h, --help for help."
        self.err_dict["parser:database_wrong_dia"] = "In ER diagram parser: Your dia xml file does not contain elements required for dia2code to work in the database mode (\"Database - Table\"). Did you perhaps mean to work in the class mode? Type -h, --help for help."
        
        self.err_dict["generator:wrong_multiplicity"] = "In cls_association.py: Encountered invalid association multiplicity ({}) for class {}. Allowed format: \"x\", \"x..y\" or \"*\" where x is decimal, y is decimal or *."        
        self.err_dict["generator:runtime"] = "In cls_association.py: Runtime error. Blame cls_generator.py."
        
        
        
    def print_error(self,index):
        
        string = "ERROR - " + self.err_dict[index]
        print(string, file=sys.stderr)
        
    
    def print_error_onevar(self,index,var1):
        
        s = self.err_dict[index].format(var1)
        string = "ERROR - {}".format(s)
        
        print(string, file=sys.stderr)
        
    
    def print_error_twovar(self,index,var1,var2):
        
        s = self.err_dict[index].format(var1,var2)
        string = "ERROR - {}".format(s)
        
        print(string, file=sys.stderr)