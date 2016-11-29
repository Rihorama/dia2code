

class ErrorHandler:
    
    def __init__(self):
        
        #dictionary for exit codes
        self.exit_code = {}
        
        self.exit_code["diagram"] = 1
        self.exit_code["xml"] = 2
        
        
        #dictionary for error print quotes
        self.err_dict = {}
        
        self.err_dict["dia:ref_not_closed"] = "In dia xml file: reference not connected on one or both sides. \nCheck your diagram for connections not properly connected to their tables."
        self.err_dict["dia:table_name_missing"] = "In dia xml file: incomplete table element. Name attribute missing."
        
        
        
    def print_error(self,index):
        
        string = "ERROR - " + self.err_dict[index]
        print string