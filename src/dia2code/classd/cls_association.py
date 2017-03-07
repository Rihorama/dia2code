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

    
    
    def correctDirection(self):
        """This method compares the given direction (self.direction)
        with individually set arrow visibility (as these two elements
        are not linked). This action needs to be taken because
        of a bug found in the way direction displays in Dia. This bug
        might lead the user to enter invalid direction info to
        achieve the correct visual appearance. 
        
        This method usage doesn't entirely eliminate the chance
        of undesired data coming through. It only works in a directed
        association if the user uses both direction and individual arrows.
        
        If the user uses only direction and leaves both arrows set to No,
        there is no way to determine if the data coming correspond to
        user's intentions or not.
        
        Returns:
            bool - True if direction and arrows correspond, False otherwise.
        """
        
        #arrow only points to A
        directed_flag_A = self.A_dict["arrow_visible"] and not self.B_dict["arrow_visible"]
        #arrow only points to B
        directed_flag_B = self.B_dict["arrow_visible"] and not self.A_dict["arrow_visible"]
        #both arrows visible
        directed_flag_both = self.B_dict["arrow_visible"] and self.A_dict["arrow_visible"]
        
        #arrow points to A, direction says we point to B
        collision_A = directed_flag_A and self.direction == "A to B"
        #arrow points to B, direction says we point to A
        collision_B = directed_flag_B and self.direction == "B to A"
        #arrow points to both A and B but direction suggests one-sided association
        collision_both = directed_flag_both and not self.direction == "none"
        
        #if either collission happened => return False
        if (collision_A or collision_B or collision_both):
            return False
        
        else:
            return True
        
        
    
    
    
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
            err.print_error("generator:runtime")
            e_code = err.exit_code["generator"]
                
            exit(e_code)
            #This shouldn|t happen if the code is written properly
            #will result in a dirty exit
            
        

        if m.isdigit() and int(m) == 1: #single
            return True
        
        elif m == "":                   #none counts as single
            return True
        
        elif m.isdigit() or m == "*":  #variable
            return False
        
        else:           #either variable or wrong -> error      
            x = m.split("..") #if correct, we get list of two
            
            if not len(x) == 2: #not a list of two, it's wrong                                  #
                self.err.print_error_twovar("generator:wrong_multiplicity",m,m_class.name)      #
                e_code = self.err.exit_code["generator"]                                        #
                                                                                                #
                exit(e_code)                                                                    #
                #TODO: Solve these errors earlier, this is dirty, does not close file in code
            
            elif not (x[0].isdigit and (x[1].isdigit or x[1] == "*")):                          #
                self.err.print_error_twovar("generator:wrong_multiplicity",m,m_class.name)      #
                e_code = self.err.exit_code["generator"]                                        #
                                                                                                #
                exit(e_code)                                                                    #
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
