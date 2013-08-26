SETTINGS_PATH = './settings/settings.ini'
USER_SETTINGS_PATH = 'User Settings'

# ONTOLOGIES SETTINGS
ONTOLOGIES_SETTINGS = 'Ontologies Settings'
ONTOLOGIES_PATH = 'Settings Path'
ONTOLOGY_FILENAMES= "Filenames"
LAYOUT_SETTINGS = "Layouts Settings"

# SCRIPT INPUT
I18N_INPUT = 'i18n'
DEFAULT_INPUT = 'default'

# LANGUAGES
# List of languages used. It's set with the second script parameter.
I18N = ["es_ES", "en_GB"]
DEFAULT = ["en_GB"]

# CONFIG SECTIONS AND OPTIONS
OUTPUT_DIRECTORIES_SECTION = 'Output Directories'
STRINGS_OUTPUT_OPTION = 'Strings'
MODEL_OUTOUT_OPTION = 'Model'
XML_STRINGS_SECTION = 'XML Strings Filenames'
DEFAULT_STRINGS_SECTION = "Default Dicom"
I18N_SECTION = "i18n Dicom"
PROPERTIES_OPTION = "Properties"
# Properties
EXTENSIONS_SECTION = 'Extensions'
PROPERTIES_EXTENSION = 'Properties'
XML_EXTENSION = 'Xml'
JAVA_EXTENSION = 'Java'
SETTINGS_EXTENSION = 'Settings'

# LAYOUTS
LAYOUTS = "Layouts"
LAYOUT_FILENAME = "-Layouts"
LEVEL_TAG = "level_"
CHILDREN_TAG = "_children" 
COLUMN_1 = "1 Column"
COLUMNS_2 = "2 Columns"

#ACTIVITIES
ACTIVITIES="Activities"
ACTIVITY = 'Activity'

# This variables match with the settings.ini
# TEMPLATE_TYPES
TEMPLATE_PACKAGE = 'templates'
TEMPLATES_SECTION = 'Templates'
TEMPLATES_ROOT_PATH = 'Templates Path'

STRING_TEMPLATES_SECTION = 'String Templates'
STRING_TEMPLATES_PATH = 'String Templates Path'
PATIENT_ID = 'RADLEX-RID13159'

LAYOUT_TEMPLATES_SECTION = 'Layout Templates'
LAYOUT_TEMPLATES_PATH = 'Layout Templates Path'

MODEL_TEMPLATES_PATH = 'Model Templates Path'
MODEL_TEMPLATES_SECTION = 'Model Templates'
MODEL_FILE = 'Model File'

ACTIVITIES_TEMPLATES_PATH = 'Activity Templates Path'
ACTIVITIES_TEMPLATES_SECTION = 'Activity Templates'

# STRING TEMPLATES
DEFAULT_STRINGS = 'default_strings'
LEVEL_STRINGS = 'level_strings'
CHILDREN_ARRAYS = 'children_arrays'
DICOM_LEVEL = 'dicom_level'
#It is the same template as CHILDREN_ARRAYS, but filled with different data.
CODE_ARRAYS = 'code_arrays'
STRING_TEMPLATES = [DEFAULT_STRINGS, LEVEL_STRINGS, CHILDREN_ARRAYS,
                    DICOM_LEVEL, CODE_ARRAYS]
#The options for these properties section replace a unique template value
MULTIPLE_PROPERTIES = {LEVEL_STRINGS: ('level_code', 'level_meaning'),
                       CHILDREN_ARRAYS: ('nodes', 'parent_code', 'children'),
                       CODE_ARRAYS: ('nodes', 'parent_code', 'children'),
                       DICOM_LEVEL: ('levels', 'attributes', 'level_num',
                                     'level_name', 'code', 'meaning')}
#These templates are filled based on the report ID
TEMPLATE_BY_ID = [LEVEL_STRINGS]
#These templates are filled based on data from the report
TEMPLATE_BY_REPORT = [CHILDREN_ARRAYS, DICOM_LEVEL, CODE_ARRAYS]

# LAYOUT TEMPLATES
END = 'End'
HEADER = 'Header'
MAIN_LEFT = 'Main and Left'
NEXT_LEVEL = 'Next level'
RIGHT = 'Right'
GENERIC_TITLE = 'Generic title'
TREE_TITLE = 'Tree title'
NUM = 'num'
BOOL = 'bool'
DATE = 'date'
TEXT = 'text'
CODE = 'code'
SCROLL = 'scroll'
LISTVIEW = 'ListView'
EXPANDABLELISVIEW = "Expandable ListView"
ATTRIBUTES = 'Attributes'
# LAYOUT
ONE_COLUMN = '1 Column'
TWO_COLUMNS ='2 Columns'
LAYOUT_TEMPLATES = [END, HEADER, MAIN_LEFT, RIGHT, NEXT_LEVEL, GENERIC_TITLE,
                    NUM, DATE, TEXT, SCROLL, ONE_COLUMN, CODE,
                    TWO_COLUMNS, EXPANDABLELISVIEW, LISTVIEW]

# JAVA TEMPLATES
CLASS = 'Class'
BOOL_JAVA = 'Boolean'
INT_JAVA = 'Integer'
STRING_JAVA = 'String'
DATE_JAVA = 'Date'
CUSTOM_JAVA = 'Custom'
CUSTOM_ARRAY = 'Custom Array'
IMPORT_ARRAY = 'Import Array'
CHILD_CLASS = '_Child'
CHILD_STRING = 'String instance;'
GROUP_CLASS = '_Group'
GROUP_STRING = '\tString group_name;'
# XML FILETYPES
STRINGS = 'Strings'

#ANDROID
ANDROID_PACKAGES = 'Android Packages'
PACKAGE_MODEL = 'Model'
BASE_MODEL = 'Base'
IMPORT_DATE = 'Import Date'
MANIFEST = 'Manifest'

