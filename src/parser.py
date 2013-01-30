# -*- coding: utf-8 -*-
import sys
import codecs
from xml.sax import make_parser, handler

STRINGS_XML = "strings.xml"

class Property(object):
    def __init__(self):
        self.max_cardinality = 0
        self.min_cardinality = 0
        self.max_value = 0
        self.min_value = 0
        self.condition = ""


class Concept(object):
    def __init__(self,concept_name="",concept_value=-1):
        self.concept_name = concept_name
        self.concept_value = concept_value
    def __str__(self):
        return u"Concept name: {0} - Concept value: {1}".format(self.concept_name, self.concept_value).encode('utf-8')
    def __repr__(self):
        return u"Concept name: {0} - Concept value: {1}".format(self.concept_name, self.concept_value).encode('utf-8')


class Data_type(object):
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


class Containter(object):
    def __init__ (self):
        self.concept_name = Concept()
        self.childs = []


class Container(object):
    def __init__(self,concept=Concept(),level=-1,open_level=True, parent=Concept()):
        self.concept = Concept(concept.concept_name,concept.concept_value)
        #A list of attributes (date, num, text)
        self.attributes = []
        self.tree_level = level
        self.open = open_level
        self.parent = parent
    def has_concept(self):
        return (self.concept.concept_name != "")
    #Si lo cambias a un diccionario añadir el atributo será más rápido
    def add_attribute(self,attribute):
        self.attributes.append(attribute)
    def __repr__(self):
        return u"L{0}: {1} ({2}) p({3}){4}\n".format(
            self.tree_level,self.concept.concept_name, len(self.attributes),
            self.parent.concept_name if (self.parent!=None) else "", 
            "..." if self.open else "" ).encode('utf-8')

class Report(object):
    def __init__(self):
        # tree_level: Level()
        self.container = {}
        
        
class DicomParser(handler.ContentHandler):

    def __init__(self):
        # Internal variables
        self.tree_level = 0
        self.child_level = 0
        self.buffer = ''
        self.inData = False
        self.inType = False
        self.inConcept = False
        self.inLevel = False
        self.current_attribute = None
        # Report-related variables
        self.report = []
        self.concept = None
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
            #if (self.currentLevel != None):
            #    self.report.append (self.currentLevel)
            self.tree_level += 1
            self.inLevel = True
            #self.currentLevel = Level()
            #self.currentLevel.level = self.tree_level
            print '* Tree level {0}'.format(self.tree_level)
            #Report level
            if (self.tree_level==1):
                self.xml_files[strings_xml_filename].write("\n\t<!-- Report -->\n")
            #Organs level
            elif (self.tree_level==2):
                self.xml_files[strings_xml_filename].write("\n\n\t<!-- Organ -->\n")
            #Lesions level
            elif (self.tree_level==3):
                self.xml_files[strings_xml_filename].write("\n\n\t<!-- Lesions -->\n")
            #if (self.child_level == self.tree_level):   
        if (name == "CHILDS"): 
            self.child_level += 1
            self.inLevel = False
            print '* Child level {0}'.format(self.child_level)
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
            self.concept = Concept()
        if (name == "DATE"):
            self.inType = True
            self.current_attribute = Date()        
        if (name == "TEXT"):
            self.inType = True
            self.current_attribute = Text()
        if (name == "NUM"):
            self.inType = True
            self.current_attribute = Num()
        if (name == "CODE_VALUE" or "CODE_MEANING"):
            self.inData = True
            self.buffer = ""


    def add_attribute(self):
        for level in self.report:
            if ((level.tree_level == self.child_level) and level.open):
                level.attributes.append(self.current_attribute)
                return True
        return False

    def close_level(self):
        for level in self.report:
            if ((level.tree_level == self.child_level) and level.open):
                level.open = False
                print self.report
                return True
        return False

    def return_parent(self):
        for level in self.report:
            if(level.tree_level == self.tree_level-1 and level.open):
                return level.concept
        return None

    def endElement(self,name,strings_xml_filename=STRINGS_XML):
        if (name == "CODE_VALUE"):
            self.inData = False
            self.concept.concept_value = self.buffer
            #print u'Code_value : {0}'.format(self.concept.concept_value)
        if (name == "CODE_MEANING"):
            self.inData = False
            self.concept.concept_name = self.buffer
            #print u'Code_meaning : {0}'.format(self.concept.concept_name)
        if (name == "CONCEPT_NAME"):
            self.inConcept = False
            #self.concepts.append(self.concept)
            self.xml_files[strings_xml_filename].write(
                u"\t<string name=\"{0}\">{1}</string>\n".
                format(self.concept.concept_value,self.concept.concept_name).encode('utf-8'))
            if (self.inLevel):
                print self.concept
                # (tree_level,open):Level()
                #self.report[(self.tree_level,True)]= Level(self.concept,self.tree_level)
                self.report.append(Container(self.concept,self.tree_level,True,self.return_parent()))
                print self.report
            if (self.inType == False):
                self.concept = None
        if (name == "CONTAINER"):
            print "* End tree level: ", self.tree_level
            self.tree_level -= 1
            self.currentLevel = None
        if (name == "CHILDS"): 
            print "* End of child-level: ", self.child_level
            self.close_level()
            self.child_level -= 1
        if (name == "DATE"):
            self.current_attribute.concept = self.concept
            print "    -> Date: ", self.current_attribute.concept
            self.inType = False
            self.concept = None
            self.add_attribute()
        if (name == "TEXT"):
            self.current_attribute.concept = self.concept
            print "    -> Text: ", self.current_attribute.concept
            self.add_attribute()
            self.inType = False
            self.concept = None
        if (name == "NUM"):
            self.current_attribute.concept = self.concept
            print "    -> Num: ", self.current_attribute.concept
            self.add_attribute()
            self.inType = False
            self.concept = None
       
       
    def characters(self,chars):
        if (self.inData):
            self.buffer += chars

    def endDocument(self,strings_xml_filename=STRINGS_XML):
        self.xml_files[strings_xml_filename].write("\n</resources>")
        for xml_file in self.xml_files.values():
            xml_file.close()
            print self.report

parser = make_parser()
parser.setContentHandler(DicomParser())
#parser.parse(codecs.open(sys.argv[1],mode='r'encoding='utf-8'))
dicom_xml = open(sys.argv[1],"r") 
parser.parse(dicom_xml)
dicom_xml.close()
