# -*- coding: utf-8 -*-
import sys
import codecs
from xml.sax import make_parser, handler

STRINGS_XML = "strings.xml"

class Property:
    def __init__(self):
        self.max_card = 0
        self.min_card = 0
        self.max_val = 0
        self.min_val = 0
        self.condition = ""

class Concept:
    def __init__(self):
        self.concept_name = ""
        self.cocept_value = ""

class Data_type:
    def __init__(self):
        self.type = ""
        self.concept = Concept()
        self.properties = []

class Date(Data_type):
    def __init__(self):
        self.type = "date"

class Text(Data_type):
    def __init__(self):
        self.type = "text"

class Num(Data_type):
    def __init__(self):
        self.type = "num"

class Containter:
    def __init__ (self):
        concept_name = Concept()
        childs = []

class Report:
    def __init__(self):
        report_type = Concept()
        #It will be a list of data types
        report_properties = []
        
        
class DicomParser(handler.ContentHandler):

    def __init__(self):
        # Internal variables
        self.tree_level=0
        self.buffer = ''
        self.inData = False;
        self.inType = False;
        self.inConcept = False
        # Report-related variables
        self.organs = {}
        self.injuries = {}
        self.concept = Concept()
        # XML files 
        self.xml_files = {}

    def startDocument(self, strings_xml_filename=STRINGS_XML):
        xml_strings = open(strings_xml_filename, 'w')
        self.xml_files[strings_xml_filename]=xml_strings
        for xml_file in self.xml_files.values():
            xml_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        xml_strings.write("<resources>\n")

    def startElement(self, name, attrs, strings_xml_filename=STRINGS_XML):
        if (name == "CONTAINER"):
            self.tree_level +=  1
            print 'Tree level {0}'.format(self.tree_level)
            #Report level
            if (self.tree_level==1):
                self.xml_files[strings_xml_filename].write("\n\t<!-- Report -->\n")
            #Organs level
            if (self.tree_level==2):
                self.xml_files[strings_xml_filename].write("\n\n\t<!-- Organ -->\n")
            #Lesions level
            if (self.tree_level==3):
                self.xml_files[strings_xml_filename].write("\n\n\t<!-- Lesions -->\n")
        if (name == "CHILDS"): 
            #Report level
            if (self.tree_level==1):
                self.xml_files[strings_xml_filename].write("\n\t<!-- Report attributes-->\n")
            #Organs level
            if (self.tree_level==2):
                self.xml_files[strings_xml_filename].write("\n\t<!-- Organ attributes-->\n")
            #Lesions level
            if (self.tree_level==3):
                self.xml_files[strings_xml_filename].write("\n\t<!-- Lesion attributes-->\n")
        if (name == "CONCEPT_NAME"):
            self.inConcept = True
        if (name == "DATE"):
            self.inType = True
        if (name == "CODE_VALUE" or "CODE_MEANING"):
            self.inData = True
            self.buffer = ""

    def endElement(self,name,strings_xml_filename=STRINGS_XML):
        if (name == "CONTAINER"):
            print "This is the end: ", self.tree_level
            self.tree_level -= 1
        if (name == "CODE_VALUE"):
            self.inData = False
            self.concept.concept_value = self.buffer
            print u'Code_value : {0}'.format(self.concept.concept_value)
        if (name == "CODE_MEANING"):
            self.inData = False
            self.concept.concept_name = self.buffer
            print u'Code_meaning : {0}'.format(self.concept.concept_name)
        if (name == "CONCEPT_NAME"):
            self.inConcept = False
            self.xml_files[strings_xml_filename].write(
                u"\t<string name=\"{0}\">{1}</string>\n".
                format(self.concept.concept_value,self.concept.concept_name).encode('utf-8'))
            #Cuidado con los carácteres utf-8 que no se ven bien
            #print u'Concept_name : {0}'.format(self.concept)

    def characters(self,chars):
        if (self.inData):
            self.buffer += chars

    def endDocument(self,strings_xml_filename=STRINGS_XML):
        self.xml_files[strings_xml_filename].write("\n</resources>")
        for xml_file in self.xml_files.values():
            print xml_file
            xml_file.close()

parser = make_parser()
parser.setContentHandler(DicomParser())
#parser.parse(codecs.open(sys.argv[1],mode='r'encoding='utf-8'))
dicom_xml = open(sys.argv[1],"r") 
parser.parse(dicom_xml)
dicom_xml.close()
