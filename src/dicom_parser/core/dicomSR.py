 #  -*- coding: utf-8 -*-
from config_variables import (MULTIPLE_PROPERTIES, DICOM_LEVEL,
                              CHILDREN_ARRAYS, CODE_ARRAYS)
from config import get_ontology_level
from tree import Tree


class DicomSR(object):
    def __init__(self, report_type="", id_ontology=-1):
        self.report_type = report_type
        self.id_ontology = id_ontology
        self.report = Tree()

    def imprime(self):
        """ Pretty print of a report """
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        self.report.print_tree(0)

    def add_node(self, node, parent):
        self.report.add_node(node, parent)

    def get_ontology(self):
        """ Return current report ontology """
        return self.id_ontology

    def get_flat_data(self):
        flat = {}
        self.report.get_flat_tree(flat)
        return flat

    def get_root(self):
        return self.report.value

    def get_data_from_report(self, template_type, languages=None,
                             position=None, cardinality=None):
        """ Return data from the report in a dictionary

        Keyword arguments:
        languages -- list of languages supported in the  report.
        template_type -- indicates the template type and
                         therefore the information to extract from the report.
        self -- Dict Report with the information extracted from the dicom XML.
        position -- dictionary where it's stored parent and
                    its children position

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
                    ontology = get_ontology_level(
                        ontology_id=self.get_ontology(),
                        tree_level=container.get_level(),
                        languages_tag=language)
                    for language in languages:
                        aux = {}
                        aux[level_num] = container.get_level()
                        aux[level_name] = (unicode(ontology, "utf-8"))
                        aux[code] = container.get_code().lower()
                        aux[meaning] = container.get_meaning()[language]
                        substitution_words[language][levels_tag].\
                            append(aux.copy())
                for attribute in attributes:
                    for language in languages:
                        aux = {}
                        aux[code] = attribute.code.lower()
                        aux[meaning] = attribute.meaning[language]
                        substitution_words[language][attrs_tag].\
                            append(aux.copy())

            elif (template_type == CHILDREN_ARRAYS):
                nodes_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][0]
                parent_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][1]
                children_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][2]
                # Get a flat version of the report
                # TODO: check if the flat version of the tree is
                # always the same
                flat = {}
                self.report.get_flat_tree(flat)
                #Delete leaf items. They are not needed
                flat = {key: flat[key] for key in flat if flat[key]}
                if languages:
                    for language in languages:
                        substitution_words[language] = {nodes_tag: []}

                    for parent, children in flat.iteritems():
                        for language in languages:
                            aux = {parent_tag: parent.get_code().lower(),
                                   children_tag: []}
                            position = 0
                            for child in children:
                                aux[children_tag].append(
                                    child.get_meaning()[language])
                                #print parent.get_schema_code()
                                #print child.get_schema_code(), position
                                position += 1
                            substitution_words[language][nodes_tag].append(aux)
                else:
                    for parent, children in flat.iteritems():
                        p_code = (parent.get_schema().lower() + '_' 
                                  + parent.get_code().lower())
                        position[p_code] = {}
                        cardinality[p_code] = {}
                        pos = 0
                        for child in children:
                            position[p_code][pos] = child.get_schema_code()
                            cardinality[p_code][pos] = child.get_max_cardinality()
                            pos += 1

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
                        aux = {parent_tag: code.code.lower(), children_tag: []}
                        for option in code.options:
                            aux[children_tag].append(
                                option.meaning[language])
                        substitution_words[language][nodes_tag].append(aux)

        return substitution_words
