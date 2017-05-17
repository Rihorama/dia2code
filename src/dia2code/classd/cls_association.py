#!/usr/bin/python3

import error_handler


class Association:
    
    assoc_type_dict = {0 : "association",
                       1 : "aggregation",
                       2 : "composition"}
    
    direction_dict = {0 : "none",
                      1 : "A to B",
                      2 : "B to A"}
    
    ret_val_dict = {"single"  :  1,  #single multiplicity return value
                    "variable":  0,  #variable multiplicity return value
                    "error"   : -1}

  
    def __init__(self):
        
        self.assoc_type = None
        self.direction = None            #taken from direction_dict
        self.err = error_handler.ErrorHandler()
        
        self.A_dict = {"class"        : None,
                       "role"         : None,
                       "multiplicity" : None,
                       "visibility"   : None,
                       "arrow_visible": None}
        
        self.B_dict = {"class"        : None,
                       "role"         : None,
                       "multiplicity" : None,
                       "visibility"   : None,
                       "arrow_visible": None}


    
    def whichMemberIs(self,cls):
        """Gets a class and decides whether it's A or B member in
        this association.
        
        Args:
            cls (cls_class.Class) - class whose membership is to be determined
            
        Returns:
            String "A" for A-member, "B" for B-member
        """
        
        if cls == self.A_dict["class"]:
            return "A"
        
        else: #B_class
            return "B"

    
    
    def isSingleMultiplicity(self,member):
        """ First conducts a test if the given multiplicity
        is valid ("1", "1..15", "1..*" etc) and if yes, returns
        True for single value ("1") and false for variable with
        multiple possible values ("3", "1..15" etc.). No multiplicity
        counts as single value.
        
        Used to decide whether the representing attribute should
        be single-value or multi-value (list,vector...)
        
        NOTE: Notations such as 1..n or m..n are not supported. The only
        non-digit character allowed is asterisk *.
        
        Args:
            member (String) - A letter stating which member multiplicity we examine (A | B)
            
        Returns:
            int - 0 for single multiplicity, 1 for variable multiplicity, -1 for error.
        """
        
        #setting the right member's multiplicity
        m = None
        m_class = None        
        
        
        if member == "A":
            m = self.A_dict["multiplicity"]
            m_class = self.A_dict["class"]
            
        elif member == "B":
            m = self.B_dict["multiplicity"]
            m_class = self.B_dict["class"]
            
        else:
            err.printError("generator:runtime")
            e_code = err.exit_code["generator"]
                
            exit(e_code)
            #This shouldn|t happen if the code is written properly
            #will result in a dirty exit            
        

        if m.isdigit() and int(m) == 1: #single
            return self.ret_val_dict["single"]
        
        elif m == "":                   #none counts as single
            return self.ret_val_dict["single"]
        
        elif m.isdigit() or m == "*":  #variable
            return self.ret_val_dict["variable"]
        
        else:           #either variable or wrong -> error      
            x = m.split("..") #if correct, we get list of two
            
            if not len(x) == 2: #not a list of two, it's wrong                                  #
                self.err.printErrorTwovar("generator:wrong_multiplicity", m, m_class.name)      #
                e_code = self.err.exit_code["generator"]                                        #
                                                                                                #
                exit(e_code)                                                                    #
                #TODO: Solve these errors earlier, this is dirty, does not close file in code
            
            elif not (x[0].isdigit and (x[1].isdigit or x[1] == "*")):                          #
                self.err.printErrorTwovar("generator:wrong_multiplicity", m, m_class.name)      #
                e_code = self.err.exit_code["generator"]                                        #
                                                                                                #
                exit(e_code)                                                                    #
                #TODO: Solve these errors earlier, this is dirty, does not close file in code
                
            else: #either both are decimal or first is decimal, second is * => that's correct
                return self.ret_val_dict["variable"]
                

                
    
        
    def printMe(self):
        """A simple print method for debugging purposes.
        """
        
        print("  CONNECTION {}".format(self))
        print("  Name: {}".format(self.name))
        print("  Type: {}".format(self.assoc_type))
        print("  Participant A: name: {}, role: {}, multiplicity:" 
              " {}, visibility: {}".format(self.A_dict["class"].name, self.A_dict["role"],
                                           self.A_dict["multiplicity"],self.A_dict["visibility"]))
              
        print("  Participant B: name: {}, role: {}, multiplicity:"
              " {}, visibility: {}".format(self.B_dict["class"].name, self.B_dict["role"],
                                           self.B_dict["multiplicity"],self.B_dict["visibility"]))
        print("  ###############")
