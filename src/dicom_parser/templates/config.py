#  -*- coding: utf-8 -*-
from config_variables import *
from ConfigParser import SafeConfigParser, ConfigParser
from os.path import join, exists
import codecs


def read_config(path=SETTINGS_PATH):
    config = ConfigParser()
    if(config.read(path)==[]):
        exit("The settings file is empty or it's not where it's supposed to be.\n"\
                 "it should be at ./settings (I was looking for this file: {0})".format(path))
    return config

def get_template_filename(template):
    """ Given a template name, returns the path and the filename """
    config = read_config(SETTINGS_PATH)
    #String templates
    if (template in STRING_TEMPLATES):
        options = config.options(STRING_TEMPLATES_SECTION)  
        for option in options:
            if (option==template):
                #Get root path for the templates
                root_path = config.get(TEMPLATES_SECTION,TEMPLATES_ROOT_PATH)
                #Get the strings path templates
                strings_path =  config.get(STRING_TEMPLATES_SECTION,STRING_TEMPLATES_PATH)
                return join(root_path,strings_path),config.get(STRING_TEMPLATES_SECTION,option)


#TODO This methos is very simmilar to set_languages from /parser/templates.py try to refactor
def get_strings_filepath(language_code):
    """ Return the xml file for the strings in the language given by the language_code parameter """
    config = read_config()
    #Get the root path for the outputs
    output_directory = config.get(OUTPUT_DIRECTORIES_SECTION,STRINGS_OUTPUT_SECTION)
    #Get the path for the filename for the language_code
    string_filename = config.get(XML_STRINGS_SECTION,language_code)
    return join(output_directory, string_filename)


#TODO: Refactor with config.py in parser module
def get_substitution_dictionary(language_code,section,template_type):
    """ 
    Read properties file for the language and returns a dictionary 
    with substitution words for this language
    Multiple is a boolean parameter. If it is true the template is filled multiple times,
    so, we return a dictionary with every possible substitution. 
    """
    config = SafeConfigParser()
    path = join(PROPERTIES_PATH,language_code+PROPERTIES_EXTENSION)
    #Since it may appear utf-8 characters we read this file coded as utf-8
    with codecs.open(path,'r',encoding='utf-8') as f:
        if(config.readfp(f)==[]):
            exit('The settings file is empty or it\'s not where it\'s supposed to be.\n'\
                     'it should be under {0} (I was looking for this file: {1})'.format(PROPERTIES_PATH,path))
    
    options = config.options(section)
    #print options
    substitution_words = {}
    #If the section has multiple values
    if (template_type  not in MULTIPLE_PROPERTIES.keys()):
        for option in options:
            #Store words in unicode since jinja2 uses it
            substitution_words[option] = unicode(config.get(section,option))
    else:
        for option in options:
            if (template_type not in substitution_words.keys()):
                #The template_type is used as variable for the list in the template
                substitution_words[template_type] = [{MULTIPLE_PROPERTIES[template_type][0]:unicode(option),
                                              MULTIPLE_PROPERTIES[template_type][1]:
                                                   unicode(config.get(section,option))}]
            else:
                substitution_words[template_type].append({MULTIPLE_PROPERTIES[template_type][0]:unicode(option),
                                              MULTIPLE_PROPERTIES[template_type][1]:
                                                       unicode(config.get(section,option))})

    return substitution_words                                  

def get_data_form_report(language_code,template_type,report):
    """ Return data from the report in a dictionary

    Keyword:
    language_code -- language for the data returned
    template_type -- indicates the template type and therefore the information to extract from the report.
    report -- Dict Report with the information extracted from the dicom XML.
    
    """
    substitution_words = [] 
    children_dict = report.get_children()
    if (template_type in MULTIPLE_PROPERTIES.keys()):
        for parent, children in children_dict.iteritems():
            dict_aux = {MULTIPLE_PROPERTIES[template_type][0]:parent}
            for child in children:
                if (MULTIPLE_PROPERTIES[template_type][1] not in dict_aux.keys()):
                    dict_aux[MULTIPLE_PROPERTIES[template_type][1]] = [unicode(child[language_code])]
                else:
                    dict_aux[MULTIPLE_PROPERTIES[template_type][1]].append(unicode(child[language_code]))
                    #substitution_words[template_type].append(unicode(child[language_code]))
            substitution_words.append(dict_aux)
            
    return substitution_words
