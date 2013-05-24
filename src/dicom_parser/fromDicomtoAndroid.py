import parser.handler as parser
import templates.handler as template_engine
from core.files import AndroidFiles
import sys
from core.config_variables import *

#read_config()
LANGUAGE_CODE = sys.argv[2]

#Set which files are going to be used as output for the parser
#Strings
xml_filenames = AndroidFiles()
xml_filenames.set_languages(LANGUAGE_CODE)

# PARSE  
#While parsing, the strings file is written.
report = parser.DicomParser().parse(sys.argv[1])
report.imprime()
template_engine.write_strings(LANGUAGE_CODE,report)
# Write the filenames of the layouts and the activities based on the report odontology
xml_filenames.set_odontology(report.get_odontology())

#WRITE STRINGS XML
#Default strings: template_type = Strings
#template_engine.write_template(DEFAULT_STRINGS,LANGUAGE_CODE)
#template_engine.write_template(LEVEL_STRINGS,LANGUAGE_CODE,report)
#template_engine.write_template(CHILDREN_ARRAYS,LANGUAGE_CODE,report)
#template_engine.close_resources(LANGUAGE_CODE)

#deepest_level = report.get_deepest_level()
#WRITE LAYOUTS
#template_engine.write_layouts(xml_filenames.layouts,report,LANGUAGE_CODE)
#dicom_xml.close()
