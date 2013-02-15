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
ENGLISH = {"ADD":"Add",
           "FINISH":"Finish",
           "VALIDATE":"Validate",
           "CHANGE":"Change"}

SPANISH = {"ADD":"Añadir",
           "FINISH":"Terminar",
           "VALIDATE":"Validar",
           "CHANGE":"Cambiar"}


CONCEPT = {"CONCEPT_NAME":"",
           "CODE_VALUE":""}
