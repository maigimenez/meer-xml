# -*- coding: utf-8 -*-

""" Layout strings and templates """

""" General layouts and varibles """
TAB_MARGIN = "20dp"
BLOCK_MARGIN_BOTTOM = "10dp"

DEFAULT_STRINGS_TEMPLATE = "\n\t<!-- Default buttons -->\n" \
"\t<string name=\"add\">${ADD}</string>\n"\
"\t<string name=\"finish\">${FINISH}</string>\n"\
"\t<string name=\"validate\">${VALIDATE}</string>\n"\
"\t<string name=\"change\">${CHANGE}</string>\n"\
"\t<string name=\"next_level\">${NEXT_LEVEL}</string>\n"

HEADER_LAYOUT = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"\
"<RelativeLayout xmlns:tools=\"http://schemas.android.com/tools\"\n"\
"\txmlns:android=\"http://schemas.android.com/apk/res/android\"\n"\
"\tandroid:layout_width=\"match_parent\" android:layout_height=\"match_parent\">\n"\
"\n"\
"\t<!-- HEADER -->\n"\
"\t<include android:id=\"@+id/top_header\"\n"\
"\t\tandroid:layout_alignParentTop=\"true\" layout=\"@layout/layout_header\" />\n"\
"\n"\
"\t<!-- FOOTER -->\n"\
"\t<LinearLayout android:id=\"@+id/bottom_menu\"\n"\
"\t\tandroid:layout_width=\"fill_parent\" android:layout_height=\"wrap_content\"\n"\
"\t\tandroid:orientation=\"horizontal\" android:layout_alignParentBottom=\"true\">\n"\
"\t\t<!-- menu bar -->\n"\
"\t\t<include layout=\"@layout/layout_footer_menu\" />\n"\
"\t</LinearLayout>\n"\
"\n"

MAIN_LEFT_LAYOUT="\t<!-- MAIN PART: split layout -->\n"\
"\t<LinearLayout android:orientation=\"horizontal\"\n"\
"\t\tandroid:layout_width=\"fill_parent\" android:layout_height=\"fill_parent\"\n"\
"\t\tandroid:layout_below=\"@id/top_header\" android:layout_above=\"@id/bottom_menu\"\n"\
"\t\tandroid:id=\"@+id/sub_content_view\"\n"\
"\t\tandroid:paddingBottom=\"5sp\" android:background=\"@color/lightGrey\"\n"\
"\t\tandroid:baselineAligned=\"false\">\n"\
"\n"\
"\t\t<!-- Left layout -->\n"\
"\t\t<RelativeLayout android:id=\"@+id/left_layout\"\n"\
"\t\t\tandroid:layout_width=\"match_parent\" android:layout_height=\"wrap_content\"\n"\
"\t\t\tandroid:layout_weight=\"1\" android:background=\"#eeeeee\"\n"\
"\t\t\tandroid:layout_margin=\"20dp\" android:paddingBottom=\"20dp\"\n"\
"\t\t\tandroid:paddingTop=\"25dp\" android:paddingLeft=\"25dp\"\n"\
"\t\t\tandroid:paddingRight=\"25dp\">\n"\
"\n"

RIGHT_LAYOUT = "\t\t</RelativeLayout>\n"\
"\n"\
"\t\t<!-- Right layout -->\n"\
"\t\t<RelativeLayout android:id=\"@+id/right_layout\"\n"\
"\t\t\tandroid:layout_width=\"match_parent\" android:layout_height=\"wrap_content\"\n"\
"\t\t\tandroid:layout_weight=\"1\" android:background=\"#eeeeee\"\n"\
"\t\t\tandroid:layout_margin=\"20dp\" android:paddingBottom=\"20dp\"\n"\
"\t\t\tandroid:paddingTop=\"25dp\" android:paddingLeft=\"25dp\"\n"\
"\t\t\tandroid:paddingRight=\"25dp\">\n"
			
NEXT_LEVEL_LAYOUT = "\n\t\t\t<ListView android:id=\"@+id/children${LEVEL}_list\"\n"\
"\t\t\t\tandroid:layout_width=\"match_parent\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/level_${LEVEL}_label\" >\n"\
"\t\t\t</ListView>\n"		

MAIN_LAYOUT="\t<!-- MAIN PART: split layout -->\n"\
"\t<LinearLayout android:orientation=\"horizontal\"\n"\
"\t\tandroid:layout_width=\"fill_parent\" android:layout_height=\"fill_parent\"\n"\
"\t\tandroid:layout_below=\"@id/top_header\" android:layout_above=\"@id/bottom_menu\"\n"\
"\t\tandroid:id=\"@+id/sub_content_view\"\n"\
"\t\tandroid:paddingBottom=\"5sp\" android:background=\"@color/lightGrey\"\n"\
"\t\tandroid:baselineAligned=\"false\">\n"\
"\n"\
"\t\t<!-- Left layout -->\n"\
"\t\t<RelativeLayout android:id=\"@+id/main_layout\"\n"\
"\t\t\tandroid:layout_width=\"match_parent\" android:layout_height=\"wrap_content\"\n"\
"\t\t\tandroid:layout_weight=\"1\" android:background=\"#eeeeee\"\n"\
"\t\t\tandroid:layout_margin=\"20dp\" android:paddingBottom=\"20dp\"\n"\
"\t\t\tandroid:paddingTop=\"25dp\" android:paddingLeft=\"25dp\"\n"\
"\t\t\tandroid:paddingRight=\"25dp\">\n"\
"\n"

"""
This next level layout contains space for a button, since we are listing all the children level
it could be confusing for the user.

NEXT_LEVEL_LAYOUT = "<TextView android:id=\"@+id/injuriesSum_label\"\n"\
"android:layout_width=\"wrap_content\"\n"\
"android:layout_height=\"wrap_content\"\n"\
"android:text=\"@string/in_title\"\n"\
"android:textAppearance=\"@android:style/TextAppearance.Large\"\n"\
"android:layout_marginBottom=\"20dp\"\n"\
"android:textColor=\"@color/black\"/>\n"\
"<LinearLayout android:id=\"@+id/injuriesButtons_layout\"\n"\
"android:layout_height=\"wrap_content\"\n"\
"android:layout_width=\"wrap_content\"\n"\
"android:layout_alignParentBottom=\"true\"\n"\
"android:layout_alignRight=\"@+id/injuries_list\"\n"\
"android:gravity=\"right|bottom\">\n"\
"\n"\
"<Button android:id=\"@+id/addInjuries_button\"\n"\
"android:layout_width=\"wrap_content\"\n"\
"android:layout_height=\"wrap_content\" android:text=\"@string/add\" />\n"\
"</LinearLayout>\n"\
"<ListView\n"\
"android:id=\"@+id/injuries_list\"\n"\
"android:layout_width=\"match_parent\"\n"\
"android:layout_height=\"wrap_content\"\n"\
"android:layout_above=\"@id/injuriesButtons_layout\"\n"\
"android:layout_below=\"@id/injuriesSum_label\" >\n"\
"</ListView>\n"		
"""

END_LAYOUT="\t\t</RelativeLayout>\n"\
"\t</LinearLayout>\n"\
"</RelativeLayout>\n"\


""" Data type layouts """
#TODO: find a better way to handle the tabs
DATE_LAYOUT = "\n\t\t\t<!-- Date: ${CONCEPT_NAME} -->\n" \
"\t\t\t<TextView android:id=\"@+id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:text=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/${PREVIOUS_ITEM}\"/>\n"\
"\n"\
"\t\t\t<Button android:id=\"@+id/button_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:text=\"@string/change\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\" \n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_alignParentRight=\"true\"\n "\
"\t\t\t\tandroid:layout_alignBaseline=\"@+id/etext_${CONCEPT_VALUE}\"/>\n"\
"\n"\
"\t\t\t<EditText android:id=\"@id/etext_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:text=\"\"\n "\
"\t\t\t\tandroid:hint=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"match_parent\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_toLeftOf=\"@id/button_${CONCEPT_VALUE}\"\n "\
"\t\t\t\tandroid:layout_marginBottom=\"10dp\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\"\n "\
"\t\t\t\tandroid:inputType=\"date\" />\n"

""" 
Right now num and text are being handle equally 
TODO: Improve this template!

"""
NUM_LAYOUT = "\n\t\t\t<!-- Num: ${CONCEPT_NAME} -->\n" \
"\t\t\t<TextView android:id=\"@+id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/${PREVIOUS_ITEM}\"\n"\
"\t\t\t\tandroid:text=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\" />\n"\
"\n"\
"\t\t\t<EditText android:id=\"@+id/etext_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"fill_parent\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:hint=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:text=\"\"\n"\
"\t\t\t\tandroid:layout_marginBottom=\"10dp\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\" /> \n"\

TEXT_LAYOUT = "\n\t\t\t<!-- Text: ${CONCEPT_NAME} -->\n" \
"\t\t\t<TextView android:id=\"@+id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/${PREVIOUS_ITEM}\"\n"\
"\t\t\t\tandroid:text=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\" />\n"\
"\n"\
"\t\t\t<EditText android:id=\"@+id/etext_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:layout_width=\"fill_parent\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_below=\"@id/label_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:hint=\"@string/code_${CONCEPT_VALUE}\"\n"\
"\t\t\t\tandroid:text=\"\"\n"
"\t\t\t\tandroid:layout_marginBottom=\"10dp\"\n"\
"\t\t\t\tandroid:layout_marginLeft=\"20dp\" /> \n"\

GENERIC_TITLE_LAYOUT = "\n\t\t\t <TextView android:id=\"@+id/level_${LEVEL}_label\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_alignParentLeft=\"true\"\n"\
"\t\t\t\tandroid:layout_alignParentTop=\"true\"\n"\
"\t\t\t\tandroid:layout_marginBottom=\"20dp\"\n"\
"\t\t\t\tandroid:text=\"@string/level_${LEVEL}\"\n"\
"\t\t\t\tandroid:textAppearance=\"@android:style/TextAppearance.Large\" />\n"

TITLE_LAYOUT = "\n\t\t\t <TextView android:id=\"@+id/level_${LEVEL}_label\"\n"\
"\t\t\t\tandroid:layout_width=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_height=\"wrap_content\"\n"\
"\t\t\t\tandroid:layout_alignParentLeft=\"true\"\n"\
"\t\t\t\tandroid:layout_alignParentTop=\"true\"\n"\
"\t\t\t\tandroid:layout_marginBottom=\"20dp\"\n"\
"\t\t\t\tandroid:text=\"@string/code_${LEVEL}\"\n"\
"\t\t\t\tandroid:textAppearance=\"@android:style/TextAppearance.Large\" />\n"

""" JAVA CLASSES TEMPLATES """
SETTINGS_JAVA ="package com.i3m.meerAndroid.model\;\n"\
"public class settings {"

STRING_ARRAY = 	"private static String[] values_{CODE_MEANING}  = \{${VALUES}\};" 

END_CLASS ="}"

