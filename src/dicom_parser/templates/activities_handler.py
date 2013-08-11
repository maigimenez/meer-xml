from os.path import join, exists
from os import makedirs
from core.config_variables import (MANIFEST, ACTIVITIES_TEMPLATES_PATH,
								   ACTIVITIES_TEMPLATES_SECTION,CODE)
from core.config import set_environment, get_property,get_filepath

def write_manifest(package_name, activities, launcher_activity):
	# Get the AndroidManifest
	output_directory = get_filepath(MANIFEST)
	if (not exists(output_directory)):
		makedirs(output_directory)
	manifest_filename = get_property(ACTIVITIES_TEMPLATES_SECTION,MANIFEST)
	manifest_path = join(output_directory,manifest_filename)

	# Set the Environment for the jinja2 templates and get the template
	environment = set_environment(ACTIVITIES_TEMPLATES_PATH)
	template_name = get_property(ACTIVITIES_TEMPLATES_SECTION, MANIFEST)
	template = environment.get_template(template_name)

	# Open and write the manifest file
	manifest_file = open(manifest_path,'w')
	manifest_file.write(template.render(package_name=package_name, activities=activities))
	manifest_file.close()

def get_spinners(attributes):
	spinners = []
	for attribute in attributes:
		if attribute.type == CODE:
			spinners.append(attribute.concept.code)
	return spinners