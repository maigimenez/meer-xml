#  -*- coding: utf-8 -*-
#from ConfigParser import SafeConfigParser, ConfigParser, NoOptionError
import ConfigParser
from config_variables import *
from os.path import join, exists
from os import makedirs
import codecs
from jinja2 import Environment, PackageLoader
from string import Template

def get_class_name(schema, code, parent_schema, parent_code):
    """ Builds class name of a container """
    # If this is root container its class has no parents.  
    if ((parent_schema == None) or (parent_code == None)):
        return (schema.lower().capitalize() + '_' + 
                code.lower())
    return (parent_schema.lower().capitalize() + '_' + 
            parent_code.lower() + '_' +
            schema.lower() + '_' +
            code.lower())

def get_model_file(java_filename, class_name):
    """ Return filename of current container."""
    return Template(java_filename).safe_substitute(CLASS_NAME=class_name)


# TODO: There are 3 ways to instantiate a filename: get_template_filename, instantiate_filename and get_template_model_file. Merge!
def instantiate_filename(report_level, xml_filename, 
                         concept=None, parent=None):
    """ Reuturn filename of current layout
    based on the concept and its parent. """
    # Add the concept_value to the layout file and open the file for writting
    if (int(report_level) == 1):
        filename = Template(xml_filename).safe_substitute(
            CODE=concept.lower())    
    else:
        filename = Template(xml_filename).safe_substitute(
            CODE=concept.lower(),
            PARENT=parent.lower())
    return filename

def set_environment(template_type):
    """ Set the jinja2 environment given a template type
    (string,layouts,activities or java classe).

    """
    #Get the template_type path
    template_root = get_property(TEMPLATES_SECTION, TEMPLATES_ROOT_PATH)
    template_folder = get_property(TEMPLATES_SECTION, template_type)
    path = join(template_root, template_folder)
    #Check if the template directory exists
    if not exists(path):
        raise TemplateNotFound('Path \'{0}\' does not exists '.format(path))
    elif (template_folder == ''):
        raise TemplateNotFound(
            'Not valid template type \'{0}\''.format(template_type))
    #Set the environment
    env = Environment(loader=PackageLoader(TEMPLATE_PACKAGE, template_folder))
    return env


def get_languages(language_code):
    """ Return the languages supported  based on the language_code """
    if (language_code == I18N_INPUT):
        return I18N
    elif (language_code == DEFAULT_INPUT):
        return DEFAULT
    return None

def read_config(path=SETTINGS_PATH):
    """ Read the config file """
    config = ConfigParser.ConfigParser()
    if(config.read(path)==[]):
        exit("The settings file is empty or it's not where it's supposed to be.\n"\
                 "it should be at ./settings (I was looking for this file: {0})".format(path))
    return config


#TODO: Hay 3 funciones para encontrar la ruta en la configuración: get_properties_path, get_filepath y get_filepath_ontology haz un merge de las tres. 
def get_filepath(filetype,language_code=None):
    """ Return the output path for the file type (section) given """ 
    config = read_config()
    try:
        # If the user has its own output paths setting get them. 
        # Otherwise use default settings.
        user_settings = config.get(USER_SETTINGS_PATH,OUTPUT_DIRECTORIES_SECTION)

         #Get the path for the filename for the language_code
        if(exists(user_settings)):
            user_config = read_config(user_settings)
            if (filetype == STRINGS and language_code):
                output_directory = user_config.get(OUTPUT_DIRECTORIES_SECTION,STRINGS_OUTPUT_OPTION)
                #Get the path for the filename for the language_code
                xml_filename = config.get(XML_STRINGS_SECTION,language_code)
                # Return filepath for string given a language
                return join(output_directory, xml_filename)
            else:            
                # Return user configuration
                return user_config.get(OUTPUT_DIRECTORIES_SECTION,filetype)
        else:
            # Return default configuration
            return config.get(OUTPUT_DIRECTORIES_SECTION,filetype)
    except ConfigParser.NoOptionError:
        #TODO: Handle properly this error
        return "Path not found", filetype, language_code


def get_properties_path(language):
    """ Return the path for the properties given the language """
    config = read_config()
    return join(config.get(OUTPUT_DIRECTORIES_SECTION,PROPERTIES_OPTION),
                language+
                config.get(EXTENSIONS_SECTION, PROPERTIES_EXTENSION))


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
        exit("The template path for: {0}, has not been found.".format(template))
    # Return the path to tempalate file.
    return join(root_path,template_path),template_name

#TODO: If interpolation is false get_property_interpolation and get_property do exactly the same. Merge!
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

def get_ontology_level(ontology_id,tree_level,dicom_tag=None,languages_tag=None,language=None):
    """ 
    Return the level name.

    Keyword Arguments:
    ontology_id -- Odontolgy ID of the report. 
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
    ontology_path = get_properties_path(comments_language)
    config = read_config(ontology_path)
    ontology_section = ontology_id+' '+LEVEL_STRINGS
    #TODO: Handle the exceptions
    return config.get(ontology_section,str(tree_level))

def get_substitution_dictionary(language_code,section,template_type):
    """  Read properties file for the language and returns a dictionary 
    with substitution words for this language
    Multiple is a boolean parameter. If it is true the template is filled multiple times,
    so, we return a dictionary with every possible substitution. 
    
    """
    config = ConfigParser.SafeConfigParser()
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

def get_filepath_ontology(ontology_id, filetype):
    """ Retun layouts filenames inside a dictionary, the key is the level id and the value is the filename

    Keyword:
    ontology_id -- ontology id of the report. Every ontology has its own layout configuration in 
    the settings file
    filetype -- file type of the filenames we are looking for (layouts or activities).

    """
    config = read_config()
    # Get layouts filepath
    # Get the ouputs directory
    output_directory = get_filepath(filetype)
    # If the directory does not exist, create it. 
    if( not exists(output_directory)):
        makedirs(output_directory)
    # Read the ontology settings file
    ontology_settings_path = config.get(ONTOLOGIES_SETTINGS,ONTOLOGIES_PATH)
    extension = config.get(EXTENSIONS_SECTION,SETTINGS_EXTENSION)
    ontology_settings_file = join(ontology_settings_path,ontology_id+extension)

    #Get the templates for the file names. 
    ontology_config = read_config(ontology_settings_file)
    section = ONTOLOGY_FILENAMES
    options = ontology_config.options(section)
    filenames = {}
    #Get files extension
    if (filetype == LAYOUTS):
        extension = config.get(EXTENSIONS_SECTION,XML_EXTENSION)
    elif (filetype == ACTIVITIES):
        extension = config.get(EXTENSIONS_SECTION,JAVA_EXTENSION)
        # For every level build the filename. 
    for option in options:
        level = option.replace(LEVEL_TAG,'')
        #Get the filename. If it's an activity it need to be capitalize.
        if (filetype == LAYOUTS):
            filename = ontology_config.get(section,option)+extension
        elif (filetype == ACTIVITIES):
            template_name = ontology_config.get(section,option)
            template_capitalize = template_name[0].upper() + template_name[1:]
            filename = template_capitalize+extension
        filenames[level] = join( output_directory,filename)
    return filenames
    
# TODO: get_layout_settings and get_children_settings are just looking in different sections. Merge!
def get_layout_settings(ontology_id, level):
    """ Return a layout distribution for ontology and level given
    set by the user in the settings.ini file. (1 column or 2 columns)

    """
    #Get the default config file
    config = read_config()

    # Read the ontology settings file
    ontology_settings_path = config.get(ONTOLOGIES_SETTINGS,ONTOLOGIES_PATH)
    extension = config.get(EXTENSIONS_SECTION,SETTINGS_EXTENSION)
    ontology_settings_file = join(ontology_settings_path,ontology_id+extension)
    # Get the ontolgy settings. And from this get the 
    ontology_config = read_config(ontology_settings_file)
    layout_option = LEVEL_TAG + level
    return ontology_config.get(LAYOUT_SETTINGS,layout_option)

def get_children_settings(ontology_id, level):
    """ Return children layout distribution for ontology and level given
    set by the user in the settings.ini file. (ExpandableListView or Listview)

    """
    #Get the default config file
    config = read_config()

    # Read the ontology settings file
    ontology_settings_path = config.get(ONTOLOGIES_SETTINGS,ONTOLOGIES_PATH)
    extension = config.get(EXTENSIONS_SECTION,SETTINGS_EXTENSION)
    ontology_settings_file = join(ontology_settings_path,ontology_id+extension)

    # Get the ontolgy settings. And from this get the 
    ontology_config = read_config(ontology_settings_file)
    children_option = LEVEL_TAG + level + CHILDREN_TAG
    return ontology_config.get(LAYOUT_SETTINGS,children_option)


def get_template_model_file():
    """ Return filename for java model """
    output_directory = get_filepath(MODEL_OUTOUT_OPTION)
    model_template = get_property(TEMPLATES_SECTION,MODEL_FILE)
    if (not exists(output_directory)):
        makedirs(output_directory)
    return join(output_directory,model_template)
