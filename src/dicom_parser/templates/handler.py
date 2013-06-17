#  -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, TemplateNotFound
from os.path import join, exists, isfile
from string import Template
from core.config import (get_template_filename, get_property,
                         get_xml_filepath, get_substitution_dictionary,
                         get_layout_settings, get_language_code)
from core.config_variables import (I18N_INPUT, I18N, STRING_TEMPLATES,
                                   STRING_TEMPLATES_PATH, TEMPLATES_SECTION,
                                   TEMPLATES_ROOT_PATH, TEMPLATE_PACKAGE,
                                   TEMPLATE_BY_REPORT, TEMPLATE_BY_ID,
                                   COLUMN_1, COLUMNS_2, LAYOUT_TEMPLATES_PATH,
                                   HEADER, MAIN_LEFT, TREE_TITLE,
                                   LAYOUT_TEMPLATES_SECTION, DEFAULT,
                                   DEFAULT_INPUT, GENERIC_TITLE, NUM, END,
                                   NEXT_LEVEL, DATE, TEXT, STRINGS,
                                   DEFAULT_STRINGS, LEVEL_STRINGS,
                                   CHILDREN_ARRAYS, DICOM_LEVEL, BOOL, RIGHT,
                                   SCROLL)


def get_languages(language_code):
    """ Return the languages supported  based on the language_code """
    if (language_code == I18N_INPUT):
        return I18N
    elif (language_code == DEFAULT_INPUT):
        return DEFAULT
    return None


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


#TODO: Capture the exceptions
def substitute_words(environment, section,
                     template_name, languages, template_var):
    """ Return localized strings
                        write_two_columns_layout_one_level(report_level,
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
            section = report.get_odontology() + " " + template
        elif (template in TEMPLATE_BY_REPORT):
            section = template
    else:
        section = template
    # Get the template path and its filename
    template_path, template_filename = get_template_filename(template)

    # The template is STRING type
    if (template in STRING_TEMPLATES):
        env = set_environment(STRING_TEMPLATES_PATH)
        # Localize the template for this language
        # Get localized strings from report or form properties
        if (template in TEMPLATE_BY_REPORT):
            localized_strings = get_localized_report(
                env, template_filename, languages, template, report)
        else:
            localized_strings = substitute_words(env, section,
                                                 template_filename, languages,
                                                 template)

        #Write the localized string
        for language, localized_string in localized_strings.iteritems():
            xml_files[language].write(
                u'{0}'.format(localized_string).encode('utf-8'))


def write_strings(language_code, report):
    """ Write all needed strings in report for all supported languages.

    Keyword Arguments:
    language_code -- languages supported.
    report -- DICOM report where the information is.
    """
    #Get supported languages.
    languages = get_languages(language_code)
    strings_filename = {}
    strings_files = {}
    # Get and open current language file
    for language in languages:
        strings_filename[language] = get_xml_filepath(language, STRINGS)
        strings_files[language] = open(strings_filename[language], 'w')
        strings_files[language].write(
            u'<?xml version=\"1.0\" encoding=\"utf-8\"?>\n')
        strings_files[language].write(u'<resources>')

    # Write default strings for every language and close the resources
    write_template(DICOM_LEVEL, languages, strings_files, report)
    write_template(DEFAULT_STRINGS, languages, strings_files)
    write_template(LEVEL_STRINGS, languages, strings_files, report)
    write_template(CHILDREN_ARRAYS, languages, strings_files, report)

    # Write closing tags for the xml files
    for language in languages:
        strings_files[language].write(u'\n</resources>')
        strings_files[language].close()

###################################LAYOUTS###################################


def write_template_snippet(layout_file, template_name):
    """ Write a template snippet that does NOT requiere substitution
    at the end of the layout file given

    """
    #Get the template_type path
    template_root_path, template_name = get_template_filename(template_name)
    template_path = join(template_root_path, template_name)
    #Open the template, read its content and write in in the layout xml file.
    template_file = open(template_path, 'r')
    for line in template_file:
        layout_file.write(line)
    template_file.close()


def write_template_substitution(environment, layout_file, template_type,
                                concept=None, report_level=None,
                                previous_item=None, language=None):
    """ Write a template snippet that does requiere substitution
    to fill the template

    """
    print template_type
    template_name = get_property(LAYOUT_TEMPLATES_SECTION, template_type)
    template = environment.get_template(template_name)
    render_template = ""
    # Strore in a variable the current item id. We will need this when
    # we write self dependent layout items.
    current_item = ""
    # Title of a tree section
    if (template_type == TREE_TITLE):
        render_template = template.render(level=concept.concept_value)
        # TODO: find a better way to do this. Dependent on the template
        # using a regex to find "#+id/    \n", and not hardcoded here.
        current_item = "level_{0}_label".format(concept.concept_value)
    # Title of a generic section
    elif (template_type == GENERIC_TITLE):
        render_template = template.render(level=report_level)
        current_item = "level_{0}_label".format(report_level)
    # Listview for next (deeper) level of the dicom tree.
    elif (template_type == NEXT_LEVEL):
        render_template = template.render(code=concept.concept_value,
                                          parent_code=concept.concept_value)
        current_item = "children_{0}_list".format(concept.concept_value)
    # Num type attribute
    elif (template_type == NUM or template_type == TEXT):
        localized_concept = concept.concept_name[language]
        render_template = template.render(concept_name=localized_concept,
                                          concept_value=concept.concept_value,
                                          previous_item=previous_item)
        current_item = "etext_{0}".format(concept.concept_value)
    elif (template_type == SCROLL):
        render_template = template.render(parent=previous_item)
    #Write the template instatiated in layout file
    layout_file.write(render_template.encode('utf-8'))
    return current_item


def get_layout_file(report_level, xml_filename, concept, parent):
    """ Reuturn filename of current layout
    based on the concept and its parent. """
    # Add the concept_value to the layout file and open the file for writting
    if (int(report_level) == 1):
        filename = xml_filename
    else:
        filename = Template(xml_filename).safe_substitute(
            CODE=concept.concept_value.lower(),
            PARENT=parent.lower())
    return filename


def write_attributes_layout(environment, layout_file, attributes,
                            previous_item, language_code):
    print len(attributes)
    for attribute in attributes:
        #print " - {0}".format(attribute.type)
        if (attribute.type == NUM and attribute.is_bool()):
            attribute_type = BOOL
        else:
            attribute_type = attribute.type
        print u" - {0} ({1})".format(
            attribute.concept.concept_name,
            attribute_type).encode('utf-8')
        #TODO: Discriminate between num and bool
        if(attribute_type == NUM or attribute_type == DATE or
           attribute_type == TEXT or attribute_type == BOOL):
            # Get the concept name in the default language.
            # TODO: Check if this is "really" needed.
            default_language = get_language_code('CODE_MEANING', language_code)
            current_item = write_template_substitution(
                environment,
                layout_file,
                attribute.type,
                concept=attribute.concept,
                previous_item=previous_item,
                language=default_language)
            previous_item = current_item
            print current_item
        else:
            #Throw an error
            current_item = previous_item
    print
    return current_item


#TODO: add the behaviour to support a layout with only attributes too ->
#      -> write_one_column_layout_one_level
def write_one_column_layout_children(report_level, xml_filename, report):
    """ Write a layout with one columns where there are only children

    Keyword Arguments:
    report_level -- level of the report to write
    xml_filename -- file name where the layout should be written
    dict_level -- DICOM report where information is to write in the xml layout

    """
    dict_level = report.get_level(int(report_level))
    for concept, children in dict_level.containers.iteritems():
        parent = report.get_parent_code(int(report_level), concept)
        layout_filename = get_layout_file(report_level, xml_filename, concept,
                                          parent)
        #If the concept have already generate a layout don't do it again.
        if (not isfile(layout_filename)):
            layout_file = open(layout_filename, 'w')
            print(" * {0} \n {1}".format(concept, layout_filename))
            # Set the Environment for the jinja2 templates.
            environment = set_environment(LAYOUT_TEMPLATES_PATH)
            # Write those templates snippet than does not need substitution
            # Write the header, main and left layout
            write_template_snippet(layout_file, HEADER)
            write_template_snippet(layout_file, MAIN_LEFT)
            # There are ONLY CHILDREN in this layout
            # Get the template snippet,find the subtitution terms
            # and write the template
            write_template_substitution(environment, layout_file,
                                        TREE_TITLE, concept=concept)
            write_template_substitution(environment, layout_file,
                                        NEXT_LEVEL, concept=concept)
            #Write layout end, close open xml tags.
            write_template_snippet(layout_file, END)
            print
            layout_file.close()
        else:
            print "Layout {0} already created".format(layout_filename)


def write_two_columns_layout_one_level(level, layout_filename, concept,
                                       children, language_code):
    layout_file = open(layout_filename, 'w')
    print(" * {0}".format(concept))
    # Set the Environment for the jinja2 templates.
    environment = set_environment(LAYOUT_TEMPLATES_PATH)
    # Write those templates snippet than does not need substitution
    # Write the header, main and left layout
    write_template_snippet(layout_file, HEADER)
    write_template_snippet(layout_file, MAIN_LEFT)

    # There are ONLY ATTRIBUTES in this layout
    if (len(children.attributes) > 0):
        # Get the template snippet, find the subtitution terms and
        # write the template
        write_template_substitution(environment, layout_file,
                                    GENERIC_TITLE, report_level=level)
        # Store previous concept id
        previous_item = "level_{0}_label".format(level)
        # Write the scoll for the attributes 
        write_template_substitution(environment, layout_file,
                                    SCROLL, previous_item=previous_item)        
        # Split attributes in two columns
        num_attributes = len(children.attributes)
        first_attributes = children.attributes[0:(num_attributes / 2)]
        last_attributes = children.attributes[(num_attributes / 2):]
        #Write the attributes
        previous_item = write_attributes_layout(environment, layout_file,
                                                first_attributes,
                                                previous_item, language_code)
        #Write the end of left layout, the right layout
        write_template_snippet(layout_file, RIGHT)
        # Write the scoll for the attributes 
        write_template_substitution(environment, layout_file,
                                    SCROLL, previous_item=previous_item)        

        previous_item = write_attributes_layout(environment, layout_file,
                                                last_attributes,
                                                previous_item, language_code)
        write_template_snippet(layout_file, END)
        layout_file.close()

    # There are ONLY CHILDREN in this layout
    else:
        pass 


def write_two_columns_layout_two_levels():
    pass


def write_two_columns_layout(report_level, xml_filename, report,
                             language_code):
    parent_level = report.get_level(int(report_level) - 1)
    # If parent_level is None we are in the root level.
    if (parent_level is not None):
        for parent, dict_level in parent_level.containers.iteritems():
            for level_children in dict_level.children_containers:
                layout_filename = get_layout_file(report_level, xml_filename,
                                                  level_children,
                                                  parent.concept_value)
                #If the concept have already generate a layout don't replicate.
                if (not isfile(layout_filename)):
                    # Get the level to write its layout
                    children_to_write = report.get_children(
                        int(report_level), level_children)
                    if(len(children_to_write.attributes) == 0 or
                       len(children_to_write.children_containers) == 0):
                        print "{0}: One Level".format(layout_filename)
                        write_two_columns_layout_one_level(report_level,
                                                           layout_filename,
                                                           level_children,
                                                           children_to_write,
                                                           language_code)
                    else:
                        print "Two levels"
                        #write_two_columns_layout_two_levels(xml_files,
                        #filename,level,concept,children)
                else:
                    print "Layout {0} already created".format(layout_filename)
            print


def write_layouts(xml_filenames, report, language_code):
    print xml_filenames
    for level, layout_filename in xml_filenames.items():
       #Get the odontology id of the report
        odontology_id = report.get_odontology()
        #Get the actual level to write its layout
        #dict_level = report.get_level(int(level))
        #parent_code = report.get_parent_code(int(level))
        #print "parent", parent_code, " level: ", level
        #Get the level distribution for this level.
        level_settings = get_layout_settings(odontology_id, level)
        print "[Level {0}] {1}".format(level, level_settings)
        if (level_settings == COLUMN_1):
            # TODO: Discriminate between layouts with children,
            # attributes or both.
            write_one_column_layout_children(level, layout_filename,
                                             report)
        elif (level_settings == COLUMNS_2):
            write_two_columns_layout(level, layout_filename,
                                     report, language_code)
        print
