import sys

class ErrorHandler:
    
    def __init__(self):
        
        #dictionary for exit codes
        self.exit_code = {}
        
        self.exit_code["parameter"] = 1
        self.exit_code["xml"] = 2
        self.exit_code["diagram"] = 2
        self.exit_code["parser"] = 3
        self.exit_code["generator"] = 4
        
        
        #dictionary for error print quotes
        self.err_dict = {}

        #------- PARAMETER ERRORS -------- 

        # WRONG MODE
        self.err_dict["parameter:wrong_mode"] = "Wrong \"mode\" parameter (\"{}\"). Accepted parameters: \"d\" for Database,\
        \"c\" for Class. Type -h,--help for help."
        
        # BAD SOURCE
        self.err_dict["parameter:bad_source"] = "Given source file (\"{}\") does not exist."
        
        # BAD DESTINATION
        self.err_dict["parameter:bad_destination"] = "Given destination folder path (\"{}\") is not valid."
        
        # UNSUPPORTED LANGUAGE
        self.err_dict["parameter:unsupported_language"] = "Given target language (\"{}\") is not supported in chosen mode (\"{}\")."
        
        # WRONG PRINT
        self.err_dict["parameter:wrong_print"] = "Given printing option (\"{}\") not recognized. Accepted options: \"t\" for Terminal,\
        \"f\" for File, \"ff\" for one file per class.\ Type -h,--help for help."
      
        
        
        #------- DIAGRAM ERRORS --------
        
        # REFERENCE NOT CLOSED
        self.err_dict["dia:ref_not_closed"] = "In dia xml file: reference not connected on one or both sides.\n\
        \nCheck your diagram for connections not properly connected to their tables."
        
        # TABLE NAME MISSING
        self.err_dict["dia:table_name_missing"] = "In dia xml file: incomplete table element. Name attribute missing."
        
        # CLASS NAME MISSING
        self.err_dict["dia:class_name_missing"] = "In dia xml file: incomplete class element. Name attribute missing."
        
        # DIRECTION COLLISION
        self.err_dict["dia:direction_collision"] = "Association between classes \"{}\" and \"{}\" contains colliding direction data.\n\
        Displayed arrows do not correspond with the set direction. Synchronization of the two is mandatory due to an existing\n\
        direction bug in Dia UML XML. For this program to generate a correct code, we reccomend setting Direction to None and leaving\n\
        only the arrows. For undirected association (= both sides know about the other) set Direction to None and both arrow\n\
        visibility to No."
        
        
        
        #------- PARSER ERRORS --------
        
        # WRONG DIA FILE FOR CLASS PARSER
        self.err_dict["parser:class_wrong_dia"] = "In class diagram parser: Your dia xml file does not contain\
        elements required for dia2code to work in the class mode (\"UML - Class\").\
        Did you perhaps mean to work in the database mode? Type -h, --help for help."
        
        # WRONG DIA FOR DATABASE PARSER
        self.err_dict["parser:database_wrong_dia"] = "In ER diagram parser: Your dia xml file does not contain\
        elements required for dia2code to work in the database mode (\"Database - Table\"). Did you perhaps mean\
        to work in the class mode? Type -h, --help for help."
        
        
        
        #------- GENERATOR ERRORS --------
        
        # WRONG MULTIPLICITY
        self.err_dict["generator:wrong_multiplicity"] = "In cls_association.py: Encountered invalid association\
        multiplicity (\"{}\") for class \"{}\". Allowed format: \"x\", \"x..y\" or \"*\" where x is decimal, y is decimal or *."
        
        # RUNTIME ERROR
        self.err_dict["generator:runtime"] = "In cls_association.py: Runtime error. Blame cls_generator.py."
        
        
        #---------------------------------
        
        
        
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