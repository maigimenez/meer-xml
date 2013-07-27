import sys
import parser.handler as parser
import templates.handler as template_engine
from core.files import AndroidFiles


#read_config()
LANGUAGE_CODE = sys.argv[2]

# OUTPUT STRINGS
#Set which files are going to be used as output for the parser
xml_filenames = AndroidFiles()
xml_filenames.set_languages(LANGUAGE_CODE)

# PARSE
report = parser.DicomParser().parse(sys.argv[1])
#report.imprime()
#print
#print
report.report.depthFirst()

# OUTPUT LAYOUTS
# Write the file names of the layouts and
# the activities based on the report ontology
#xml_filenames.set_odontology(report.get_odontology())

#WRITE STRINGS XML
#template_engine.write_strings(LANGUAGE_CODE, report)

#WRITE LAYOUTS
#template_engine.write_layouts(xml_filenames.layouts, report, LANGUAGE_CODE)

# WRITE JAVA MODEL
#template_engine.write_model(xml_filenames.model, report, LANGUAGE_CODE)

# WRITE ANDROID ACTIVITIES
#template_engine.write_activities(xml_filenames.activities, report)
