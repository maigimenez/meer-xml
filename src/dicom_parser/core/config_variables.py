SETTINGS_PATH = "./settings/settings.ini"

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
XML_STRINGS_SECTION = 'XML Strings Filenames'
DEFAULT_STRINGS_SECTION = "Default Dicom"
I18N_SECTION = "i18n Dicom"
PROPERTIES_OPTION = "Properties"
# Properties
EXTENSIONS_SECTION = 'Extensions'
PROPERTIES_EXTENSION = 'Properties'

# LAYOUTS
LAYOUTS = "Layouts"
LAYOUT_FILENAME = "-Layouts"
LAYOUT_SETTINGS = "-Layouts Settings"
LEVEL_TAG = "level_"
CHILDREN_TAG = "_children" 
COLUMN_1 = "1 Column"
COLUMNS_2 = "2 Columns"
LISTVIEW = "ListView"
EXPANDABLELISVIEW = "ExpandableListView"

# This variables match with the settings.ini
# TEMPLATE_TYPES
TEMPLATE_PACKAGE = 'templates'
TEMPLATES_SECTION = 'Templates'
TEMPLATES_ROOT_PATH = 'Templates Path'

STRING_TEMPLATES_SECTION = 'String Templates'
STRING_TEMPLATES_PATH = 'String Templates Path'

LAYOUT_TEMPLATES_SECTION = 'Layout Templates'
LAYOUT_TEMPLATES_PATH = 'Layout Templates Path'

# STRING TEMPLATES
DEFAULT_STRINGS = 'default_strings'
LEVEL_STRINGS = 'level_strings'
CHILDREN_ARRAYS = 'children_arrays'
DICOM_LEVEL = 'dicom_level'
STRING_TEMPLATES = [DEFAULT_STRINGS, LEVEL_STRINGS, CHILDREN_ARRAYS,
                    DICOM_LEVEL]
#The options for these properties section replace a unique template value
MULTIPLE_PROPERTIES = {LEVEL_STRINGS: ('level_code', 'level_meaning'),
                       CHILDREN_ARRAYS: ('nodes', 'parent_code', 'children'),
                       DICOM_LEVEL: ('levels', 'attributes', 'level_num',
                                     'level_name', 'code', 'meaning')}
#These templates are filled based on the report ID
TEMPLATE_BY_ID = [LEVEL_STRINGS]
#These templates are filled based on data from the report
TEMPLATE_BY_REPORT = [CHILDREN_ARRAYS, DICOM_LEVEL]

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
SCROLL = 'scroll'
# LAYOUT
TWO_COLUMNS_ONE_LEVEL ='2 Columns 1 Level'
TWO_COLUMNS_TWO_LEVELS = '2 Columns 2 Levels'
LAYOUT_TEMPLATES = [END, HEADER, MAIN_LEFT, RIGHT, NEXT_LEVEL, GENERIC_TITLE,
                    NUM, DATE, TEXT, SCROLL, TWO_COLUMNS_ONE_LEVEL,
                    TWO_COLUMNS_TWO_LEVELS]

# XML FILETYPES
STRINGS = 'Strings'
