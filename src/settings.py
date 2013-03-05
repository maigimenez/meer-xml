# -*- coding: utf-8 -*-

""" XML files """
STRINGS_XML = "strings.xml"
LEVEL_1_LAYOUT = "summary.xml"


        
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
 

""" Level names """
EXPLORATION_OF_BREAST_LEVELS = {1:"Summary",
                                2:"Organs",
                                3:"Lesions"}

EXPLORACION_DE_PECHO_NIVELES = {1:"Resumen",
                                2:"Organos",
                                3:"Lesiones"}

MAMOGRAPHY_LEVELS = {1:"Summary",
                     2:"Organs",
                     3:"Lesions"}

MAMOGRAFIA_NIVELES = {1:"Resumen",
                      2:"Organos",
                      3:"Lesiones"}

LEVELS_DICTIONARY = {4:{"en":EXPLORATION_OF_BREAST_LEVELS,
                        "es":EXPLORACION_DE_PECHO_NIVELES},
                     5:{"en":MAMOGRAPHY_LEVELS,
                        "es":MAMOGRAFIA_NIVELES}
                     }


CONCEPT_LAYOUT = {"CONCEPT_NAME":"",
                  "CODE_VALUE":"",
                  "PREVIOUS":""}

