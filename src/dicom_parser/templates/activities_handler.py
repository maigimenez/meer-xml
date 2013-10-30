from os.path import join, exists, isfile
from os import makedirs
from core.config_variables import (MANIFEST, ACTIVITIES_TEMPLATES_PATH,
                                   ACTIVITIES_TEMPLATES_SECTION, CODE,
                                   ACTIVITIES, LISTADAPTER, ANDROID_PACKAGES,
                                   PACKAGE_MODEL, TEMPLATES_SECTION,
                                   LISTADAPTER_FILE, EXPANDABLE_ATTRIBUTES,
                                   SET_CHILDREN, EXPANDABLELISVIEW, ACTIVITY,
                                   APPLICATION, APPLICATION_FILE,
                                   ANDROID_PACKAGES, PACKAGE_MODEL)
from core.java_types import (IMPORT_CUSTOM, IMPORT_ARRAY,
                             IMPORT_EXPANDABLE_LISTVIEW)
from core.config import (set_environment, get_property, get_filepath,
                         instantiate_filename, get_children_settings,
                         get_class_name)
from string import Template


def write_manifest(package_name, activities,app_name):
    """ Write the Android Manifest file """

    # Get the AndroidManifest
    output_directory = get_filepath(MANIFEST)
    if (not exists(output_directory)):
            makedirs(output_directory)
    manifest_filename = get_property(ACTIVITIES_TEMPLATES_SECTION, MANIFEST)
    manifest_path = join(output_directory, manifest_filename)

    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(ACTIVITIES_TEMPLATES_PATH)
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION, MANIFEST)
    template = environment.get_template(template_name)

    # Open and write the manifest file
    manifest_file = open(manifest_path, 'w')
    manifest_file.write(template.render(package_name=package_name,
                                        app_name=app_name,
                                        activities=activities))
    manifest_file.close()


def get_spinners(attributes):
    """ Return a list of attributes which should be represented as a spinner

    Keyword arguments:
    attributes -- a list of container's attributes

    """
    spinners = []
    for attribute in attributes:
            if attribute.type == CODE:
                    spinners.append(attribute.concept.code)
    return spinners


def write_listAdapter(environment, package, c_class, c_code,
                      children_position, imports):
    """ Write custom list adapter for expandableListView class

    Keyword arguments:
    environment -- Jinja2 templates environment
    package -- Android package where this adapter should be
    c_class -- child class.
    c_code -- child schema and code.
    children_position -- list with children positons.
    imports -- import list to add any new class.

    """
    # Instantiate LISTVIEW ADAPTER
    # Get listView Adapter Template
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,
                                 LISTADAPTER)
    template = environment.get_template(template_name)

    # Get data model package and include it in imports.
    model_package = get_property(ANDROID_PACKAGES, PACKAGE_MODEL)
    imports.append(Template(IMPORT_CUSTOM).
                   safe_substitute(PACKAGE=model_package,
                                   CLASS=c_class + '_Group'))
    imports.append(Template(IMPORT_CUSTOM).
                   safe_substitute(PACKAGE=model_package,
                                   CLASS=c_class + '_Children'))

    # Get custom listView Adapter
    list_adapter = template.render(package_name=package,
                                   container_class=c_class,
                                   string_array=c_code,
                                   imports=imports,
                                   children=children_position)

    # WRITE CUSTOM LISTVIEW ADAPTER
    template_filename = get_property(TEMPLATES_SECTION,
                                     LISTADAPTER_FILE)
    # Get the output path
    path = get_filepath(ACTIVITIES)

    adapter_filename = join(path,
                            (Template(template_filename).
                             safe_substitute(CLASS_NAME=c_code)))
    # TODO: Check if this file already exists
    adapter_file = open(adapter_filename, 'w')
    adapter_file.write(list_adapter)
    adapter_file.close()


def get_children_position(child_level, position, c_activity_template,
                          p_schema_code):
    """ Return a list with position and class name for each  children
    given a container.

    Keyword arguments:
    container -- Container from which we get its children position.
    position -- Dictionary with position of every container of the report.
    c_activity_template -- Template for children activity.
    p_schema_code -- Schema and Code string for this container.

    """
    children_position = []
    # For every child of this container get its position and its class name
    for child_pos, child_code in position[p_schema_code].iteritems():
        c_schema_code  = child_code.lower()
        child_filename = instantiate_filename(child_level,
                                              c_activity_template,
                                              c_schema_code,
                                              p_schema_code)
        c_name = child_filename.split('/')[-1].split('.')[0]
        children_position.append({"position": child_pos, "class_name": c_name})

    return children_position


def get_init_children(environment, children_layout, children_position, a_name,
                      layout_id):
    """ Return a string with children initialized """

    # Get template name of the children layout
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,
                                 children_layout)
    template = environment.get_template(template_name)

    # Get the child_list variable
    child_list = layout_id.split('_')[-1].upper()

    # Get initialize string for listview child.
    return template.render(string_array=child_list,
                           children=children_position,
                           activity_name=a_name)


def get_expandable_attributes(environment, c_class, c_code):
    """ Return a string with expandable listView children attributes """
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,
                                 EXPANDABLE_ATTRIBUTES)
    template = environment.get_template(template_name)
    return template.render(container_class=c_class,
                           string_array=c_code)


def get_expandable_methods(environment, c_class, c_code):
    """ Return a string with expandable listView methods """
    # Set_children() : fill expandable listview with its data
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,
                                 SET_CHILDREN)
    template = environment.get_template(template_name)

    return template.render(container_class=c_class,
                           string_array=c_code)


def get_children(environment, package, activities_filenames, tree_level,
                 activity_name, position, imports, container, children_layout,
                 layout_id, parent_schema, parent_code):

    init_children = ""
    attr_children = ""
    methods_children = ""

    container_name = container.get_schema_code()

    # Get the children activity template
    c_activity_template = activities_filenames[str(tree_level + 1)]

    # Get the position for every child. Render strings and
    # activities should be at same position.
    child_tree_level = str(tree_level + 1)
    children_position = get_children_position(child_tree_level,
                                              position,
                                              c_activity_template,
                                              container_name)

    # Get initialize string for listview child.
    init_children = get_init_children(environment, children_layout,
                                      children_position,
                                      activity_name, layout_id)

    #EXPANDABLELISVIEW OPTIONS
    if(children_layout == EXPANDABLELISVIEW):
        c_code = container.get_code()
        c_class = get_class_name(container.get_schema(),
                                 c_code,
                                 parent_schema,
                                 parent_code)
        # Children methods
        methods_children = get_expandable_methods(environment,
                                                  c_class,
                                                  c_code)
        # Children attributes
        attr_children = get_expandable_attributes(environment,
                                                  c_class,
                                                  c_code)
        # Write expandableListView custom adapter
        write_listAdapter(environment, package, c_class, c_code,
                          children_position, imports)

        imports.append(Template(IMPORT_CUSTOM).
                       safe_substitute(PACKAGE=package,
                                       CLASS=c_code + '_ListAdapter'))

    imports.append(IMPORT_ARRAY)
    imports.append(IMPORT_EXPANDABLE_LISTVIEW)

    return (init_children, attr_children, methods_children)


def get_activity_filename(activities_filenames, flat, container,
                          parent_code, parent_schema):
    """ Return filename for this container. It depends on its parent """
    tree_level = container.tree_level

    # Get container class name
    container_name = container.get_schema_code()

    if (parent_code):
        parent_name = (parent_schema + '_' + parent_code)
    else:
        parent_name = None

    #Instantiate activity filename
    activity_template = activities_filenames[str(tree_level)]
    activity_filename = instantiate_filename(str(tree_level),
                                             activity_template,
                                             container_name,
                                             parent_name)
    return activity_filename


def get_activity_name(activity_filename):
    return activity_filename.split('/')[-1].split('.')[0]


def write_activity_file(environment, ontology_id, package,
                        activities_filenames, activity_filename, activity_name,
                        container, children, position, parent_schema,
                        parent_code):
    """ Write activity file for given container and its children """
    imports = []
    tree_level = container.tree_level

    # Don't overwrite activities
    if (not isfile(activity_filename)):
        activity_file = open(activity_filename, 'w')

        # This variables should store attributes for listview children
        init = ""
        attributes = ""
        methods = ""

        # Get the layout id and the activity name. It matches partially
        # with the activity filename.
        layout_id = activity_filename.split('/')[-1].split('.')[0].lower()

        # Get a list of attributes that will be shown as spinners.
        spinners = get_spinners(container.attributes)

        # Get children layout if there are childrens in this container.
        if(children):
            children_layout = get_children_settings(ontology_id,
                                                    str(tree_level))
            # If there are children, will be a listview or
            # an expandable listview to load
            init, attributes, methods = get_children(environment,
                                                     package,
                                                     activities_filenames,
                                                     tree_level, activity_name,
                                                     position, imports,
                                                     container,
                                                     children_layout,
                                                     layout_id,
                                                     parent_schema,
                                                     parent_code)

        # Write Activity Tempalte
        template_name = get_property(ACTIVITIES_TEMPLATES_SECTION,
                                     ACTIVITY)
        template = environment.get_template(template_name)

        #Write the template
        activity_file.write(template.render(imports=imports,
                                            package_name=package,
                                            activity_name=activity_name,
                                            childview=init,
                                            layout_file=layout_id,
                                            spinners=spinners,
                                            setChildren=methods,
                                            attributes=attributes))
        activity_file.close()
    else:
        print "Activity {0} already created".format(activity_filename)


def write_application(package, report_class):
    """ Write java class which extends android application. 
    I will handle shared information as the report 
    
    Returns a dictionary with the information to add to Manifest file. 
    """
    # Get the application class file. 
    output_directory = get_filepath(ACTIVITIES)
    if (not exists(output_directory)):
        makedirs(output_directory)
    application_template_filename = get_property(TEMPLATES_SECTION,
                                                 APPLICATION_FILE)
    application_filename = join(output_directory,
                                (Template(application_template_filename).
                                 safe_substitute(CLASS_NAME=report_class)))

    # Set the Environment for the jinja2 templates and get the template
    environment = set_environment(ACTIVITIES_TEMPLATES_PATH)
    template_name = get_property(ACTIVITIES_TEMPLATES_SECTION, APPLICATION)
    template = environment.get_template(template_name)

    model_package = get_property(ANDROID_PACKAGES, PACKAGE_MODEL)

    # Open and write the manifest file
    app_file = open(application_filename, 'w')
    app_file.write(template.render(package=package,
                                   model_package=model_package,
                                   report_class=report_class))
    app_file.close()
    return {'name':report_class+'_Application', 'launcher':False}
