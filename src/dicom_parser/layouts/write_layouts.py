#  -*- coding: utf-8 -*-
import logging
import os
from string import Template
from templates import *
#from jinja2 import Enviroment,PackageLoaderT,emplate

logging.basicConfig(filename='write-layouts.log',level=logging.INFO) 

def write_attributes_layout(xml_files,filename,attributes,previous):
    #template = Template('Hello {{ name }}')
    #template.render(name=='John Doe')
    #Variable where we store the previous concept id
    previous_item = previous        
    #Attributes
    for attr in attributes:
        #Fill the substitution dictionary with this concept
        CONCEPT_LAYOUT = {}
        CONCEPT_LAYOUT["CONCEPT_NAME"] = attr.concept.concept_name
        CONCEPT_LAYOUT["CONCEPT_VALUE"] = attr.concept.concept_value
        CONCEPT_LAYOUT["PREVIOUS_ITEM"] = previous_item
        #print CONCEPT_LAYOUT
        #print 
        #Write the xml for the attribute depending on its data type.
        if (attr.type == "date"):
            xml_files.layouts[filename].write(
                Template(DATE_LAYOUT).safe_substitute(CONCEPT_LAYOUT))
        elif (attr.type == "num"):
            xml_files.layouts[filename].write(
                Template(NUM_LAYOUT).safe_substitute(CONCEPT_LAYOUT))
        elif (attr.type == "text"):
            xml_files.layouts[filename].write(
                Template(NUM_LAYOUT).safe_substitute(CONCEPT_LAYOUT))
        #Now the previous value  has change, so we store the new one.
        previous_item = "etext_%s" % attr.concept.concept_value 
        logging.info("New previous item: {0}".format(previous_item))
        print u"  {0} ".format(attr).encode('utf-8')            
    return previous_item          
   
def write_one_column_layout(xml_files,filename_code,level,level_container):
    for concept,children in level_container.containers.iteritems():
        #Add the concept_value to the layout file and open the file for writting 
        filename = Template(filename_code).safe_substitute(CODE=concept.concept_value.lower())
        print filename, "One column"
        print concept
        xml_files.layouts[filename] = open(filename, 'w')
        try:
            print(" * {0}".format(concept))
            #Write the header, main and left layout
            xml_files.layouts[filename].write(HEADER_LAYOUT)
            xml_files.layouts[filename].write(MAIN_LAYOUT)    
            #Write the main title
            xml_files.layouts[filename].write(
                Template(TITLE_LAYOUT).safe_substitute(LEVEL=concept.concept_value))  
            #Variable where we store the previous concept id
            previous_item = "level_{0}_label".format(concept.concept_value)
               
            #Write the children's listView
            xml_files.layouts[filename].write(
                Template(NEXT_LEVEL_LAYOUT).safe_substitute(LEVEL=concept.concept_value))
            values=[]
            for concept in children.children_containers:
                values.append(concept.concept_name)
                print u"  -{0}".format(concept.concept_name).encode('utf-8')
                
            print 
            #Write the end of the layout
            xml_files.layouts[filename].write(END_LAYOUT) 

        except KeyError:
            #It should go to logging error
            print "Layouts can't be created"
 

def write_two_columns_layout_one_level(xml_files,filename,level,concept,children):
    print filename, "- Two columns"
    xml_files.layouts[filename] = open(filename, 'w')
    try:
        print(" * {0}".format(concept))
        #Write the header, main and left layout
        xml_files.layouts[filename].write(HEADER_LAYOUT)
        xml_files.layouts[filename].write(MAIN_LEFT_LAYOUT)    
            
        #There are only children in this layout
        if (len(children.attributes)>0):
            #Write the title
            xml_files.layouts[filename].write(
                Template(GENERIC_TITLE_LAYOUT).safe_substitute(LEVEL=level))  
            #Variable where we store the previous concept id
            previous_item = "level_{0}_label".format(level)
            num_attributes = len(children.attributes)
            first_attributes = children.attributes[0:num_attributes/2]
            last_attributes = children.attributes[num_attributes/2:]
            #Write the attributes
            previous_item = write_attributes_layout(xml_files,filename,first_attributes,previous_item)
            #Write the end of left layout, the right layout
            xml_files.layouts[filename].write(RIGHT_LAYOUT) 
            previous_item = write_attributes_layout(xml_files,filename,last_attributes,previous_item)

            
        #There are only children in this layout
        else:
            #Write the title
            xml_files.layouts[filename].write(
                Template(GENERIC_TITLE_LAYOUT).safe_substitute(LEVEL=level))  
            #Variable where we store the previous concept id
            previous_item = "level_{0}_label".format(level)

            #TODO: this is not handled in the string-array, so the java activitity will NOT
            #populate this properly
            #Write the children
            #Write the children's listView
            xml_files.layouts[filename].write(
                Template(NEXT_LEVEL_LAYOUT).safe_substitute(LEVEL=concept.concept_value+"-1"))
            xml_files.layouts[filename].write(RIGHT_LAYOUT) 
            xml_files.layouts[filename].write(
                Template(NEXT_LEVEL_LAYOUT).safe_substitute(LEVEL=concept.concept_value+"2"))

            #Write the end of the layout
            xml_files.layouts[filename].write(END_LAYOUT) 
            print
            
    except KeyError:
        #It should go to logging error
        print "Layouts can't be created"

def write_two_columns_layout_two_levels(xml_files,filename,level,concept,children):
    print filename, "- Two columns"
    xml_files.layouts[filename] = open(filename, 'w')
    try:
        print(" * {0}".format(concept))
        #Write the header, main and left layout
        xml_files.layouts[filename].write(HEADER_LAYOUT)
        xml_files.layouts[filename].write(MAIN_LEFT_LAYOUT)    
        #Write the left title
        xml_files.layouts[filename].write(Template(GENERIC_TITLE_LAYOUT).safe_substitute(LEVEL=level))  
        #Variable where we store the previous concept id
        previous_item = "level_{0}_label".format(level)
               
        #ATTRIBUTES
        write_attributes_layout(xml_files,filename,children.attributes,previous_item)

        #Write the end of left layout, the right layout and the listView for the next layout
        xml_files.layouts[filename].write(RIGHT_LAYOUT) 
                
        #CHILDREN
        #Write the right title
        xml_files.layouts[filename].write(Template(GENERIC_TITLE_LAYOUT).safe_substitute(LEVEL=level+1))
            
        #Write the children's listView
        xml_files.layouts[filename].write(
            Template(NEXT_LEVEL_LAYOUT).safe_substitute(LEVEL=level+1))
        #TODO: Children must be in a java array   
        for concept in children.children_containers:
            print u"  -{0}".format(concept.concept_name).encode('utf-8')

        #Write the end of the layout
        xml_files.layouts[filename].write(END_LAYOUT) 
        print
        
    except KeyError:
        #It should go to logging error
        print "Layouts can't be created"

def write_two_columns_layout(xml_files,filename_code,level,level_container):
    for concept,children in level_container.containers.iteritems():
        #Add the concept_value to the layout file and open the file for writting 
        filename = Template(filename_code).safe_substitute(CODE=concept.concept_value.lower())
        #If the file already exists do not write the layout again. 
        if (not os.path.isfile(filename)):
            #Without children or attributes there will be only one level in the layout
            if (len(children.attributes)==0 or len(children.children_containers)==0):
                print "One Level"
                write_two_columns_layout_one_level(xml_files,filename,level,concept,children)
            else:
                print "Two levels"
                write_two_columns_layout_two_levels(xml_files,filename,level,concept,children)
             
def write_layouts(xml_filenames,xml_files,report,deepest_level):
    """ Write xml layouts and settings.java with the arrays needed to populate the listviews """
    #Set which files are going to be used as output in this parser
    #TODO: Layouts
    #TODO: Java files 
    # The files for the layout are linked to the odontology of the report
    logging.info("\nWRITE LAYOUTS")
    xml_filenames.set_odontology(report.id_odontology)

    #Open for write all the files
    for level, layout in zip(xrange(1,deepest_level+1),xml_filenames.layouts.values()):
        print layout
        #Get the actual level to write its layout
        dict_level = report.get_level(level)
        print "[Level {0}]".format(level)
        #for the first and third level we went a one column layout
        #TODO: This should go to a conf file
        if (layout[1]==1):
            write_one_column_layout(xml_files,layout[0],level,dict_level)
        else:
            write_two_columns_layout(xml_files,layout[0],level,dict_level)
