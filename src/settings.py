# -*- coding: utf-8 -*-

""" XML files """
STRINGS_XML = "strings.xml"
LEVEL_1_LAYOUT = "summary.xml"


""" Layouts """
EXPLORATION_OF_BREAST = {1:"summary.xml",
                         2:"tree.xml",
                         3:"edit_node.xml"}

MAMOGRAPHY = {1:"summary.xml",
              2:"tree.xml",
              3:"edit_node.xml"}

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

        
"""Localization strings. 
Replace template strings using a dictionary. 
Check internalization standard (and more complex) methods to improve this

"""
ENGLISH = {"ADD":"Add",
           "FINISH":"Finish",
           "VALIDATE":"Validate",
           "CHANGE":"Change",
           "NEXT  _LEVEL": "Children level"}

SPANISH = {"ADD":"Añadir",
           "FINISH":"Terminar",
           "VALIDATE":"Validar",
           "CHANGE":"Cambiar",
           "NEXT_LEVEL": "Siguiente nivel"}
 

""" Level names [EN] """
EXPLORATION_OF_BREAST_LEVELS = {1:"Summary",
                                2:"Organs",
                                3:"Lesions"}

MAMOGRAPHY_ACTIVITIES_LEVELS = {1:"Summary",
                                2:"Organs",
                                3:"Lesions"}

LEVELS_DICTIONARY = {4:EXPLORATION_OF_BREAST_LEVELS,
                     5:MAMOGRAPHY_LEVELS}




CONCEPT_LAYOUT = {"CONCEPT_NAME":"",
                  "CODE_VALUE":"",
                  "PREVIOUS":""}

