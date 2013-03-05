# -*- coding: utf-8 -*-

""" Layouts """
#level: (filename,number of columns)
EXPLORATION_OF_BREAST = {1:("summary.xml",2),
                         2:("tree_${CODE}.xml",1),
                         3:("edit_node_${CODE}.xml",2)}

MAMOGRAPHY = {1:("summary.xml",1),
              2:("tree_${CODE}.xml",1),
              3:("edit_node_${CODE}.xml",2)}

LAYOUTS_DICTIONARY = {4:EXPLORATION_OF_BREAST,
                      5:MAMOGRAPHY}


""" Activities """
EXPLORATION_OF_BREAST_ACTIVITIES = {1:"SummaryActivity.xml",
                                    2:"TreeActivity.xml",
                                    3:"Edit_NodeActivity.xml"}

MAMOGRAPHY_ACTIVITIES = {1:"SummaryActivity.xml",
                         2:"TreeActivity.xml",
                         3:"Edit_NodeActivity.xml"}

ACTIVITIES_DICTIONARY = {4:EXPLORATION_OF_BREAST_ACTIVITIES,
                         5:MAMOGRAPHY_ACTIVITIES}


""" Models """
SETTINGS_CLASS = "settings.java"

""" Internacionalization/Strings """
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

