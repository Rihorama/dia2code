#!/usr/bin/python3

from abc import ABCMeta, abstractmethod
from parents.base_textbank import BaseTextBank


class DatabaseTextBank(BaseTextBank):  
    #Abstract class to be parent to all database text banks
    
    __metaclass__ = ABCMeta    
    
    
    #the following methods are called by db_generator and thus MUST be
    #implemented in every textbank used for generating code from a database diagram.
    
    @abstractmethod
    def startEntity(self, ent): pass

    @abstractmethod
    def addAttribute(self,attr): pass

    @abstractmethod
    def wrapUpEntity(self): pass