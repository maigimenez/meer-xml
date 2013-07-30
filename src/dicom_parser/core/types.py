class Property(object):
    """This class manages the properties of a concept """
    def __init__(self):
        self.max_cardinality = 0
        self.min_cardinality = 0
        self.condition = ""
        self.xquery = ""
        self.default_value = None

    def set_cardinality(self,max_value=1,min_value=1):
        self.max_cardinality = max_value
        self.min_cardinality = min_value

    def __repr__(self):
        return "max:{0} - min:{1} | condition:{2} ? {3} | default = {4} ".format(self.max_cardinality, self.min_cardinality, self.condition, self.xquery, self.default_value)

class Concept(object):
    """ This class manages the concept"""
    def __init__(self,value=-1,schema="", meaning={}):
        self.value = value
        self.schema = schema
        self.meaning = meaning

    def __str__(self):
        localized_strings = ""
        for localized_string in self.meaning.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}-{2}".format(
            localized_strings, self.schema, self.value).encode('utf-8')

    def __repr__(self):
        localized_strings = ""
        for localized_string in self.meaning.values():
            localized_strings +=  localized_string + ", "
        return u"Concept names: {0} - Concept value: {1}-{2}".format(
            localized_strings, self.schema, self.value).encode('utf-8')

    def __getattribute__(self,name):
        if (name=='code' or name=='value'):
            return object.__getattribute__(self,'value')
        else:
            return object.__getattribute__(self,name)

    def get_schema_code(self,separator='_'):
        return self.schema + separator + self.code


class Data_type(object):
    """This class manages a data type. 
    This is the superclass, the  child classes are: date, text and num

    """
    def __init__(self):
        self.type = ""
        self.concept = Concept()
        self.properties = Property()

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
        return u"{0}: {1} ({2})".format(self.type,self.concept.meaning.values()[0],
            self.properties)

    def get_schema_code(self,separator='_'):
        return self.concept.get_schema_code()

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
        unit_type = self.unit_measurement.meaning.values()
        if ("Unidades Boleanas" in unit_type or "Boolean Units" in unit_type):
            return True
        return False

    def __repr__(self):
         return u"{0}: {1} - type({2})".format(
             self.type,self.concept.meaning,self.unit_measurement.meaning)
