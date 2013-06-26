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
    #TODO: Add CODE_SCHEMA support
    def __init__(self,value=-1,meaning={}):
        self.value = value
        self.meaning = meaning

    def __str__(self):
        localized_strings = ""
        for localized_string in self.meaning.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}".format(
            localized_strings, self.value).encode('utf-8')

    def __repr__(self):
        localized_strings = ""
        for localized_string in self.meaning.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}".format(
            localized_strings, self.value).encode('utf-8')

    def __getattribute__(self,name):
        if (name=='code' or name=='value'):
            return object.__getattribute__(self,'value')
        else:
            return object.__getattribute__(self,name)


class Data_type(object):
    """This class manages a data type. 
    This is the superclass, the  child classes are: date, text and num

    """
    def __init__(self):
        self.type = ""
        self.concept = Concept()

    def __getattribute__(self,name):
        if (name=='code'):
            return self.concept.code
        elif (name=='meaning'):
            return self.concept.meaning
        else:
            return object.__getattribute__(self,name)

    def __repr__(self):
        return u"{0}: {1}".format(self.type,self.concept.meaning)

    def __str__(self):
        return u"{0}: {1}".format(self.type,self.concept.meaning.values()[0])


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
             self.type,self.concept.meaning,self.unit_measurement.meaning)
