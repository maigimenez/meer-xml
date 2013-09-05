 #  -*- coding: utf-8 -*-
from core.config import get_model_file, get_property
from core.config_variables import (CHILD_CLASS, GROUP_CLASS, GROUP_STRING,
								   MODEL_TEMPLATES_SECTION, CUSTOM_JAVA,
								   CLASS, NUM, TEXT, CODE, DATE,
								   CUSTOM_ARRAY, INTERFACE_IDENTIFIER,
								   INTERFACE_CLASS, GETTERS_SETTERS,
								   TYPE_JAVA)
from core.java_types import (ARRAY, BOOL, DATE, INT, STRING, IMPORT_DATE,
                             IMPORT_ARRAY)
from os.path import isfile
from string import Template

def write_group_class (environment, template_model_file, class_name, attribute_variable, package):
	""" Write group class

	This class is needed to handle Expandablelistview in Android. 
	It will have only two attributes: 
		- String with its  concept name. It need to be internazionalized
		- ArrayList with children.

    Keyword Arguments:
    template_model_file -- template for model filename. Handles ouptput rpath.
    class_name -- Name of the class to write. 
    """
    # Import Arraylist. It's always needed with a group class
	imports =[]
	imports.append(IMPORT_ARRAY)

	#Load template to instantiate getters and setters
	getters_setters_template_name = get_property(MODEL_TEMPLATES_SECTION, GETTERS_SETTERS)
	getters_setters_template = environment.get_template(getters_setters_template_name)


	model_filename = get_model_file(template_model_file,class_name+GROUP_CLASS)
	if (not isfile(model_filename)):
		model_file = open(model_filename, 'w')
		# Create a list with this class attributes and add a default group name
		attributes = [GROUP_STRING]
		methods = [getters_setters_template.render(type="type",
												   variable_type=STRING)]
		# Create custom child class
		template_name = get_property(MODEL_TEMPLATES_SECTION, TYPE_JAVA)
		template = environment.get_template(template_name)
		type_name = Template(ARRAY).safe_substitute(CLASS=class_name+CHILD_CLASS)

		array = template.render(type=(type_name), variable="children")
		attributes.append(array)
		methods.append( getters_setters_template.render(type="children",
														variable_type=type_name))
		# Load model template and write the class
		template_name = get_property(MODEL_TEMPLATES_SECTION, CLASS)
		template = environment.get_template(template_name)
		model_file.write(template.render(package=package,
										 imports=imports,
										 class_name=class_name+GROUP_CLASS,
										 attributes=attributes,
										 methods=methods))
		#TODO: Getters & setters
		model_file.close()
	else:
		print "Java class {0} already created".format(model_filename)

def write_children_interface (environment, template_model_file, class_name, package):
	""" Write interface children class

	This class is needed to handle Expandablelistview in Android. 
	It will have only one attribute: a string with its identifier.

    Keyword Arguments:
    template_model_file -- template for model filename. Handles ouptput rpath.
    class_name -- Name of the class to write. 
    """
	model_filename = get_model_file(template_model_file,class_name+CHILD_CLASS)
	#print "*", model_filename
	if (not isfile(model_filename)):
		model_file = open(model_filename, 'w')
		# Create a list with this class attributes and add a default get Id 
		attributes = [INTERFACE_IDENTIFIER]
		# Load model template and write the class
		template_name = get_property(MODEL_TEMPLATES_SECTION, INTERFACE_CLASS)
		template = environment.get_template(template_name)
		model_file.write(template.render(package=package,
										 class_name=class_name+CHILD_CLASS,
										 attributes=attributes))
		model_file.close()
	else:
		print "Java class {0} already created".format(model_filename)


def get_attributes(environment, attributes, imports):
	# Boolean variable preventing multiple imports.
	import_date = False

	java_attributes=[]
	java_getters_setters = []

	#Get model string for every attribute
	for attribute in attributes:
		render_template = ""
		attribute_name = attribute.concept.get_schema_code().lower().replace('-','_')

		#Load template writte the attributes
		template_name = get_property(MODEL_TEMPLATES_SECTION, TYPE_JAVA)
		template = environment.get_template(template_name)

		#Load template to instantiate getters and setters
		getters_setters_template_name = get_property(MODEL_TEMPLATES_SECTION, GETTERS_SETTERS)
		getters_setters_template = environment.get_template(getters_setters_template_name)

 		# BOOL ATTRIBUTE
 		if (attribute.type == NUM and attribute.is_bool()):
			java_attributes.append(template.render(type=BOOL, 
												   variable=attribute_name))
			java_getters_setters.append( getters_setters_template.render(
												type=attribute_name,
												variable_type=BOOL))
 		# NUM ATTRIBUTE
 		elif (attribute.type == NUM and not attribute.is_bool()):
			java_attributes.append(template.render(type=INT, 
													variable=attribute_name))
			java_getters_setters.append( getters_setters_template.render(
 										type=attribute_name,
 										variable_type=INT))
 		# TEXT ATTRIBUTE
 		elif(attribute.type==TEXT or attribute.type==CODE):
			java_attributes.append(template.render(type=STRING, 
													variable=attribute_name))
			java_getters_setters.append( getters_setters_template.render(
											type=attribute_name,
											variable_type=STRING))
		# DATE ATTRIBUTE
		elif(attribute.type==DATE):
			java_attributes.append(template.render(type=DATE, 
													variable=attribute_name))
			java_getters_setters.append( getters_setters_template.render(
											type=attribute_name,
											variable_type=DATE))
			if(not import_date):
				imports.append(IMPORT_DATE)
				import_date = True
		

	return java_attributes, java_getters_setters


def get_children(environment, children, imports, parent_class, 
				 parent_class_name, expandables, template_model_file,
				 package):
	# Boolean variable preventing multiple imports.
	import_array = False
	#Boolean variable set true if we need to handle Expandable Children
	# If at least one of the children has multiple items all of them
	# will be inside an expandablelist.
	has_expandable = False
	# Find out if you need an ExpandableList
	for child in children:
		if (child.value.properties.max_cardinality == -1 ):
			has_expandable = True
			break
	
	attribute_variable = parent_class_name.lower()
	if (has_expandable):
		write_group_class(environment, template_model_file, parent_class_name,
						  attribute_variable, package)
		write_children_interface(environment, template_model_file,
								 parent_class_name, package)

	#Load template to instantiate getters and setters
	getters_setters_template_name = get_property(MODEL_TEMPLATES_SECTION, GETTERS_SETTERS)
	getters_setters_template = environment.get_template(getters_setters_template_name)

	attributes = []
	methods = []

	#print
	#print "********** Get children ****************"
	for child in children:
		# Create the class name 
		attribute_variable = child.value.concept.get_schema_code().lower()
		child_class_name = parent_class + '_' + attribute_variable
		child_class_name = child_class_name.replace('-','_')

		# This child has multiple items. Write a Group class. 
		if (has_expandable):
			expandables.append(child_class_name)

		# Load template for java types
		template_name = get_property(MODEL_TEMPLATES_SECTION, TYPE_JAVA)
		template = environment.get_template(template_name)

		render_template = ""
		#Children with multiple items.
		if (child.value.properties.max_cardinality == -1 ):
			type_name = Template(ARRAY).safe_substitute(CLASS=child_class_name)
			render_template = template.render(type=type_name,
		     	                              variable=attribute_variable)
			methods.append( getters_setters_template.render( 
										type=attribute_variable,
 										variable_type=type_name))
			if(not import_array):
				imports.append(IMPORT_ARRAY)
				import_array = True
		
		else:
			render_template = template.render(type=child_class_name,
			                                  variable=attribute_variable)
			methods.append( getters_setters_template.render( 
										type=attribute_variable,
 										variable_type=child_class_name))

		attributes.append(render_template)

	# if (write_group):
	# 	write_group_class(environment, template_model_file, child_class_name, attribute_variable, package)
		#write_children_interface(environment,template_model_file,parent_class,package)
	#print "********** END Get children ****************"
	#print
	return attributes,methods