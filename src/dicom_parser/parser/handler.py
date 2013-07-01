#  -*- coding: utf-8 -*-
import sys
import logging
import xml.sax
from core.types import Date, Num, Text, Concept
from core.dicom import (SAXReport, SAXContainer,
                        DictReport, DictContainer, Children)

from core.dicomSR import DicomSR, Container

from core.config import get_language_code


class DicomParser(xml.sax.handler.ContentHandler):
    #TODO: Improve the logging system
    logging.basicConfig(filename='info.log', level=logging.INFO)

    def __init__(self):
        """ Init all the internal variables """
        # Internal variables
        self._deepest_level = 0
        self._tree_level = 0
        self._child_level = 0
        self._buffer = ''
        #Boolean variables to know where we are
        self._in_data = False
        self._in_type = False
        self._in_concep = False
        self._in_level = False
        self._repeated = False
        self._in_unit_measurement = False
        #Store information read from xml
        self._current_attribute = None
        self._concept = None
        self._unit_measurement = None
        # A list of the code values already writen in strings.xml
        self._code_values = []
        # Report-related variables
        self._report = SAXReport()
        self._dict_report = None

    def parse(self, xml_file):
        """ Parse the file using this handler.
        Returns the report using a DictReporT.

        Keyword Argument:
        xml_file  -- XML file in DICOM format to parse

        """
        xml.sax.parse(xml_file, self)
        return self._dict_report

    def startElement(self, name, attrs):
        """ Handles start of a tag """
        #XML root: stores the odontology
        if (name == "DICOM_SR"):
            try:
                self._report.report_type = attrs['Description']
                self._report.id_odontology = attrs['IDOntology']
            except KeyError:
                #report_type it's an old specification
                self._report.report_type = attrs['reportType']
        #Begin of a container tag
        if (name == "CONTAINER"):
            # We are in a new (deeper) tree level
            self._tree_level += 1
            if (self._tree_level > self._deepest_level):
                self._deepest_level = self._tree_level
            self._in_level = True
            logging.info('* Tree level {0}'.format(self._tree_level))
        #Begin of child tag
        if (name == "CHILDS"):
            # We are in a new (deeper) child level
            self._child_level += 1
            self._in_level = False
            logging.info('* Child level {0}'.format(self._child_level))
        if (name == "CONCEPT_NAME"):
            self._in_concept = True
            self._repeated = False
            #Unit measurement tag also has a concept name
            #It explains the unit measurement type (boolean units basically)
            if (self._in_unit_measurement):
                self._unit_measurement = Concept(-1,"",{})
            else:
                self._concept = Concept(-1,"",{})
        if (name == "DATE"):
            self._in_type = True
            self._current_attribute = Date()
        if (name == "TEXT"):
            self._in_type = True
            self._current_attribute = Text()
        if (name == "NUM"):
            self._in_type = True
            self._current_attribute = Num()
        if (name == "UNIT_MEASUREMENT"):
            self._in_unit_measurement = True
        if (name == "CODE_VALUE" or "CODE_MEANING" or "CODE_MEANING2" or name=="CODE_SCHEMA"):
            self._in_data = True
            self._buffer = ''

    def endElement(self, name):
        """ Store data read in the report internal variable """
        if (name == "CODE_VALUE"):
            self._in_data = False
            if(not self._in_unit_measurement):
                self._concept.value = self._buffer
            else:
                self._unit_measurement.value = self._buffer

        if( name == "CODE_MEANING" or name == "CODE_MEANING2"):
            self._in_data = False
            # If it's a unit measurement this is the end of a concept
            # If there are 2 languages (CODE_MEANING and CODE_MEANING2) in
            # the report tree It's stored concept name of the main langage
            # (CODE_MEANING)
            # TODO: pass language code  with a variable (not sys.argv)
            if (not self._in_unit_measurement):
                self._concept.meaning[
                    get_language_code(name, sys.argv[2])] = self._buffer
            #The attribute is a Num type and we store its unit measurement
            elif(self._in_unit_measurement):
                self._unit_measurement.meaning[
                    get_language_code(name, sys.argv[2])] = self._buffer
        
        if (name == "CODE_SCHEMA"):
            self._in_data = False
            if(not self._in_unit_measurement):
                self._concept.schema = self._buffer
            else:
                self._unit_measurement.schema = self._buffer

        if (name == "CONCEPT_NAME"):
            self._in_concept = False
            #This is the end of a concept name tag, if in_level is true
            #this concept will be the level ID
            if (self._in_level):
                logging.info(self._concept)
                self._report.add_container(
                    SAXContainer(self._concept, self._tree_level, True,
                              self._report.return_parent(self._tree_level)))
                #TODO: no va al log, s'imprimix per consola igual
                 #logging.info(self._report.imprime())
            if (self._in_type is False):
                self._concept = None
        if (name == "CONTAINER"):
            logging.info("* End tree level: {0}".format(self._tree_level))
            self._tree_level -= 1
            self.currentLevel = None

        if (name == "CHILDS"):
            logging.info("* End of child-level: {0}".format(self._child_level))
            self._report.close_level(self._child_level)
            self._child_level -= 1

        if (name == "DATE"):
            self._current_attribute.concept = self._concept
            logging.info(
                "    -> Date: {0}".format(self._current_attribute.concept))
            self._in_type = False
            self._concept = None
            self._report.add_attribute(
                self._child_level, self._current_attribute)

        if (name == "TEXT"):
            self._current_attribute.concept = self._concept
            logging.info(
                "    -> Text: {0}".format(self._current_attribute.concept))
            self._report.add_attribute(
                self._child_level, self._current_attribute)
            self._in_type = False
            self._concept = None

        if (name == "NUM"):
            self._current_attribute.concept = self._concept
            self._current_attribute.unit_measurement = self._unit_measurement
            logging.info(
                "    -> Num: {0} * {1}".format(
                    self._current_attribute.concept,
                    self._current_attribute.unit_measurement))
            self._report.add_attribute(
                self._child_level, self._current_attribute)
            self._in_type = False
            self._concept = None

        if (name == "UNIT_MEASUREMENT"):
            self._in_unit_measurement = False

    def characters(self, chars):
        """ Store the characters read in a buffer """
        if (self._in_data):
            self._buffer += chars

    def build_tree(self):
        """ Build a dictionary tree using the information read in the file.
        Return this dictionary report """
        self._dict_report = DictReport(self._report.report_type,
                                       self._report.id_odontology)
        logging.info(
            u"Dictionary report  type: {0} ({1})".format(
                self._dict_report.report_type,
                self._dict_report.id_odontology).encode('utf-8'))
        for container in self._report._containers:
            #If the level doesn't exist I created it
            if (container.tree_level not in self._dict_report.tree):
                self._dict_report.tree[container.tree_level] = DictContainer()
            #We assume that concept is unique in the xml file
            self._dict_report.tree[container.tree_level].containers[
                container.concept] = Children()
            #TODO: check if this structure is the most suitable
            self._dict_report.tree[container.tree_level].containers[
                container.concept].attributes = container.attributes
            #If we are not in the root, this container has a parent
            if(container.tree_level - 1 > 0):
                #If parent level does not exist we create it
                if (container.tree_level - 1 not in self._dict_report.tree):
                    self._dict_report.tree[
                        container.tree_level - 1] = DictContainer()
                    if(container.parent not in self._dict_report.tree[
                            container.tree_level - 1].containers):
                        self._dict_report.tree[container.tree_level - 1].\
                            containers[container.parent] = Children()
                self._dict_report.tree[container.tree_level - 1].\
                    containers[container.parent].children_containers.\
                    append(container.concept)

    def build_dicom_tree(self):
        self._dict_report = DicomSR(self._report.report_type,
                            self._report.id_odontology)
        #Sort containers list by its tree level. 
        self._report._containers.sort(key = lambda x: x.tree_level)
        for container in self._report._containers:
            self._dict_report.add_node(Container(container.tree_level,container.concept,[],container.attributes),container.parent)

    def endDocument(self):
        """ Build the report tree and close the string files """
      #  self.build_tree()
        self.build_dicom_tree()
        #self._report.imprime()
