 #  -*- coding: utf-8 -*-
from config_variables import *
from config import get_odontology_level
from types import *

class SAXContainer(object):
    """This class stores a container tag from xml"""
    def __init__(self,concept=Concept(),level=-1,open_level=True, parent=Concept()):
        self.concept = Concept(concept.value,concept.schema,concept.meaning)
        #A list of attributes/nodes (date, num, text)
        self.attributes = []
        self.tree_level = level
        self.open = open_level
        self.parent = parent

    """Return if the concept name has some data"""
    def has_concept(self):
        return (self.concept.concept_name != "")
    
    """Add a new attribute to the list of attributes of this concept"""
    #Si lo cambias a un diccionario añadir el atributo será más rápido
    def add_attribute(self,attribute):
        self.attributes.append(attribute)

    """ Pretty print a container"""
    def __repr__(self):
        return u"L{0} {1}_{2}: {3} ({4}) p({5}){6}\n".format(
            self.tree_level, self.concept.schema, self.concept.value,
            self.concept.meaning, len(self.attributes),
            self.parent.meaning if (self.parent!=None) else "", 
            "..." if self.open else "" ).encode('utf-8')


class SAXReport(object):
    """This class manages the report while we are reading it from xml"""
    def __init__(self):
        self.report_type = ""
        self.id_odontology = -1
        # tree_level: Container()
        self._containers = []
        
    def add_attribute(self,child_level,current_attribute):
        """Add an attribute given the child level of the attribute and the attribute to add""" 
        for container in self._containers:
            if ((container.tree_level == child_level) and container.open):
                container.attributes.append(current_attribute)
                return True
        return False

    def add_container(self,new_container):
        """Add a container to the report """ 
        self._containers.append(new_container)

    #TODO:
    # Si n'hi han atributs al final tanqem abans d'hora
    # hi hauria d'utilitzar tree_level
    def close_level(self,child_level):
        """Close the container given a level of the attributes (child_level)"""
        for container in self._containers:
            if ((container.tree_level == child_level) and container.open):
                container.open = False
                return True
        return False


    def return_parent(self,tree_level):
        """Return the container parent of the given tree level
        we are assuming that dicom xml file is well formed
        
        Keyword arguments:
        tree level -- tree level we want to know the father
        
        """
        for container in self._containers:
            if(container.tree_level == tree_level-1 and container.open):
                return container.concept
        return None


    def imprime(self):
        """ Prettqy print of a report """
        print u"\n ******** {0} ********* \n".format(self.report_type)
        for container in self._containers:
            print u"(L{0} {1}_{2}) {3} ({4}):".format(
                container.tree_level,
                container.concept.schema,
                container.concept.value,
                container.concept.meaning.values(),
                len(container.attributes)).encode('utf-8')
            for attr in container.attributes:
                print u"    - {0} ({1})".format(
                    attr.concept.meaning,
                    attr.type).encode('utf-8')
            print 
        
 
"""
Dictionay implementation of the report
"""


class Children(object):
    def __init__(self):
        self.attributes = []
        self.children_containers = []

class DictContainer(object):
    """This class stores a container tag from xml"""
    def __init__(self):
        #Container's concept_name is the key and the values are its children (attributes and other containers)
        self.containers = {}


class DictReport(object):
    def __init__(self, report_type="",id_odontology=-1):
        self.report_type = report_type
        self.id_odontology = id_odontology
        #This dictionary stores the report. Level is the key and the values are DictContainers
        self.tree = {}
        
    def get_deepest_level(self):
        """ Return deepest level of the tree."""
        deepest_level = -1
        for level in self.tree.keys():
            if (level>deepest_level):
                deepest_level = level
        return deepest_level

    """ Pretty print of a report """
    def imprime(self):
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        
        for level,dict_containers in self.tree.iteritems():
            for concept,children in dict_containers.containers.iteritems():
                num_children = len(children.children_containers)
                num_attrs = len(children.attributes)
                print u"(L{0}) {1} (no.attr: {2} - no.child:{3}):".format(
                    level,
                    concept.meaning,
                    num_attrs,
                    num_children).encode('utf-8')
                if(num_attrs > 0):
                    print u"  * Attributes"
                    for attr in children.attributes:
                        if (attr.type == NUM and attr.is_bool()):
                            attr_type = BOOL
                        else:
                            attr_type = attr.type
                        print u"    - {0} ({1})".format(
                            attr.concept.concept_name,
                            attr_type).encode('utf-8')
                if (num_children > 0):
                    print u"  * Childs"
                    for child in children.children_containers:
                        print u"    - {0}".format(child.concept_name).encode('utf-8')
                    
            print

    def get_parent_code(self, level,concept):
        """ Return container code parent of level given """
        if (level==1):
            return ""
        for parent, children  in self.tree[level-1].containers.iteritems():
            for child in children.children_containers:
                if (child.concept_value == concept.concept_value):
                    return parent.concept_value

    def get_level(self,level):
        """ Retun the tree level given a level """
        if (level == 0):
            return None
        return self.tree[level]

    def get_children(self,level,concept):
        """ Retun the tree level given a level """
        if (level == 0):
            return None
        else:
            #print "*", type(self.tree[level].containers)
            #print self.tree[level].containers
            for concept_level,children  in self.tree[level].containers.iteritems():
                if (concept_level.concept_value == concept.concept_value):
                    return children

    def get_leaf_level(self):
        """ Return deepest level of the report tree """
        return max(self.tree.keys())

    def get_tree(self):
        """ Return the dicom report in a dictionary """
        return self.tree

    def get_odontology(self):
        """ Return current report odontology """
        return self.id_odontology
    
    def get_children_dictionary(self):
        """ Return a dictionary with the children of the report

        The key is the concept_value of the parent and the value is a list 
        whith the children concept meaning

        """
        children_dict = {}
        for level,dict_containers in self.tree.iteritems():
            for concept,children in dict_containers.containers.iteritems():
                num_childs = len(self.tree[level].containers[concept].children_containers)
                if (num_childs>0):
                    children_dict[concept.concept_value] = []
                    for child in self.tree[level].containers[concept].children_containers:
                        children_dict[concept.concept_value]\
                            .append(child.concept_name)
        return children_dict

    def get_data_form_report(self, languages, template_type):
        """ Return data from the report in a dictionary

        Keyword:
        language_code -- language for the data returned
        template_type -- indicates the template type and
                         therefore the information to extract from the report.
        self -- Dict Report with the information extracted from the dicom XML.

        """
        substitution_words = {}
        if (template_type in MULTIPLE_PROPERTIES.keys()):
            if (template_type == DICOM_LEVEL):
                levels_tag = MULTIPLE_PROPERTIES[DICOM_LEVEL][0]
                attrs_tag = MULTIPLE_PROPERTIES[DICOM_LEVEL][1]
                # Init dictinary. Keys are language code and values contains
                # values to fill the template
                for language in languages:
                    substitution_words[language] = {
                        levels_tag: [],
                        attrs_tag: []}
                written_codes = []
                attributes = []
                levels = []
                for level, dict_containers in self.tree.iteritems():
                    level_aux = {}
                    for concept, children in (dict_containers.
                                              containers.iteritems()):
                        num_attrs = len((self.tree[level].
                                         containers[concept].attributes))
                        if (concept.concept_value not in written_codes):
                            for language in languages:
                                # Get keys from template
                                level_name = MULTIPLE_PROPERTIES[
                                    DICOM_LEVEL][3]
                                level_num = MULTIPLE_PROPERTIES[
                                    DICOM_LEVEL][2]
                                code = MULTIPLE_PROPERTIES[
                                    DICOM_LEVEL][4]
                                meaning = MULTIPLE_PROPERTIES[
                                    DICOM_LEVEL][5]
                                odontology = get_odontology_level(
                                    odontology_id=self.get_odontology(),
                                    tree_level=level,
                                    languages_tag=language)
                                # Write words for this template keys
                                level_aux[level_num] = level
                                level_aux[level_name] = (unicode(odontology,
                                                                 "utf-8"))
                                level_aux[code] = concept.concept_value
                                level_aux[meaning] = concept.\
                                    concept_name[language]
                                # Store written code, we don't repeat any code
                                written_codes.append(concept.concept_value)
                                # End of current concept. Appennd concept words
                                # substitution dictionary.
                                substitution_words[language][levels_tag]\
                                    .append(level_aux.copy())
                        #Write attributes if there are any.
                        if (num_attrs > 0):
                            attrs_aux = {}
                            for attr in (self.tree[level].
                                         containers[concept].attributes):
                                #Get this attribute code.
                                attr_code = attr.concept.concept_value
                                #Write this attribute if its not written.
                                if (attr_code not in written_codes):
                                    for lang in languages:
                                        attrs_aux[code] = attr_code
                                        attrs_aux[meaning] = attr.concept.\
                                            concept_name[lang]
                                        # Add this code to written codes list
                                        written_codes.append(attr_code)
                                        # End of current attribute.
                                        # Add it to substitution dictionary
                                        substitution_words[lang][attrs_tag]\
                                            .append(attrs_aux.copy())
            elif (template_type == CHILDREN_ARRAYS):
                # Get children in a dictionary.
                # TODO: Check this time complexity.
                children_dict = self.get_children_dictionary()
                # Init dictinary. Keys are language code and values contains
                # values to fill the template
                nodes_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][0]
                parent_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][1]
                children_tag = MULTIPLE_PROPERTIES[CHILDREN_ARRAYS][2]
                for language in languages:
                    substitution_words[language] = {nodes_tag: []}
                for parent, children in children_dict.iteritems():
                    # TODO: If I expect handle X languages but in the report
                    # there are Y languages, this will throw an error.
                    #  Solve this
                    for language in languages:
                        dict_aux = {parent_tag: parent}
                        for child in children:
                            if (children_tag not in dict_aux.keys()):
                                dict_aux[children_tag] = []
                            dict_aux[children_tag]\
                                .append(unicode(child[language]))
                        #End of this node. Append to substitution dictionary
                        substitution_words[language][nodes_tag]\
                            .append(dict_aux.copy())
            return substitution_words
