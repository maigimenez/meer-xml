#  -*- coding: utf-8 -*-
import re
from config import ( get_substitution_options,get_filepath,get_language_section_options, 
    get_property, get_property_interpolation , get_filepath_odontology )
from config_variables import *

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
    
    #TODO: This is method is obsolete
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
        #self.model.append(SETTINGS_CLASS)
        self.activities={}


    #ef set_odontology(self,id_odontology):
    #   self.layouts = LAYOUTS_DICTIONARY[int(id_odontology)]
    #   self.activities = ACTIVITIES_DICTIONARY[int(id_odontology)]        
    
    def set_odontology(self,id_odontology):
        """ Set the filenames for of layouts and android activities using the report odontology id """
        self.layouts = get_filepath_odontology(id_odontology,LAYOUTS)

    #TODO: Move this to config.py
    def set_languages(self,languages=""):
        section,options = get_language_section_options(languages)

        #Get default strings
        default_section = XML_STRINGS_SECTION
        default_options = get_substitution_options(default_section)
        output_directory = get_filepath('Strings')
        defaults = {}
        for default_option in default_options:
            defaults[default_option]= get_property(default_section,default_option)
        #Populate the dictionary where the key is the DICOM XML tag and the value is the filename.
        for option in options:
            self.strings[option.upper()] = ( output_directory+'/'+
                                             get_property_interpolation(section,option,False,defaults))
            
