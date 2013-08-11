 #  -*- coding: utf-8 -*-
from types import Concept, Property

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