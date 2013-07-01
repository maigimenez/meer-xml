#  -*- coding: utf-8 -*-
from types import Concept


class SAXContainer(object):
    """This class stores a container tag from xml"""
    def __init__(self, concept=Concept(), level=-1, open_level=True,
                 parent=Concept()):
        self.concept = Concept(concept.value, concept.schema, concept.meaning)
        #A list of attributes/nodes (date, num, text)
        self.attributes = []
        self.tree_level = level
        self.open = open_level
        self.parent = parent

    def has_concept(self):
        """Return if the concept name has some data"""
        return (self.concept.concept_name != "")

    def add_attribute(self, attribute):
        """Add a new attribute to the list of attributes of this concept"""
        self.attributes.append(attribute)

    def __repr__(self):
        """ Pretty print a container"""
        return u"L{0} {1}_{2}: {3} ({4}) p({5}){6}\n".format(
            self.tree_level, self.concept.schema, self.concept.value,
            self.concept.meaning, len(self.attributes),
            self.parent.meaning if (self.parent is None) else "",
            "..." if self.open else "" ).encode('utf-8')


class SAXReport(object):
    """This class manages the report while we are reading it from xml"""
    def __init__(self):
        self.report_type = ""
        self.id_odontology = -1
        # tree_level: Container()
        self._containers = []

    def add_attribute(self, child_level, current_attribute):
        """Add an attribute

        Keyword arguments:
        child_level -- level where we add the attribute
        current_attribute --- attribute to add

        """
        for container in self._containers:
            if ((container.tree_level == child_level) and container.open):
                container.attributes.append(current_attribute)
                return True
        return False

    def add_container(self, new_container):
        """Add a container to the report """
        self._containers.append(new_container)

    #TODO:
    # Si n'hi han atributs al final tanqem abans d'hora
    # hi hauria d'utilitzar tree_level
    def close_level(self, child_level):
        """Close the container given a level of the attributes (child_level)"""
        for container in self._containers:
            if ((container.tree_level == child_level) and container.open):
                container.open = False
                return True
        return False

    def return_parent(self, tree_level):
        """Return the container parent of the given tree level
        we are assuming that dicom xml file is well formed

        Keyword arguments:
        tree level -- tree level we want to know the father

        """
        for container in self._containers:
            if(container.tree_level == (tree_level - 1) and container.open):
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
