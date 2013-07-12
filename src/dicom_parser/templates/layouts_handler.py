#  -*- coding: utf-8 -*-
from os.path import isfile
from core.config import set_environment, get_property, get_language_code
from core.config_variables import (LAYOUT_TEMPLATES_PATH, 
                                   LAYOUT_TEMPLATES_SECTION, TWO_COLUMNS,
                                   ONE_COLUMN, NUM, DATE, TEXT, TREE_TITLE,
                                   GENERIC_TITLE,NEXT_LEVEL, BOOL, SCROLL,
                                   LISTVIEW, EXPANDABLELISVIEW)

#TODO: Check when is been used GENERIC_TITLE, TREE_TITLE, NEXT_LEVEL and SCROLL 

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


def get_template_substitution(environment, template_type, concept=None,
                              report_level=None, previous_item=None,
                              language=None):
    """ Return a temp snippet that does requiere subtitution
    and the current item to nest template levels.

    """
    #print template_type
    template_name = get_property(LAYOUT_TEMPLATES_SECTION, template_type)
    template = environment.get_template(template_name)
    render_template = ""
    # Strore in a variable the current item id. We will need this when
    # we write self dependent layout items.
    current_item = ""
    # TITLE of a tree section
    if (template_type == TREE_TITLE):
        render_template = template.render(level=concept.value)
        # TODO: find a better way to do this. Dependent on the template
        # using a regex to find "#+id/    \n", and not hardcoded here.
        current_item = "level_{0}_label".format(concept.value)
    # TITLE of a generic section
    elif (template_type == GENERIC_TITLE):
        render_template = template.render(level=report_level)
        current_item = "level_{0}_label".format(report_level)
    # Listview for next (deeper) level of the dicom tree.
    elif (template_type == NEXT_LEVEL):
        render_template = template.render(code=concept.value,
                                          parent_code=concept.value)
        current_item = "children_{0}_list".format(concept.value)
    # NUM type attribute & TEXT type attribute
    elif (template_type == NUM or template_type == TEXT):
        localized_concept = concept.meaning[language]
        render_template = template.render(concept_name=localized_concept,
                                          concept_value=concept.value,
                                          previous_item=previous_item)
        current_item = "etext_{0}".format(concept.value)
    # BOOL type attribute
    elif (template_type == BOOL):
        localized_concept = concept.meaning[language]
        render_template = template.render(concept_name=localized_concept,
                                          concept_value=concept.value,
                                          previous_item=previous_item)
        current_item = "cbox_{0}".format(concept.value)
    # DATE type attribute
    elif (template_type == DATE):
        localized_concept = concept.meaning[language]
        render_template = template.render(concept_name=localized_concept,
                                          concept_value=concept.value,
                                          previous_item=previous_item)
        current_item = "etext_{0}".format(concept.value)
    # SCROLL
    elif (template_type == SCROLL):
        render_template = template.render(parent=previous_item)
    # LISTVIEW & EXPANDABLELISVIEW
    elif (template_type == LISTVIEW or template_type == EXPANDABLELISVIEW):
        render_template = template.render(concept_value=concept.value,
                                          previous_item=previous_item)
        current_item = "list_{0}".format(concept.value)

    return render_template, current_item


def get_attributes_list(environment, attributes,
                        previous_item, language_code):
    """ Retrun a list of Android layout xml snipppets for the attributes
    passed as parameter.

    Keyword Arguments:
    environment --jinja2 environment variable.
    attributes -- DICOM attributes used to generate Android XML Layout
    previous_item -- Last item ID. Used to nest layout levels.
    language_code -- code with supported languages.
                     Used to get the default language.
    """
    attributes_layouts = []
    current_item = ""
    # Get android xml layout for every attribute
    for attribute in attributes:
        # Discriminate if an attributes is boolean
        if (attribute.type == NUM and attribute.is_bool()):
            attribute_type = BOOL
        else:
            attribute_type = attribute.type
        #print u" - {0} ({1})".format(
        #    attribute.concept.meaning,
        #    attribute_type).encode('utf-8')
        #TODO: Discriminate between num and bool
        if(attribute_type == NUM or attribute_type == DATE or
           attribute_type == TEXT or attribute_type == BOOL):
            # Get the concept name in the default language.
            # TODO: Check if this (comments in default language)
            #is "really" needed.
            default_language = get_language_code('CODE_MEANING', language_code)
            attribute_layout, current_item = get_template_substitution(
                environment,
                attribute_type,
                concept=attribute.concept,
                previous_item=previous_item,
                language=default_language)
            attributes_layouts.append(attribute_layout)
            previous_item = current_item
            #print current_item
        else:
            #Throw an error
            current_item = previous_item
    #print
    return attributes_layouts, current_item


def get_children_list(environment, children_code,
                      previous_item, children_layout):
    children, current_item = get_template_substitution(
        environment,
        children_layout,
        concept=children_code,
        previous_item=previous_item)
    return [children], current_item


#TODO: add the behaviour to support a layout with only attributes too ->
#      -> write_one_column_layout_one_level
def write_one_column_layout_one_level(layout_filename, container, children,
                                      children_layout):
    """ Write a layout with one columns where there are only children

    Keyword Arguments:
    report_level -- level of the report to write
    xml_filename -- file name where the layout should be written
    dict_level -- DICOM report where information is to write in the xml layout

    """
    #If the concept have already generate a layout don't do it again.
    if (not isfile(layout_filename)):
        #print(" * {0}".format(container))
        layout_file = open(layout_filename, 'w')
        # Set the Environment for the jinja2 templates.
        environment = set_environment(LAYOUT_TEMPLATES_PATH)

        # There are ONLY CHILDREN in this layout
        if (len(children) > 0):
            # Get the template
            template_name = get_property(LAYOUT_TEMPLATES_SECTION,
                                         ONE_COLUMN)
            template = environment.get_template(template_name)
            # Store previous concept id
            previous_item = "code_{0}".format(container.get_code())
            items, current_item  = get_children_list(environment,
                                                     container.get_concept(),
                                                     previous_item,
                                                     children_layout)

            # Render layout template with correct values.
            layout_file.write(template.render(level_code=container.get_code(),
                                              items_list=items)
                              .encode('utf-8'))
            layout_file.close()

        # TODO: There are ONLY ATTRIBUTES in this layout
        if (len(container.attributes) > 0):
            pass
    else:
        print "Layout {0} already created".format(layout_filename)


def write_two_columns_layout(layout_filename, container, children,
                             children_layout, language_code):
    #print container.concept, children
    #If the concept have already generate a layout don't replicate.
    if (not isfile(layout_filename)):
        layout_file = open(layout_filename, 'w')
        print(" * {0}".format(container))
        # Set the Environment for the jinja2 templates.
        environment = set_environment(LAYOUT_TEMPLATES_PATH)

        # Get the template
        template_name = get_property(LAYOUT_TEMPLATES_SECTION,
                                     TWO_COLUMNS)
        template = environment.get_template(template_name)

        # Store previous concept id
        previous_item = "code_{0}".format(container.get_code())

        # There are ONLY ATTRIBUTES in this layout
        if (len(container.attributes) > 0 and len(children) == 0):
            # Split attributes in two columns
            num_attributes = len(container.attributes)
            left_attributes = container.attributes[0:(num_attributes / 2)]
            right_attributes = container.attributes[(num_attributes / 2):]
            # Get the attributes list
            left_items, previous_item  = get_attributes_list(environment,
                                                             left_attributes,
                                                             previous_item,
                                                             language_code)
            right_items, previous_item = get_attributes_list(environment,
                                                             right_attributes,
                                                             previous_item,
                                                             language_code)
        # There are ATTRIBUTES and CHILDREN in this layout
        elif((len(container.attributes) > 0) and (len(children) > 0)):
            attributes = container.attributes
            concept = container.get_concept()
            # Get the attributes list
            left_items, previous_item  = get_attributes_list(environment,
                                                             attributes,
                                                             previous_item,
                                                             language_code)
            right_items, previous_item = get_children_list(environment,
                                                           concept,
                                                           previous_item,
                                                           children_layout)
        try:
            # Render layout template with correct values.
            layout_file.write(template.render(level_code=container.get_code(),
                                              left_items=left_items,
                                              right_items=right_items)
                              .encode('utf-8'))
            layout_file.close()

        except NameError:
            layout_file.close()
            print "Error generating layout items for layout {0}".format(
                layout_filename)
    else:
        print "Layout {0} already created".format(layout_filename)
