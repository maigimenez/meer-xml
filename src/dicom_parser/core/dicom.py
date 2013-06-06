 #  -*- coding: utf-8 -*-
from config_variables import * 
from config import get_odontology_level

class Property(object):
    """This class manages the properties of a concept """
    def __init__(self):
        self.max_cardinality = 0
        self.min_cardinality = 0
        self.max_value = 0
        self.min_value = 0
        self.condition = ""


class Concept(object):
    """ This class manages the concept"""
    def __init__(self,concept_name={},concept_value=-1):
        #print "init"
        self.concept_name = concept_name
        self.concept_value = concept_value

    def __str__(self):
        localized_strings = ""
        for localized_string in self.concept_name.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}".format(
            localized_strings, self.concept_value).encode('utf-8')

    def __repr__(self):
        localized_strings = ""
        for localized_string in self.concept_name.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}".format(
            localized_strings, self.concept_value).encode('utf-8')

class Data_type(object):
    """This class manages a data type. 
    This is the superclass, the  child classes are: date, text and num

    """
    def __init__(self):
        self.type = ""
        self.concept = Concept()

    def __repr__(self):
        return u"{0}: {1}".format(self.type,self.concept.concept_name)

class Date(Data_type):
    """Child class of Data_type
    It stores a date

    """
    def __init__(self):
        Data_type.__init__(self)
        self.type = "date"


class Text(Data_type):
    """Child class of Data_type
    It stores a text field

    """
    def __init__(self):
        Data_type.__init__(self)
        self.type = "text"


class Num(Data_type):
    """Child class of Data_type
    It stores a number

    """
    def __init__(self):
        Data_type.__init__(self)
        self.type = "num"
        self.unit_measurement = Concept()

    def is_bool(self):
        """ Return if a num data is boolean or not"""
        unit_type = self.unit_measurement.concept_name.values()
        if ("Unidades Boleanas" in unit_type or "Boolean Units" in unit_type):
            return True
        return False

    def __repr__(self):
        return u"{0}: {1} - type({2})".format(
            self.type,self.concept.concept_name,self.unit_measurement.concept_name)


class Container(object):
    """This class stores a container tag from xml"""
    def __init__(self,concept=Concept(),level=-1,open_level=True, parent=Concept()):
        self.concept = Concept(concept.concept_name,concept.concept_value)
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
        return u"L{0}: {1} ({2}) p({3}){4}\n".format(
            self.tree_level,self.concept.concept_name, len(self.attributes),
            self.parent.concept_name if (self.parent!=None) else "", 
            "..." if self.open else "" ).encode('utf-8')


class Report(object):
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
            print u"(L{0}) {1} ({2}):".format(
                container.tree_level,
                container.concept.concept_name.values(),
                len(container.attributes)).encode('utf-8')
            for attr in container.attributes:
                print u"    - {0} ({1})".format(
                    attr.concept.concept_name,
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
                num_children = len(self.tree[level].containers[concept].children_containers)
                num_attrs = len(self.tree[level].containers[concept].attributes)
                print u"(L{0}) {1} (no.attr: {2} - no.child:{3}):".format(
                    level,
                    concept.concept_name,
                    num_attrs,
                    num_children).encode('utf-8')
                if(num_attrs > 0):
                    print u"  * Attributes"
                    for attr in self.tree[level].containers[concept].attributes:
                        if (attr.type == NUM and attr.is_bool()):
                            attr_type = BOOL
                        else:
                            attr_type = attr.type
                        print u"    - {0} ({1})".format(
                            attr.concept.concept_name,
                            attr_type).encode('utf-8')
                if (num_children > 0):
                    print u"  * Childs"
                    for child in self.tree[level].containers[concept].children_containers:
                        print u"    - {0}".format(child.concept_name).encode('utf-8')
                    
            print

    def get_level(self,level):
        """ Retun the tree level given a level """
        return self.tree[level]

    def get_tree(self):
        """ Return the dicom report in a dictionary """
        return self.tree

    def get_odontology(self):
        """ Return current report odontology """
        return self.id_odontology
    
    def get_children(self):
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
                        children_dict[concept.concept_value].append(child.concept_name)
        return  children_dict
    
    # def get_data_form_report(self,languages,template_type):
    #     """ Return data from the report in a dictionary

    #     Keyword:
    #     language_code -- language for the data returned
    #     template_type -- indicates the template type and therefore the information to extract from the report.
    #     self -- Dict Report with the information extracted from the dicom XML.
    
    #     """
    #     substitution_words = []
    #     children_dict = self.get_children()
    #     if (template_type in MULTIPLE_PROPERTIES.keys()):
    #         #Dictionary for a dicom level substitution
    #         if (template_type == DICOM_LEVEL):
    #             written_codes = {}
    #             # TODO: Think a better way to reduce this complexity. 
    #             for language in languages:
    #                 written_codes[language] = []
    #                 for level,dict_containers in self.tree.iteritems():
    #                     for concept,children in dict_containers.containers.iteritems():
    #                         dict_aux = {}
    #                         dict_aux[language] = {}
    #                         parent_written = False
    #                         # Write concepts.
    #                         # A concept can be repeated but not its attributes. 
    #                         if (concept.concept_value not in written_codes[language]):
    #                             parent_written = True
    #                             #print "????????", concept.concept_value
    #                             level_names = {}
                           
    #                             #Init the ditionary to store all languages.
    #                             #  dict_aux[language] = {}
    #                             level_names[language] = unicode(get_odontology_level(
    #                                     odontology_id=self.get_odontology(),
    #                                     tree_level=level,
    #                                     languages_tag=language),"utf-8")
    #                         #print level, concept.concept_value, level_names
    #                         # Level information
    #                             dict_aux[language] = {MULTIPLE_PROPERTIES[template_type][0]:level}
    #                         #print unicode(level_names[language])
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][1]] = level_names[language]
    #                         # Parent node information
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][2]] = concept.concept_value
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][3]] = concept.concept_name[language]
    #                             written_codes[language].append(concept.concept_value)
    #                             # print written_codes
    #                             # print
    #                             # print dict_aux
    #                             # print 
    #                             # print "*************"
    #                             #substitution_words.append(dict_aux)

    #                         # Write Attributes
    #                         num_attrs = len(self.tree[level].
    #                                     containers[concept].attributes)
    #                         attributes_written = False
    #                         # Write attributes if there are any.
    #                         if(num_attrs > 0):
    #                             #for language in languages:
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][4]]=[]
    #                             #rint "init ", language," - Dictionary", dict_aux 
    #                             for attr in (self.tree[level].
    #                                          containers[concept].attributes):
    #                                 attrs_aux = {}
    #                                 if (attr.concept.concept_value not in written_codes[language]):
    #                                     atributes_written = True
    #                                     attrs_aux[MULTIPLE_PROPERTIES[template_type][5]] = attr.concept.concept_value
    #                                     attrs_aux[MULTIPLE_PROPERTIES[template_type][6]] = attr.concept.concept_name[language]
    #                                     written_codes[language].append(attr.concept.concept_value)
    #                                     dict_aux[language][MULTIPLE_PROPERTIES[template_type][4]].append(attrs_aux)
    #                             if (atributes_written and not parent_written):
    #                                 dict_aux[language][MULTIPLE_PROPERTIES[template_type][3]] = concept.concept_name[language]
    #                             # print
    #                             # print dict_aux
    #                             # print "******************"
    #                             # print
    #                             # print
    #                         substitution_words.append(dict_aux)
                    
    #         else:
    #             #print children_dict
    #             for parent, children in children_dict.iteritems():
    #                 dict_aux = {}
    #                 for language in languages:
    #                     dict_aux[language] = {MULTIPLE_PROPERTIES[template_type][0]:parent}
    #                 for child in children:
    #                     # TODO: If I expect handle X languages but in the report there are Y languages, this will throw an error. Solve this. 
    #                     for language in languages:
    #                         if (MULTIPLE_PROPERTIES[template_type][1] not in dict_aux[language].keys()):
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][1]] = [unicode(child[language])]
    #                         else:
    #                             dict_aux[language][MULTIPLE_PROPERTIES[template_type][1]].append(unicode(child[language]))
    #                 #print dict_aux
    #                 substitution_words.append(dict_aux)
    #     #print "********", substitution_words
    #     #print
    #     #print
    #     return substitution_words


    def get_data_form_report(self,languages,template_type):
        substitution_words = {}
        if (template_type in MULTIPLE_PROPERTIES.keys()):
            if (template_type == DICOM_LEVEL):
                for language in languages:
                    substitution_words[language] = {'levels':[],'attributes':[]}
                written_codes = []
                attributes = []
                levels = []
                for level,dict_containers in self.tree.iteritems():
                    level_aux = {}
                    for concept,children in dict_containers.containers.iteritems():
                        num_attrs = len(self.tree[level].containers[concept].attributes)
                        #print u"(*** L{0}) {1}:".format(level,concept.concept_name).encode('utf-8')
                        if (concept.concept_value not in written_codes):
                            for language in languages:
                                level_aux['code'] = concept.concept_value
                                level_aux['meaning'] = concept.concept_name[language]
                                level_aux['level_name'] = unicode(get_odontology_level(
                                        odontology_id=self.get_odontology(),
                                        tree_level=level,
                                        languages_tag=language),"utf-8")
                                level_aux['level_num'] = level
                                written_codes.append(concept.concept_value)
                                substitution_words[language]['levels'].append(level_aux.copy())
                        if (num_attrs>0):
                            attrs_aux = {}
                            for attr in (self.tree[level].containers[concept].attributes):
                                if (attr.concept.concept_value not in written_codes):
                                    for language in languages:
                                        attrs_aux['code'] = attr.concept.concept_value
                                        attrs_aux['meaning'] = attr.concept.concept_name[language]
                                        written_codes.append(attr.concept.concept_value)
                                        substitution_words[language]['attributes'].append(attrs_aux.copy())
                #print substitution_words
                #print 
            elif (template_type == CHILDREN_ARRAYS):
                children_dict = self.get_children()
                for language in languages:
                    substitution_words[language] = {'nodes':[]}
                for parent, children in children_dict.iteritems():
                    # TODO: If I expect handle X languages but in the report there are Y languages, this will throw an error. Solve this
                    for language in languages:
                        dict_aux = {MULTIPLE_PROPERTIES[template_type][0]:parent}
                        for child in children:
                            if ( MULTIPLE_PROPERTIES[template_type][1] not in dict_aux.keys()):
                                dict_aux[MULTIPLE_PROPERTIES[template_type][1]] = [unicode(child[language])]
                            else:
                                dict_aux[MULTIPLE_PROPERTIES[template_type][1]].append(unicode(child[language]))
                            #print dict_aux
                            #print
                        substitution_words[language]['nodes'].append(dict_aux.copy())
                            #substitution_words[language]['parent_code'].append(unicode(child[language]))
                            #print "*", dict_aux
                    #print dict_aux
                    #substitution_words[language].append(dict_aux )
                #print substitution_words
            #print substitution_words
            return substitution_words
