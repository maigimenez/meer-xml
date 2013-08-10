 #  -*- coding: utf-8 -*-
from core.config import get_model_file, get_property
from core.config_variables import (CHILD_CLASS, GROUP_CLASS, GROUP_STRING,
								   MODEL_TEMPLATES_SECTION, CUSTOM_JAVA,
								   CLASS, NUM, TEXT, CODE, DATE, DATE_JAVA,
								   IMPORT_DATE, STRING_JAVA, BOOL_JAVA, INT_JAVA)
from os.path import isfile

def write_group_class (environment, template_model_file, class_name, attribute_variable, package):
	""" Write group class.

	This class is needed to handle Expandablelistview in Android. 
	It will have only two attributes: 
		- String with its  concept name. It need to be internazionalized
		- ArrayList with children.

    Keyword Arguments:
    template_model_file -- template for model filename. Handles ouptput rpath.
    class_name -- Name of the class to write. 
    """
    
	model_filename = get_model_file(template_model_file,class_name+GROUP_CLASS)
	#print "*", model_filename
	if (not isfile(model_filename)):
		model_file = open(model_filename, 'w')
		# Create a list with this class attributes and add a default group name
		attributes = [GROUP_STRING]
		# Create custom child class
		template_name = get_property(MODEL_TEMPLATES_SECTION, CUSTOM_JAVA)
		template = environment.get_template(template_name)
		render_template = template.render(custom_class=(class_name+CHILD_CLASS), custom_variable=attribute_variable)
		attributes.append(render_template)
		# Load model template
		template_name = get_property(MODEL_TEMPLATES_SECTION, CLASS)
		template = environment.get_template(template_name)
		model_file.write(template.render(package=package,
										 class_name=class_name+GROUP_CLASS,
										 attributes=attributes))
		model_file.close()
	else:
		print "Java class {0} already created".format(model_filename)


def get_attributes(environment, attributes, imports):
	# Boolean variable preventing multiple imports.
	import_date = False

	java_attributes=[]

	#Get model string for every attribute
	for attribute in attributes:
		render_template = ""
		attribute_name = attribute.concept.get_schema_code().lower().replace('-','_')
 		# BOOL ATTRIBUTE
 		if (attribute.type == NUM and attribute.is_bool()):
 		    template_name = get_property(MODEL_TEMPLATES_SECTION, BOOL_JAVA)
 		# NUM ATTRIBUTE
 		elif (attribute.type == NUM and not attribute.is_bool()):
 		    template_name = get_property(MODEL_TEMPLATES_SECTION, INT_JAVA)
 		# TEXT ATTRIBUTE
 		elif(attribute.type==TEXT or attribute.type==CODE):
 		    template_name = get_property(MODEL_TEMPLATES_SECTION, STRING_JAVA)
 		# DATE ATTRIBUTE
 		elif(attribute.type==DATE):
 		    template_name = get_property(MODEL_TEMPLATES_SECTION, DATE_JAVA)
 		    if(not import_date):
 		        import_temp_name = get_property(MODEL_TEMPLATES_SECTION,IMPORT_DATE) 
 		        template_import = environment.get_template(import_temp_name)
 		        render_import_template = template_import.render()
 		        imports.append(render_import_template)
 		        import_date = True
 		template = environment.get_template(template_name)
		render_template = template.render(name=attribute_name)
		#print render_template, attribute_name
		java_attributes.append(render_template)
	return java_attributes


def get_children(environment, children, imports, parent_class, expandables,
				 template_model_file, package):
	# Boolean variable preventing multiple imports.
	import_array = False
	attributes = []

	for child in children:
		# Create the class name 
		attribute_variable = child.value.concept.get_schema_code().lower()
		child_class_name = parent_class + '_' + attribute_variable
		child_class_name = child_class_name.replace('-','_')

		# This child has multiple items. Write a Group class. 
		if (child.value.properties.max_cardinality == -1 ):
		    write_group_class(environment, template_model_file, 
		                      child_class_name, attribute_variable, package)
		    expandables.append(child_class_name)
		    child_class_name = child_class_name + GROUP_CLASS

 		template_name = get_property(MODEL_TEMPLATES_SECTION, CUSTOM_JAVA)
		template = environment.get_template(template_name)
		render_template = template.render(custom_class=child_class_name,
		                                  custom_variable=attribute_variable)
		attributes.append(render_template)

	return attributes