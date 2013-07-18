#  -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, TemplateNotFound
from os.path import join, exists, isfile
from core.config import (get_xml_filepath, get_substitution_dictionary,
                         get_layout_settings,
                         get_children_settings, get_template_model_file,
                         get_languages,instantiate_filename,
                         get_class_name,get_model_file, set_environment,
                         get_property)
from core.config_variables import (I18N_INPUT, I18N,
                                   COLUMN_1, COLUMNS_2,
                                   TREE_TITLE, NUM, TEXT, DATE,
                                   DEFAULT, DEFAULT_INPUT, STRINGS,
                                   DEFAULT_STRINGS, LEVEL_STRINGS,
                                   CHILDREN_ARRAYS, DICOM_LEVEL,
                                   MODEL_TEMPLATES_PATH,ACTIVITIES_TEMPLATES_PATH,
                                   MODEL_TEMPLATES_SECTION, CLASS,
                                   ANDROID_PACKAGES,PACKAGE_MODEL,
                                   BOOL_JAVA, STRING_JAVA, INT_JAVA,DATE_JAVA,
                                   CUSTOM_JAVA,BASE_MODEL, LISTVIEW, EXPANDABLELISVIEW,
                                   ACTIVITIES_TEMPLATES_SECTION, ACTIVITY, IMPORT_DATE)

from strings_handler import write_template
from layouts_handler import write_two_columns_layout, write_one_column_layout_one_level

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

def get_parent_code_schema(flat, container):
    for parent, children in flat.iteritems():
        for child in children:
            if (container == child):
                return parent.get_code(), parent.get_schema()
    return None,None


def write_layouts(xml_filenames, report, language_code):
    #print xml_filenames
    flat = report.get_flat_data()
    #Get the odontology id of the report
    odontology_id = report.get_odontology()
    #Write layout for every file
    for container, children in flat.iteritems():
        level_layout = get_layout_settings(odontology_id,
                                           str(container.tree_level))
        # Get the preferred children distribution, if there are children
        if(children):
            children_layout = get_children_settings(odontology_id,
                                                    str(container.tree_level))
        else:
            children_layout = None
        #print
        print "[Level {0}] {1}".format(container.tree_level, level_layout)
        # Get the filename for this container. It depends on its parent
        child_name = (container.get_schema() + '_' +
                      container.get_code())
        parent_code, parent_schema = get_parent_code_schema(flat, container)
        if (parent_code):
            parent_name = (parent_schema + '_' + parent_code)
        else:
            parent_name = None
        layout_filename_template = xml_filenames[str(container.tree_level)]
        layout_filename = instantiate_filename(str(container.tree_level),
                                               layout_filename_template,
                                               child_name,
                                               parent_name)
        #print layout_filename
        if (level_layout == COLUMN_1):
            # TODO: Discriminate between layouts with children,
            # attributes or both.
            write_one_column_layout_one_level(layout_filename, container,
                                              children, children_layout)
        elif (level_layout == COLUMNS_2):
            write_two_columns_layout(layout_filename, container, children,
                                     children_layout, language_code)

##########################################JAVA ##################################################


def write_model(java_filenames, report,language_code):
    template_model_file = get_template_model_file()
    flat = report.get_flat_data()
    
    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(MODEL_TEMPLATES_PATH)
    package = get_property(ANDROID_PACKAGES,PACKAGE_MODEL)

    for container,children in flat.iteritems():
        # Build this container java filename using its parent codes and its own
        parent_code, parent_schema = get_parent_code_schema(flat, container)
        class_name = get_class_name(container.get_schema(),
                                    container.get_code(),
                                    parent_schema,parent_code)
        model_filename = get_model_file(template_model_file,
                                        class_name)
        if (not isfile(model_filename)):
            #print "* {0} \n -> {1}".format(container,model_filename)
            #print
            model_file = open(model_filename, 'w')
            #TODO: Add the imports
            imports = []
            attributes = []
            # Render this container attributers
            for attribute in container.attributes:
                #print attribute.concept
                #print attribute.type
                render_template = ""
                attribute_name = attribute.concept.get_schema_code().lower().replace('-','_')
                # BOOL ATTRIBUTE
                if (attribute.type == NUM and attribute.is_bool()):
                    template_name = get_property(MODEL_TEMPLATES_SECTION, BOOL_JAVA)
                # NUM ATTRIBUTE
                elif (attribute.type == NUM and not attribute.is_bool()):
                    template_name = get_property(MODEL_TEMPLATES_SECTION, INT_JAVA)
                # TEXT ATTRIBUTE
                elif(attribute.type==TEXT):
                    template_name = get_property(MODEL_TEMPLATES_SECTION, STRING_JAVA)
                # DATE ATTRIBUTE
                elif(attribute.type==DATE):
                    template_name = get_property(MODEL_TEMPLATES_SECTION, DATE_JAVA)
                    import_temp_name = get_property(MODEL_TEMPLATES_SECTION,IMPORT_DATE) 
                    template_import = environment.get_template(import_temp_name)
                    render_import_template = template_import.render()
                    imports.append(render_import_template)

                template = environment.get_template(template_name)
                render_template = template.render(name=attribute_name)
                #print render_template, attribute_name
                attributes.append(render_template)
                

            # Render class attributes for this container's children
            for child in children:
                # Create the class name 
                attribute_variable = child.concept.get_schema_code().lower()
                parent_class = (container.get_schema().lower().capitalize() + 
                                '_' + container.get_code().lower())
                child_class_name = parent_class + '_' + attribute_variable

                template_name = get_property(MODEL_TEMPLATES_SECTION, CUSTOM_JAVA)
                template = environment.get_template(template_name)
                render_template = template.render(custom_class=child_class_name,
                                                  custom_variable=attribute_variable)
                attributes.append(render_template)

            template_name = get_property(MODEL_TEMPLATES_SECTION,CLASS)
            template = environment.get_template(template_name)
            model_file.write(template.render(package=package,
                                             class_name=class_name,
                                             attributes=attributes,
                                             imports=imports))
            model_file.close()
        else:
            print "Java class {0} already created".format(model_filename)

def write_activities(activities_filenames, report):
    flat = report.get_flat_data()
    #Get the odontology id of the report
    odontology_id = report.get_odontology()

    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(ACTIVITIES_TEMPLATES_PATH)

    #Write layout for every file
    for container, children in flat.iteritems():
        print
        print
        # Get the filenames for this container. It depends on its parent
        activity_filename_template = activities_filenames[str(container.tree_level)]
        child_name = (container.get_schema() + '_' +
                      container.get_code())
        parent_code, parent_schema = get_parent_code_schema(flat, container)
        if (parent_code):
            parent_name = (parent_schema + '_' + parent_code)
        else:
            parent_name = None

        activity_filename = instantiate_filename(str(container.tree_level),
                                               activity_filename_template,
                                               child_name,
                                               parent_name)

        layout_id = activity_filename.split('/')[-1].split('.')[0].lower()

        package = get_property(ANDROID_PACKAGES,BASE_MODEL)
        activity_name = activity_filename.split('/')[-1].split('.')[0]  
        if(children):
            children_layout = get_children_settings(odontology_id,
                                                    str(container.tree_level))
        else:
            children_layout = None
        print
        print "[Level {0}] {1}".format(container.tree_level, children_layout)
        print activity_filename, package, activity_name

        if (not isfile(activity_filename)):
            activity_file = open(activity_filename, 'w')
            render_children = None
            #If there are children, will be a listview or an expandable listview to load
            if (children_layout):
                template_name =  get_property(ACTIVITIES_TEMPLATES_SECTION,children_layout)
                template = environment.get_template(template_name)
                child_list = layout_id.split('_')[-1].upper()
                render_children = template.render(string_array=child_list)

            template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,ACTIVITY)
            template = environment.get_template(template_name)
            print render_children
            if (render_children):
                activity_file.write(template.render(package_name=package,
                                            activity_name=activity_name,
                                            layout_file=layout_id,
                                            childview=render_children))
            else:
                activity_file.write(template.render(package_name=package,
                                            activity_name=activity_name,
                                            layout_file=layout_id))
            print template_name
            activity_file.close()
        else:
            print "Activity {0} already created".format(activity_filename)              
