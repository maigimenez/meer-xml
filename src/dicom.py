 #  -*- coding: utf-8 -*-
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
    def __init__(self,concept_name="",concept_value=-1):
        self.concept_name = concept_name
        self.concept_value = concept_value

    def __str__(self):
        return u"Concept name: {0} - Concept value: {1}".format(
            self.concept_name, self.concept_value).encode('utf-8')

    def __repr__(self):
        return u"Concept name: {0} - Concept value: {1}".format(
            self.concept_name, self.concept_value).encode('utf-8')


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
        self.containers = []

    """ I store code values read in a local variable so there is no need of this, isnt't it?
    def is_reapeted(self):
        Return if the concept has been already stored in the report
        so it has been already written in the strings.xml
        
    """
        
    def add_attribute(self,child_level,current_attribute):
        for container in self.containers:
            if ((container.tree_level == child_level) and container.open):
                container.attributes.append(current_attribute)
                return True
        return False

    def add_container(self,new_container):
        return self.containers.append(new_container)

    #TODO:
    # Si n'hi han atributs al final tanqem abans d'hora
    # hi hauria d'utilitzar tree_level
    def close_level(self,child_level):
        for container in self.containers:
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
        for container in self.containers:
            if(container.tree_level == tree_level-1 and container.open):
                return container.concept
        return None


    def imprime(self):
        """ Pretty print of a report """
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        for container in self.containers:
            print u"(L{0}) {1} ({2}):".format(
                container.tree_level,
                container.concept.concept_name,
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

    """ Pretty print of a report """
    def imprime(self):
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        
        for level,dict_containers in self.tree.iteritems():
            for concept,children in dict_containers.containers.iteritems():
                num_childs = len(self.tree[level].containers[concept].children_containers)
                num_attrs = len(self.tree[level].containers[concept].attributes)
                print u"(L{0}) {1} (no.att: {2} - no.child:{3}):".format(
                    level,
                    concept.concept_name,
                    num_attrs,
                    num_childs).encode('utf-8')
            if(num_attrs > 0):
                print u"  * Attributes"
                for attr in self.tree[level].containers[concept].attributes:
                    print u"    - {0} ({1})".format(
                        attr.concept.concept_name,
                        attr.type).encode('utf-8')
            if (num_childs > 0):
                print u"  * Childs"
                for child in self.tree[level].containers[concept].children_containers:
                    print u"    - {0}".format(child.concept_name).encode('utf-8')
                    
            print

    def get_level(self,level):
        return self.tree[level]


    def get_tree(self):
        return self.tree
