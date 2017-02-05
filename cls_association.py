#!/usr/bin/python3

import error_handler


class Association:
    
    assoc_type_dict = {0 : "association",
                       1 : "aggregation",
                       2 : "composition"}
    
    direction_dict = {0 : "none",
                      1 : "A to B",
                      2 : "B to A"}

  
    def __init__(self):
        
        self.assoc_type = None
        
        self.A_class = None              #connection was initialized by clicking on this class        
        self.A_role = None               #role name . if not present -> empty string
        self.A_multiplicity = None       #multiplicity of association on A side
        self.A_visibility = None         #public/private/protected/implementation
        
        self.B_class = None              #connection was finished by clicking on this class
        self.B_role = None
        self.B_multiplicity = None
        self.B_visibility = None
        
        self.err = error_handler.ErrorHandler()
        
        self.A_dict = {}
        
        self.B_dict = {}
        
        #TODO: If I ever eel suicide enough, I might remove the single attributes
        #      and fill the dictionaries right away. And correct everything that
        #      works with it, yay...

        
    
    def fillDictionaries(self):
        """For the purpose of correctly turning this association into code
        we need to fill self.A_dict and self.B_dict with the already filled
        vallues of both roles. This method does just that.
        """
        
        self.A_dict = {"class"        : self.A_class,
                       "role"         : self.A_role,
                       "multiplicity" : self.A_multiplicity,
                       "visibility"   : self.A_visibility}
        
        self.B_dict = {"class"        : self.B_class,
                       "role"         : self.B_role,
                       "multiplicity" : self.B_multiplicity,
                       "visibility"   : self.B_visibility}
    
    
    
    def whichMemberIs(self,cls):
        """Gets a class and decides whether it's A or B member in
        this association.
        
        Args:
            cls (cls_class.Class) - class whose membership is to be determined
            
        Returns:
            String "A" for A-member, "B" for B-member
        """
        
        if cls == self.A_class:
            return "A"
        
        else: #B_class
            return "B"

    
    
    def isSingleMultiplicity(self,member):
        """ First conducts a test if the given multiplicity
        is valid ("1", "1..15", "1..*" etc) and if yes, returns
        True for single value ("1") and false for variable with
        multiple possible values ("3", "1..15" etc.).
        
        Used to decide whether the representing attribute should
        be single-value or multi-value (list,vector...)
        
        Args:
            member (String) - A letter stating which member multiplicity we examine (A | B)
            
        Returns:
            int - 0 for single multiplicity, 1 for variable multiplicity, -1 for error.
        """
        
        #setting the right member's multiplicity
        m = None
        m_class = None
        
        
        
        if member == "A":
            m = self.A_multiplicity
            m_class = self.A_class
            
        elif member == "B":
            m = self.B_multiplicity
            m_class = self.B_class
            
        else:
            err.print_error("generator:runtime")
            e_code = err.exit_code["generator"]
                
            exit(e_code)
            #This shouldn|t happen if the code is written properly
            #will result in a dirty exit
            
        

        if m.isdigit() and int(m) == 1: #single
            return True
        
        elif m.isdigit() or m == "*":  #variable
            return False
        
        else:           #either variable or wrong -> error      
            x = m.split("..") #if correct, we get list of two
            
            if not len(x) == 2: #not a list of two, it's wrong
                err.print_error_twovar("generator:wrong_multiplicity",m,m_class.name)
                e_code = err.exit_code["generator"]
                
                exit(e_code)
                #TODO: Solve these errors earlier, this is dirty, does not close file in code
            
            elif not (x[0].isdigit and (x[1].isdigit or x[1] == "*")):
                err.print_error_twovar("generator:wrong_multiplicity",m,m_class.name)
                e_code = err.exit_code["generator"]
                
                exit(e_code)
                #TODO: Solve these errors earlier, this is dirty, does not close file in code
                
            else: #either both are decimal or first is decimal, second is * => that's correct
                return self.ret_val_dict["variable"]
                

                
    
        
    def print_me(self):
        """A simple print method for debugging purposes.
        """
        
        print("  CONNECTION {}".format(self))
        print("  Name: {}".format(self.name))
        print("  Type: {}".format(self.assoc_type))
        print("  Participant A: name: {}, role: {}, multiplicity: {}, visibility: {}".format(self.A_class.name, self.A_role,
                                                                                             self.A_multiplicity,self.A_visibility))
        print("  Participant B: name: {}, role: {}, multiplicity: {}, visibility: {}".format(self.B_class.name, self.B_role,
                                                                                             self.B_multiplicity,self.B_visibility))
        print("  ###############")
