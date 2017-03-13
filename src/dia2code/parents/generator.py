#!/usr/bin/python3

from abc import ABCMeta, abstractmethod


class Generator:
    #Abstract class to be parent to all uml parsers
    
    __metaclass__ = ABCMeta     
    
    @abstractmethod
    def generate(self): pass
    