#  -*- coding: utf-8 -*-
from files_settings import *

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
