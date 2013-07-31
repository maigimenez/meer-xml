 #  -*- coding: utf-8 -*-
from types import Concept, Property
from config_variables import (MULTIPLE_PROPERTIES, DICOM_LEVEL,
                             CHILDREN_ARRAYS, CODE_ARRAYS)
from config import get_odontology_level
from collections import deque
from tree import Tree

class Container(object):
    def __init__(self, tree_level, concept=Concept(), properties=Property(),
                 attributes=[]):
        self.tree_level = tree_level
        self.concept = concept
        #List of properties for this Container.
        #TODO: Items in this list will be Property type
        self.properties = properties
        self.attributes = attributes[:]

    # TODO: def __getattr__(self,name)
    def get_code(self):
        return self.concept.value

    def get_schema(self):
        return self.concept.schema

    def get_meaning(self):
        return self.concept.meaning

    def get_level(self):
        return self.tree_level

    def get_concept(self):
        return self.concept

    def get_schema_code(self,sep='_'):
        return self.concept.schema + sep + self.concept.value

    def has_code(self,code):
        return self.concept.get_schema_code() == code

    def __str__(self):
        meaning = self.concept.meaning.values()[0]
        str_attributes = ""
        for attribute in self.attributes:
            str_attributes += " - " + attribute.__str__() + "\n"
        str_attributes = str_attributes[:-1]
        return u"[{0}_{1}] {2} (no.attr: {3} - no.prop:{4}): \n{5}".format(
            self.concept.schema, self.concept.value, meaning.upper(),
            len(self.attributes), self.properties, str_attributes)\
            .encode("utf-8")

    def __repr__(self):
        return u"[{0}_{1}] {2} (no.attr: {3} - no.prop:{4}):".format(
            self.concept.schema, self.concept.value, self.concept.meaning,
            len(self.attributes),self.properties)

class DicomTree(object):
    def __init__(self):
        self.root = {}

    def get_root(self):
        return self.root.keys()

    def get_container(self, code):
        for container in self.root.keys():
            if (container.get_code() == code):
                return container
        for child in self.root.values():
            child.get_container(code)

    def get_parents(self):
        if (self.root):
            return [parent for parent in self.root.keys()]
        else:
            return []

    def is_empty(self):
        return self.root == {}

    def print_tree(self, ident, attributes):
        if (self.root):
            for data, children in self.root.iteritems():
                meaning = data.concept.meaning.values()[0]
                str_attributes = "\n"
                for attribute in data.attributes:
                    str_attributes += ("|" + " " * (ident + 2) + " - "
                                       + attribute.__str__() + "\n")
                str_attributes = str_attributes[:-1]
                if (not attributes):
                    print u"{0} [{1}_{2}] {3} (no.attr: {4} ) (prop: {5})"\
                        .format("-" * (ident + 1), data.concept.schema,
                                data.concept.value, meaning.upper(),
                                len(data.attributes), data.properties)
                else:
                    print u"{0} [{1}_{2}] {3} "\
                        "(no.attr: {4} ) (prop:{5}): {6}"\
                        .format("-" * (ident + 1), data.concept.schema,
                                data.concept.value, meaning.upper(),
                                len(data.attributes), data.properties,
                                str_attributes)
                children.print_tree(ident + 4, attributes)

    def add_node(self, node, parent):
        if (parent is None):
            self.root[node] = DicomTree()
        else:
            codes = [container.get_code() for container in self.root.keys()]
            if parent.value in codes:
                key = self.get_container(parent.value)
                self.root[key].root[node] = DicomTree()
            else:
                for child in self.root.values():
                    child.add_node(node, parent)

    def get_set_data(self, nodes, attributes):
        if (self.root == {}):
            return (nodes, attributes)
        else:
            for data, children in self.root.iteritems():
                written_codes = [node.get_code() for node in nodes]
                written_codes.extend([attr.code for attr in attributes])
                if (data.get_code() not in written_codes):
                    nodes.append(data)
                for attribute in data.attributes:
                    if (attribute.code not in written_codes):
                        attributes.append(attribute)
                children.get_set_data(nodes, attributes)

    def get_flat_tree(self, flat):
        if (self.root == {}):
            return flat
        else:
            for parent, children in self.root.iteritems():
                flat[parent] = children.get_parents()
                children.get_flat_tree(flat)
    


class DicomSR(object):
    def __init__(self, report_type="", id_odontology=-1):
        self.report_type = report_type
        self.id_odontology = id_odontology
        self.report = Tree()

    def imprime(self):
        """ Pretty print of a report """
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        self.report.print_tree(0)

    def add_node(self, node, parent):
        self.report.add_node(node, parent)

    def get_odontology(self):
        """ Return current report odontology """
        return self.id_odontology

    def get_flat_data(self):
        flat = {}
        self.report.get_flat_tree(flat)
        return flat

    def get_report_root(self):
        return self.report.get_root()

    def get_data_form_report(self, languages, template_type):
        """ Return data from the report in a dictionary

        Keyword arguments:
        language_code -- language for the data returned
        template_type -- indicates the template type and
                         therefore the information to extract from the report.
        self -- Dict Report with the information extracted from the dicom XML.

        """
        substitution_words = {}
        if (template_type in MULTIPLE_PROPERTIES.keys()):
            if (template_type == DICOM_LEVEL):
                # Get keys for this template
                levels_tag = MULTIPLE_PROPERTIES[DICOM_LEVEL][0]
                attrs_tag = MULTIPLE_PROPERTIES[DICOM_LEVEL][1]
                level_name = MULTIPLE_PROPERTIES[DICOM_LEVEL][3]
                level_num = MULTIPLE_PROPERTIES[DICOM_LEVEL][2]
                code = MULTIPLE_PROPERTIES[DICOM_LEVEL][4]
                meaning = MULTIPLE_PROPERTIES[DICOM_LEVEL][5]
                #Init dictinary will hold the substitution.
                # Keys are language code and values  contains
                # values to fill the template
                for language in languages:
                    substitution_words[language] = {
                        levels_tag: [],
                        attrs_tag: []}
                #Get container's concept and its attributes
                containers = []
                attributes = []
                self.report.get_set_data(containers, attributes)
                for container in containers:
                    odontology = get_odontology_level(
                        odontology_id=self.get_odontology(),
                        tree_level=container.get_level(),
                        languages_tag=language)
                    for language in languages:
                        aux = {}
                        aux[level_num] = container.get_level()
                        aux[level_name] = (unicode(odontology, "utf-8"))
                        aux[code] = container.get_code()
                        aux[meaning] = container.get_meaning()[language]
                        substitution_words[language][levels_tag].\
                            append(aux.copy())
                for attribute in attributes:
                    for language in languages:
                        aux = {}
                        aux[code] = attribute.code
                        aux[meaning] = attribute.meaning[language]
                        substitution_words[language][attrs_tag].\
                            append(aux.copy())

            elif (template_type == CHILDREN_ARRAYS):
                nodes_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][0]
                parent_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][1]
                children_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][2]
                for language in languages:
                    substitution_words[language] = {nodes_tag: []}
                flat = {}
                self.report.get_flat_tree(flat)
                #Delete leaf items. They are not needed
                flat = {key: flat[key] for key in flat if flat[key]}
                for parent, children in flat.iteritems():
                     for language in languages:
                         aux = {parent_tag: parent.get_schema_code(), children_tag: []}
                         for child in children:
                             aux[children_tag].append(
                                 child.get_meaning()[language])
                         substitution_words[language][nodes_tag].append(aux)

            elif (template_type == CODE_ARRAYS):
                #TODO: Change comment on this template to make it different 
                #from CHILDREN_ARRAYS
                nodes_tag = MULTIPLE_PROPERTIES[CODE_ARRAYS][0]
                parent_tag = MULTIPLE_PROPERTIES[CODE_ARRAYS][1]
                children_tag = MULTIPLE_PROPERTIES[CODE_ARRAYS][2]
                for language in languages:
                    substitution_words[language] = {nodes_tag: []}
                codes = self.report.get_code_containers()
                for code in codes:
                    for language in languages:
                        aux = {parent_tag: code.get_schema_code(), children_tag: []}
                        for option in code.options:
                            aux[children_tag].append(
                                option.meaning[language])
                        substitution_words[language][nodes_tag].append(aux)
                    

        return substitution_words
