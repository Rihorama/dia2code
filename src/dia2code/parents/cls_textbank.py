#!/usr/bin/python3

from abc import ABCMeta, abstractmethod
from parents.base_textbank import BaseTextBank


class ClassTextBank(BaseTextBank):  
    #Abstract class to be parent to all class text banks
    
    __metaclass__ = ABCMeta    
    
    #the following methods are called by cls_generator and thus MUST be
    #implemented in every textbank used for generating code from a class diagram.
    
    @abstractmethod
    def startClass(self,cls): pass

    @abstractmethod
    def addAttribute(self,attr): pass

    @abstractmethod
    def addMethod(self,mtd): pass

    @abstractmethod
    def addAssociation(self,assoc): pass

    @abstractmethod
    def wrapUpClass(self): pass        #returns string
