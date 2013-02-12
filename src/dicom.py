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
        self.properties = []

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
        self.id_odontology = -1
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
class DictContainer(object):
    """This class stores a container tag from xml"""
    def __init__(self,concept=Concept(),level=-1,open_level=True, parent=Concept()):
        #Container's concept_name is the key and the values are its children (attributes and other containers)
        self.containers = {}


class Children(object):
    def __init__(self):
        self.attributes = []
        self.children_containers = []


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

""" Old dictionary report type"""
class Dict_Report(object):
    def __init__(self, report_type=""):
        self.report_type = report_type
        #{(level,concept):[attributes][container_childs]}
        self.tree = {}

    def find_parent(self,level):
        for k in self.tree.keys():
            if (k[0]==level): 
                return k[1]
        return None

    def return_containers(level):
        containers = [key for key in self.tree if level in key]
        print containers
        pass

    """ Pretty print of a report """
    def imprime(self):
        print u"\n ------ {0} ---------- \n".format(self.report_type)
        
        for level,concept in self.tree:
            num_childs = len(self.tree[(level,concept)].containers)
            num_attrs = len(self.tree[(level,concept)].attributes)
            print u"(L{0}) {1} (no.att: {2} - no.child:{3}):".format(
                level,
                concept,
                num_attrs,
                num_childs).encode('utf-8')
            if(num_attrs > 0):
                print u"  * Attributes"
                for attr in self.tree[(level,concept)].attributes:
                    print u"    - {0} ({1})".format(
                        attr.concept.concept_name,
                        attr.type).encode('utf-8')
            if (num_childs > 0):
                print u"  * Childs"
                for child in self.tree[(level,concept)].containers:
                    print u"    - {0}".format(child.concept_name).encode('utf-8')
                    
            print
