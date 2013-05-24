#  -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser, ConfigParser
from config_variables import *
from os.path import join
import codecs

def read_config(path=SETTINGS_PATH):
    """ Read the config file """
    config = ConfigParser()
    if(config.read(path)==[]):
        exit("The settings file is empty or it's not where it's supposed to be.\n"\
                 "it should be at ./settings (I was looking for this file: {0})".format(path))
    return config

#TODO: Hay 3 funciones para encontrar la ruta en la configuración: get_filepath, get_xml_filepath y get_filepath_odontology haz un merge de las tres. 
def get_filepath(filetype):
    """ Return the output path for the file type (section) given """ 
    config = read_config()
    return config.get(OUTPUT_DIRECTORIES_SECTION,filetype)

def get_properties_path(language):
    """ Return the path for the properties given the language """
    config = read_config()
    return join(config.get(OUTPUT_DIRECTORIES_SECTION,PROPERTIES_OPTION),
                language+
                config.get(EXTENSIONS_SECTION, PROPERTIES_EXTENSION))

def get_xml_filepath(language_code,filetype):
    """ Return the xml file for the strings in the language given by the language_code parameter """
    config = read_config()
    if (filetype == STRINGS):
        #Get the root path for the outputs
        output_directory = config.get(OUTPUT_DIRECTORIES_SECTION,STRINGS_OUTPUT_OPTION)
        #Get the path for the filename for the language_code
        xml_filename = config.get(XML_STRINGS_SECTION,language_code)
    else:
        # TODO: throw an error. 
        pass
    return join(output_directory, xml_filename)

def get_template_filename(template):
    """ Given a template name, returns the path and the filename """
    config = read_config(SETTINGS_PATH)
    root_path = config.get(TEMPLATES_SECTION,TEMPLATES_ROOT_PATH)
    template_name = "" 
    template_path = ""
    # Get the template name and its path
    # String templates
    if (template in STRING_TEMPLATES):
        templat_path =  config.get(TEMPLATES_SECTION,STRING_TEMPLATES_PATH) 
        template_name = config.get(STRING_TEMPLATES_SECTION,template)
    # Layout templates
    elif (template in LAYOUT_TEMPLATES):
        template_path = config.get(TEMPLATES_SECTION,LAYOUT_TEMPLATES_PATH)
        template_name = config.get(LAYOUT_TEMPLATES_SECTION,template)
    else:
        exit("The template path for: {0}, has not been found.)".format(template))
    # Return the path to tempalate file.
    return join(root_path,template_path),template_name

def get_property(section,option):
    """ Returns a configuration property given a section and an option from the settings file. """
    config = read_config(SETTINGS_PATH)
    return config.get(section,option)

def get_property_interpolation(section,option,interpolation,defaults):
    """ Returns a configuration property.
    
    Keywords:
    section -- configuration section
    option  -- option we are looking for in the configuartion section.
    interpolation -- Boolean to indicate if there is interpolation or not.
    defaults -- dictionary with the default information to interpolate.

    """
    config = read_config(SETTINGS_PATH)
    return config.get(section,option,interpolation,defaults)

def get_substitution_options(default_section,path=SETTINGS_PATH):
    """ Return options for a config section used as default section """
    config = read_config(path)
    return config.options(default_section)

def get_language_section_options(languages="",path=SETTINGS_PATH):
    """ Return the section and the options for the languages supported """
    config = read_config(path)
    #Select config section for the language 
    if (languages==DEFAULT_INPUT):
        section = DEFAULT_STRINGS_SECTION
        options = config.options(section)
    elif(languages==I18N_INPUT):
        section = I18N_SECTION
        options = config.options(section)
    else:
        exit("The code you have enter for internationalization is not supported.\n"\
                 "The options are \"default\"(for english) and "\
                 "\"i18n\"(for spanish as first language and english as second language)")
    return (section,options)

def get_language_code(dicom_tag,languages_tag,path=SETTINGS_PATH):
    """ Returns the language code corresponding to the dicom tag """
    config = read_config(path)
    section,options=get_language_section_options(languages_tag,path)
    dicom_tag = dicom_tag.lower()
    if (dicom_tag in options):
        #Get the language code for the dicom tag
        #We don't make the substitution because we want the language code
        return config.get(section,dicom_tag,True)[2:-2]
    else:
        return ""

def get_odontology_level(odontology_id,tree_level,dicom_tag=None,languages_tag=None,language=None):
    """ 
    Return the level name.

    Keyword Arguments:
    odontology_id -- Odontolgy ID of the report. 
    tree level -- tree level number. We want to know this level's name.
    languages_tag  --  tag with supported languages (i18n|default) to resolve
    language -- comments language tag using i18n standard. 
    dicom_tag -- dicom xml tag used to find out corresponding language in settings. 
    
    """
    #TODO: What happends if the odontogy id does not exists?
    if (dicom_tag != None):
        comments_language = get_language_code(dicom_tag,languages_tag)
        #If the language code does not exists, we will write comments in the default language
        if (comments_language == ''):
            comments_language = DEFAULT_LANGUAGE
    else:
        comments_language = languages_tag
    odontology_path = get_properties_path(comments_language)
    config = read_config(odontology_path)
    odontology_section = odontology_id+' '+LEVEL_STRINGS
    #TODO: Handle the exceptions
    return config.get(odontology_section,str(tree_level))

def get_substitution_dictionary(language_code,section,template_type):
    """  Read properties file for the language and returns a dictionary 
    with substitution words for this language
    Multiple is a boolean parameter. If it is true the template is filled multiple times,
    so, we return a dictionary with every possible substitution. 
    
    """
    config = SafeConfigParser()
    path = get_properties_path(language_code)
    #Since it may appear utf-8 characters we read this file coded as utf-8
    with codecs.open(path,'r',encoding='utf-8') as f:
        if(config.readfp(f)==[]):
            exit('The settings file is empty or it\'s not where it\'s supposed to be.\n'\
                     'it should be under {0} (I was looking for this file: {1})'.format(PROPERTIES_PATH,path))
    
    options = config.options(section)
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

def get_filepath_odontology(odontology_id, filetype):
    """ Retun layouts filenames inside a dictionary, the key is the level id and the value is the filename

    Keyword:
    odontology_id -- odontology id of the report. Every odontology has its own layout configuration in 
    the settings file
    filetype -- file type of the filenames we are looking for (layouts or activities).

    """
    config = read_config()
    # Get layouts filepath
    if (filetype == LAYOUTS):
        #Get the ouputs directory
        output_directory = get_filepath(LAYOUTS)
        #Get the filetypes file names. 
        section = odontology_id + LAYOUT_FILENAME
        options = config.options(section)
        layouts = {}
        for option in options:
            level = option.replace(LEVEL_TAG,'')
            layouts[level] = join( output_directory,config.get(section,option))
        return layouts


def get_layout_settings(odontology_id, level):
    """ Return the layout distribution for odontology and level given """
    section = odontology_id + LAYOUT_SETTINGS
    option = LEVEL_TAG + level
    return get_property(section,option)
