#  -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, TemplateNotFound
from os.path import join, exists
from core.config_variables import (TEMPLATE_BY_ID, TEMPLATE_BY_REPORT,
                                   STRING_TEMPLATES, STRING_TEMPLATES_PATH,
                                   TEMPLATES_SECTION, TEMPLATES_ROOT_PATH,
                                   TEMPLATE_PACKAGE)
from core.config import (get_template_filename, get_property, 
                         get_substitution_dictionary, set_environment)

#TODO: Capture the exceptions
def substitute_words(environment, section,
                     template_name, languages, template_var):
    """ Return localized strings
    in a dictionary if it is not multiple substitution or
    in a list of dictiories if there are multiple substitutions

    Keyword Arguments:
    environment -- jinja2 enviornment
    section -- section in the properties file with the strings to replace.
    template_name -- name of the template.
    language_code -- code for the dicom tags.
                     it has a relation of the supported languages.
    template_var -- string with the template var name from config_variables

    """
    # Get the jinja2 template
    template = environment.get_template(template_name)
    # Get the localized words for being replace in the template
    localized_strings = {}
    for language in languages:
        localized_strings[language] = template.render(
            get_substitution_dictionary(language, section, template_var))
    return localized_strings


def get_localized_report(environment, template_name, language_code,
                         template_var, report):
    """ Returns a list of localized string from the report

    Keyword Arguments:
    environment -- jinja2 enviornment
    template_name -- name of the template
    language_code -- code for the dicom tags.
                     It has a relation of the supported languages.
    Template_var -- string with the template var name from config_variables
    report -- dicom report where information is taken.

    """
    template = environment.get_template(template_name)
    # Get a dictionary with words that will be used in the template.
    substitution_languages = report.get_data_form_report(
        language_code, template_var)
    strings_render = {}
    for language, dict_words in substitution_languages.iteritems():
        strings_render[language] = template.render(dict_words)
    return strings_render


def write_template(template, languages, xml_files, report=None):
    """ Write a piece of localized template

    Keyword Arguments:
    template -- template name for being localized and written.
    language -- Language code, following i18n, to write.
    xml_file -- file open for write where
                the template should be written. (default None)
    report -- dicom report where information is taken.

    """
    # Set the section of the template name for the strings.
    if (report is not None):
        if (template in TEMPLATE_BY_ID):
            section = report.get_ontology() + " " + template
        elif (template in TEMPLATE_BY_REPORT):
            section = template
    else:
        section = template
    # Get the template path and its filename
    template_path, template_filename = get_template_filename(template)

    # The template is STRING type. 
    # This handler only get string templates. So this check is redundant
    # if (template in STRING_TEMPLATES):
    env = set_environment(STRING_TEMPLATES_PATH)
    # Localize the template for this language
    # Get localized strings from Report Data
    if (template in TEMPLATE_BY_REPORT):
        localized_strings = get_localized_report(env, template_filename,
                                                 languages, template, report)
    #Templates localized by Report Ontology ID or default strings. 
    else:
        localized_strings = substitute_words(env, section, template_filename,
                                             languages, template)
        
    #Write the localized string
    for language, localized_string in localized_strings.iteritems():
        xml_files[language].write(
            u'{0}'.format(localized_string).encode('utf-8'))
