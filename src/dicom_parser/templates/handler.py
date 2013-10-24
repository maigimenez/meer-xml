 #  -*- coding: utf-8 -*-
from os.path import isfile
from core.config import (get_filepath, get_layout_settings,
                         get_template_model_file, get_languages,
                         instantiate_filename, get_class_name, get_model_file,
                         set_environment, get_property, get_parent_code_schema,
                         get_children_settings)
from core.config_variables import (COLUMN_1, COLUMNS_2, STRINGS,
                                   DEFAULT_STRINGS, LEVEL_STRINGS,
                                   CHILDREN_ARRAYS, DICOM_LEVEL,
                                   MODEL_TEMPLATES_PATH,
                                   ACTIVITIES_TEMPLATES_PATH,
                                   MODEL_TEMPLATES_SECTION, CLASS_TEMPLATE,
                                   ANDROID_PACKAGES, PACKAGE_MODEL, BASE_MODEL,
                                   CHILD_CLASS, CODE_ARRAYS)
from core.java_types import (CLASS, IMPLEMENTS)
from strings_handler import write_template
from layouts_handler import (write_two_columns_layout,
                             write_one_column_layout_one_level)
from activities_handler import (write_manifest, get_activity_filename,
                                get_activity_name, write_activity_file,
                                write_application)
from model_handler import (get_attributes, get_children, get_parent_class,
                           add_tree_hierarchy)
from string import Template


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
        strings_filename[language] = get_filepath(STRINGS, language)
        strings_files[language] = open(strings_filename[language], 'w')
        strings_files[language].write(
            u'<?xml version=\"1.0\" encoding=\"utf-8\"?>\n')
        strings_files[language].write(u'<resources>')

    # Write default strings for every language and close the resources
    write_template(DICOM_LEVEL, languages, strings_files, report)
    write_template(DEFAULT_STRINGS, languages, strings_files)
    write_template(LEVEL_STRINGS, languages, strings_files, report)
    write_template(CHILDREN_ARRAYS, languages, strings_files, report)
    write_template(CODE_ARRAYS, languages, strings_files, report)

    # Write closing tags for the xml files
    for language in languages:
        strings_files[language].write(u'\n</resources>')
        strings_files[language].close()

###################################LAYOUTS###################################


def write_layouts(xml_filenames, report, language_code):
    #print xml_filenames
    flat = report.get_flat_data()
    #Get the ontology id of the report
    ontology_id = report.get_ontology()
    #Write layout for every file
    for container, children in flat.iteritems():
        level_layout = get_layout_settings(ontology_id,
                                           str(container.tree_level))
        # Get the preferred children distribution, if there are children
        if(children):
            children_layout = get_children_settings(ontology_id,
                                                    str(container.tree_level))
        else:
            children_layout = None
        #print
        #print "[Level {0}] {1}".format(container.tree_level, level_layout)
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

##########################JAVA #########################################


def write_model(java_filenames, report, language_code):
    template_model_file = get_template_model_file()

    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(MODEL_TEMPLATES_PATH)
    package = get_property(ANDROID_PACKAGES, PACKAGE_MODEL)
    # Store an ids list of expandable.
    expandables = []
    flat_tree = {}

    #Write model for every container.
    for container, children in report.report.depthFirstChildren():
        imports = []

        #Get parent code, parent schema and grandparent class
        parent_code, parent_schema, gparent_class = get_parent_class(flat_tree,
                                                                     container)

        # Build this container java filename using its parent codes and its own
        class_name = get_class_name(container.get_schema(),
                                    container.get_code(),
                                    parent_schema,
                                    parent_code).replace('-', '_')

        # Build a parent/children codes hash table.
        # We will use it for parent_code and schema.
        if (children):
            add_tree_hierarchy(flat_tree, container, children, class_name)

        model_filename = get_model_file(template_model_file, class_name)

        # Write model
        if (not isfile(model_filename)):
            model_file = open(model_filename, 'w')
            # Get the attributes.
            attributes, methods = get_attributes(environment,
                                                 container.attributes,
                                                 imports)
            # Get children attributes and its methods
            parent_class = (container.get_schema().lower().capitalize() +
                            '_' + container.get_code().lower())

            c_attributes, c_methods = get_children(environment,
                                                   children,
                                                   imports,
                                                   parent_class,
                                                   class_name,
                                                   expandables,
                                                   template_model_file,
                                                   package)

            attributes.extend(c_attributes)
            methods.extend(c_methods)
            #Write the model
            # If this class will be expandable in activity.
            # Child class should extend its parent interface.
            template_name = get_property(MODEL_TEMPLATES_SECTION,
                                         CLASS_TEMPLATE)
            template = environment.get_template(template_name)
            # If this class has expandables it has to implement
            # the children interface class
            has_multiple_children = container.properties.max_cardinality == -1
            if (class_name in expandables and has_multiple_children):
                implement_class = Template(IMPLEMENTS).safe_substitute(
                    PARENT_CLASS=gparent_class + CHILD_CLASS)
                model_file.write(
                    template.render(package=package,
                                    class_type=CLASS,
                                    class_name=class_name,
                                    attributes=attributes,
                                    imports=imports,
                                    implements_class=implement_class,
                                    methods=methods))
            else:
                model_file.write(
                    template.render(package=package,
                                    class_type=CLASS,
                                    class_name=class_name,
                                    attributes=attributes,
                                    imports=imports,
                                    methods=methods))
            model_file.close()
        else:
            print "Java class {0} already created".format(model_filename)


def write_activities(activities_filenames, report):
    flat = report.get_flat_data()

    #Get the ontology id of the report
    ontology_id = report.get_ontology()

    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(ACTIVITIES_TEMPLATES_PATH)

    # Get report root container. This will be the launcher activity.
    report_root = report.get_root().get_schema_code()

    # Variables to store data
    activities = []
    launcher_activity = ""

    package = get_property(ANDROID_PACKAGES, BASE_MODEL)

    # Get containers position. It must match strings-array position.
    position = {}
    report.get_data_from_report(CHILDREN_ARRAYS, position=position)

    #Write layout for every file
    for container, children in flat.iteritems():
        activity = {}

        # Get this container's parent code and Schema
        parent_code, parent_schema = get_parent_code_schema(flat, container)

        activity_filename = get_activity_filename(activities_filenames, flat,
                                                  container, parent_code,
                                                  parent_schema)
        activity_name = get_activity_name(activity_filename)
        
        # Store info to write the Android Manifest
        # Check if this activity is the launcher
        # TODO : (on liner) activity['launcher'] = (container.get_schema_code() == report_root) 
        if (container.get_schema_code() == report_root):
            activity['launcher'] = True
        else:
            activity['launcher'] = False
        activity['name'] = activity_name
        activities.append(activity)

        # Log purpose info
        #print "[Level {0}] {1}".format(container.tree_level, children_layout)
        #print activity_filename, package, a_name

        write_activity_file(environment, ontology_id, package,
                            activities_filenames, activity_filename,
                            activity_name, container, children, position,
                            parent_schema, parent_code)
    
    report_class = report_root.lower().capitalize()
    write_application(package, report_class)
    write_manifest(package, activities)
