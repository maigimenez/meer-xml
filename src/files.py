#  -*- coding: utf-8 -*-
from files_settings import *
import re

#{filename:<file>}
class XMLFiles(object):
    def __init__(self):
        self.layouts = {}
        self.strings = {}
        self.model = {}
        self.activities = {}
        # This variable handles the internazionalization as it is
        # CODE_MEANING - CODE_MEANING2
        self.language_match = {}
    
    def write_java_settings(self,filename):
        """ Write the basic structure for settings.java """
        self.model[filename] = open(filename,'w')
        self.model[filename].write('SETTINGS_JAVA')

    def get_container_meaning(self,code,filename):
        """ Returns concept meaning given a filename and a concept_code"""
        strings_file = open(filename)
        for line in strings_file:
            if (code in line):
                m = re.search('>.+<', line)
                strings_file.close()
                return m.group(0)[1:-1]

    def get_children_string(self,report_tree,filename):
        """ Returns a dictionary with parent code as key and concept meaning as children """
        level_array = {}
        for dict_containers in report_tree.values():
            for concept,children in dict_containers.containers.iteritems():
                if (len(children.children_containers)>0):
                    level_array[concept.concept_value]=[]
                    for child in children.children_containers:
                        child_meaning = self.get_container_meaning(
                            "code_{0}".format(child.concept_value),filename)
                        level_array[concept.concept_value].append(child_meaning)
                        
        return level_array
        
    def close_java_class(self,filename):
        """ The filename points to a java class file
        Write the closing bracket for the java class
        
        """
        self.model[filename].write('END_JAVA')
    
    def close_files(self):
        for xml_file in self.layouts.values():
            xml_file.close()
        for xml_file in self.strings.values():
            xml_file.close()        
        for xml_file in self.model.values():
            xml_file.close()   
        for xml_file in self.activities.values():
            xml_file.close()
        #map doesn't recognize close as a function `_´
        #map(close, self.layouts)

#{code|level:filename}
class AndroidFiles(object):
    def __init__(self):
        self.layouts = {}
        self.strings = {}
        #There is no point for the variable model to be a dictionary here. We don't need the key
        self.model = []
        #Set the model classes. At this point we know that at least we will need a settings class.
        self.model.append(SETTINGS_CLASS)
        self.activities={}

    def set_odontology(self,id_odontology):
        self.layouts = LAYOUTS_DICTIONARY[int(id_odontology)]
        self.activities = ACTIVITIES_DICTIONARY[int(id_odontology)]        
    
    def set_languages(self,languages=""):
        self.strings = STRINGS_DICTIONARY[languages]
        self.language_match = LANGUAGE_DICTIONARY[languages]
