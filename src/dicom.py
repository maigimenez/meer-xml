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
        return u"Concept name: {0} - Concept value: {1}".format(self.concept_name, self.concept_value).encode('utf-8')

    def __repr__(self):
        return u"Concept name: {0} - Concept value: {1}".format(self.concept_name, self.concept_value).encode('utf-8')


class Data_type(object):
    """This class manages a data type. 
    This is the superclass, the  child classes are: date, text and num

    """
    def __init__(self):
        self.type = ""
        self.concept = Concept()
        self.properties = []

    def __repr__(self):
        return u"{0}: {1}".format(self.type,self.concept.concept_name)

class Date(Data_type):
    """Child class of Data_type
    It stores a date

    """
    def __init__(self):
        self.type = "date"


class Text(Data_type):
    """Child class of Data_type
    It stores a text field

    """
    def __init__(self):
        self.type = "text"


class Num(Data_type):
    """Child class of Data_type
    It stores a number

    """
    def __init__(self):
        self.type = "num"


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
    """This class manages the whole report"""
    def __init__(self):
        self.report_type = ""
        # tree_level: Container()
        self.containers = []

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

    """Return the container parent of the given tree level
    we are assuming that dicom xml file is well formed
    
    """
    def return_parent(self,tree_level):
        for container in self.containers:
            if(container.tree_level == tree_level-1 and container.open):
                return container.concept
        return None


    """ Pretty print of a report """
    def imprime(self):
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
