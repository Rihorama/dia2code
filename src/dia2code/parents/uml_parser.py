#!/usr/bin/python3

from abc import ABCMeta, abstractmethod


class UmlParser:
    #Abstract class to be parent to all uml parsers
    
    __metaclass__ = ABCMeta     
    
    @abstractmethod
    def parse(self): pass
    