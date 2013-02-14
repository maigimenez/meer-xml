# -*- coding: utf-8 -*-

""" XML files """
STRINGS_XML = "strings.xml"
LEVEL_1_LAYOUT = "summary.xml"

EXPLORATION_OF_BREAST = {1:"summary.xml",
                         2:"tree.xml",
                         3:"edit_node.xml"}

MAMOGRAPHY = {1:"summary.xml",
              2:"tree.xml",
              3:"edit_node.xml"}

LAYOUTS_DICTIONARY = {4:EXPLORATION_OF_BREAST,
                      5:MAMOGRAPHY}

I18N_MATCH = {1:"es",
              2:"en"}

DEFAULT_MATCH = {1:"en"}

LANGUAGE_DICTIONARY = {"default":DEFAULT_MATCH,
                      "i18n":I18N_MATCH}

DEFAULT_STRINGS = {"en":"strings.xml"}

I18N_STRINGS = {"en":"strings.xml",
                "es":"strings_ES.xml"}

STRINGS_DICTIONARY = {"default":DEFAULT_STRINGS,
                      "i18n":I18N_STRINGS}

        
"""Localization strings. 
Replace template strings using a dictionary. 
Check internalization standard (and more complex) methods to improve this

"""
english = {"ADD":"Add",
           "FINISH":"Finish",
           "VALIDATE":"Validate",
           "CHANGE":"Change"}

spanish = {"ADD":"Añadir",
           "FINISH":"Terminar",
           "VALIDATE":"Validar",
           "CHANGE":"Cambiar"}


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


HEADER_LAYOUT = "<?xml version="1.0" encoding="UTF-8"?>\n"\
"<RelativeLayout xmlns:tools=\"http://schemas.android.com/tools\"\n"\
"\txmlns:android=\"http://schemas.android.com/apk/res/android\"\n"\
"\tandroid:layout_width=\"match_parent\" android:layout_height=\"match_parent\">\n"\
"\t<!-- HEADER -->\n"\
"\t<include android:id=\"@+id/top_header\"\n"\
"\t\tandroid:layout_alignParentTop=\"true\" layout=\"@layout/layout_header\" />\n"\
"\t<!-- FOOTER -->\n"
"\t<LinearLayout android:id=\"@+id/bottom_menu\"\n"\
"\t\tandroid:layout_width=\"fill_parent\" android:layout_height=\"wrap_content\"\n"\
"\t\tandroid:orientation=\"horizontal\" android:layout_alignParentBottom=\"true\">\n"\
"\t\t<!-- menu bar -->\n"\
"\t\t<include layout=\"@layout/layout_footer_menu\" />\n"\
"\t</LinearLayout>\n"\
"\t<!-- MAIN PART: split layout -->\n"\
"\t<LinearLayout android:orientation=\"horizontal\"\n"\
"\tandroid:layout_width=\"fill_parent\" android:layout_height=\"fill_parent\"\n"\
"\tandroid:layout_below=\"@id/top_header\" android:layout_above=\"@id/bottom_menu\"\n"\
"\tandroid:id=\"@+id/sub_content_view\"\n"\
"\tandroid:paddingBottom=\"5sp\" android:background=\"@color/lightGrey\"\n"\
"\tandroid:baselineAligned=\"false\">\n"\
"\n"\       	
"\t<!-- Left layout -->\n"\
"\t<RelativeLayout android:id=\"@+id/left_layout\"\n"\
"\tandroid:layout_width=\"match_parent\" android:layout_height=\"wrap_content\"\n"\
"\tandroid:layout_weight=\"1\" android:background=\"#eeeeee\"\n"\
"\tandroid:layout_margin=\"20dp\" android:paddingBottom=\"20dp\"\n"\
"\tandroid:paddingTop=\"25dp\" android:paddingLeft=\"25dp\"\n"
"\tandroid:paddingRight=\"25dp\">\n"\
"\n"
