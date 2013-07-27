 #  -*- coding: utf-8 -*-
from core.config import get_model_file, get_property
from core.config_variables import (CHILD_CLASS, GROUP_CLASS, GROUP_STRING,
								   MODEL_TEMPLATES_SECTION, CUSTOM_JAVA,
								   CLASS)
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
	print "*", model_filename
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
