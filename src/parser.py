# -*- coding: utf-8 -*-
import sys
import codecs
from xml.sax import make_parser, handler

class Concept:
    def __init__(self):
        self.concept_name = ""
        self.cocept_value = ""

class Date(Concept):
    type = "Date"

class Containter:
    def __init__ (self):
        concept_name = Concept()
        childs = []
    
class DicomParser(handler.ContentHandler):

    def __init__(self):
        self.tree_level=0
        self.organs = {}
        self.injuries = {}
        self.concept = Concept()
        self.buffer = '';
        self.inData = False;
    
    def startElement(self, name, attrs):
        if (name == "CONTAINER"):
            self.tree_level +=  1
            print 'Tree level {0}'.format(self.tree_level)
        if (name == "CONCEPT_NAME"):
            self.inData = True
            self.buffer = ""

    def endElement(self,name):
        if (name == "CONTAINER"):
            print "This is the end: ", self.tree_level
            self.tree_level -= 1
        if (name == "CONCEPT_NAME"):
            self.inData = False
            #Cuidado con los carácters utf-8 que no se ven bien
            print u'Concept_name : {0}'.format(self.buffer)

    def characters(self,chars):
        if (self.inData):
            self.buffer += chars

parser = make_parser()
parser.setContentHandler(DicomParser())
#parser.parse(codecs.open(sys.argv[1],mode='r', encoding='utf-8'))
parser.parse(open(sys.argv[1],"r"))
