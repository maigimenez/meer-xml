
""" XML files """
STRINGS_XML = "strings.xml"


"""Localization strings. 
Replace template strings using a dictionary. 
Check internalization standard (and more complex) methods to improve this

"""
english = {"ADD":"Add",
           "FINISH":"Finish",
           "VALIDATE":"Validate",
           "CHANGE":"Change"}

english = {"ADD":"Add",
           "FINISH":"Finish",
           "VALIDATE":"Validate",
           "CHANGE":"Change"}


""" Layout strings and templates """
TAB_MARGIN = "20dp"
BLOCK_MARGIN_BOTTOM = "10dp"

DEFAULT_STRINGS = "\n\t<!-- Default buttons -->\n" \
"\t<string name=\"add\">${ADD}</string>\n"\
"\t<string name=\"finish\">${FINISH}</string>\n"\
"\t<string name=\"validate\">${VALIDATE}</string>\n"\
"\t<string name=\"change\">${CHANGE}</string>\n"

DATE_LAYOUT = "<TextView android:id=\"@+id/${CONCEPT_VALUE}_label\"\n"\
"\tandroid:text=\"@string/${CONCEPT_NAME}\"\n"\
"\tandroid:layout_width=\"wrap_content\"\n"\
"\tandroid:layout_height=\"wrap_content\"\n"\
"\tandroid:layout_marginLeft=\"20dp\"\n"\
"\tandroid:layout_below=\"@id/${ID_PREVIOUS_ITEM}\"\n />\n"\
"\n"\
"<Button android:id=\"@+id/${CONCEPT_VALUE}_button\"\n"\
"\tandroid:text=\"@string/change\"\n"\
"\tandroid:layout_width=\"wrap_content\" \n"\
"\tandroid:layout_height=\"wrap_content\"\n"\
"\tandroid:layout_below=\"@id/${ID_PREVIOUS_ITEM}\"\n"\
"\tandroid:layout_alignParentRight=\"true\"\n "\
"\tandroid:layout_alignBaseline=\"@+id/${CONCEPT_VALUE}_text\"/>\n"\
"\n"\
"<EditText android:id=\"@id/${CONCEPT_VALUE}_text\"\n"\
"\tandroid:text=\"\"\n "\
"\tandroid:hint=\"@string/${CONCEPT_NAME}\"\n"\
"\tandroid:layout_width=\"match_parent\"\n"\
"\tandroid:layout_height=\"wrap_content\"\n"\
"\tandroid:layout_below=\"@id/${CONCEPT_VALUe}_label\"\n"\
"\tandroid:layout_toLeftOf=\"@id/${CONCEPT_VALUE}_button\"\n "\
"\tandroid:layout_marginBottom=\"10dp\"\n"\
"\tandroid:layout_marginLeft=\"20dp\"\n "\
"\tandroid:inputType=\"date\" />"
