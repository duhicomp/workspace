import os
import logging
from techrtime import *
import bko_api as bko

############## getVPFObjects
## vpf_zone: the zone where your objects will be grabbed
## types: the list of object's types to search (bko.VPFText,...)
## crossing_type: [0: object must be completely in zone, 1: even partially is ok]
## return the list of elements found
def getVPFObjects(vpf_zone, types=None, crossing_type=0):
    object_list = []
    vpf_zone.crossing = crossing_type
    ite = vpf_zone.newIterator()
    while ite.hasNext() :
        e = ite.getNextElement()
        if e:
            object_list.append(e)
    del ite
    
    if isinstance(types, list):
        object_list = [x for x in object_list if type(x) in types]
    
    return object_list

############## getVPFObjects_by_fonts
## vpf_zone: the zone where your objects will be grabbed
## font_names: the list of font names to search
## return the list of elements found
def getVPFObjects_by_fonts(vpf_zone, font_names):
    objects_list = getVPFObjects(vpf_zone, [bko.VPFText])
    logging.debug('texts found :' + str([x.getText().strip() for x in objects_list]))
    objects_list = [x for x in objects_list if x.getFontName() in font_names]
    logging.debug('texts found with the font:' + str([x.getText().strip() for x in objects_list]))
    return objects_list


############## catVPFTexts
## vpf_zone: the zone where your texts will be grabbed
## return the concatenation of all texts found in the zone (with a white space between each element)
def catVPFTexts(vpf_zone):
    string = ''
    objects_list = getVPFObjects(vpf_zone, [bko.VPFText])
    
    for e in objects_list:
        string += e.getText().strip() + ' '
    
    string.strip() # remove last white space
    return string


def formatDate(date):
    month, day, year = date.split('/')
    year = year[-2:]
    return '/'.join([month, day, year])

def set_defaults(default_params_dict):
    for key in default_params_dict.keys():
        # key_string = '"app_param_' + key + '"'
        if default_params_dict[key][0] == ("" or key):
            setattr(techvars, key, default_params_dict[key][1])

############## lineParser
## zone: where text will be grabbed from
## threshold: an integer (used as a percentage), combined with font size to compute the offset accepted to consider new line or not
## spacing: an integer (used as a percentage), combined with font size to compute the offset accepted to consider white between two chars or not
def lineParser(zone, expectedLinesReturned=0, threshold=33, spacing=12) :
    # TOIMPROVE assumes that logging is defined...
    logging.debug("--- BEGIN VPF LINE PARSING ---")
    
    zone_objects = getVPFObjects(zone, [bko.VPFText])
    
    try :
        # TOIMPROVE assumes that all elements in the zone have the same font size...
        # TOIMPROVE also assumes that you set bko.setUnit(bko.Unit('pica', 100)) (otherwise, it would need to divided by 100)
        
        heightMargin = zone_objects[0].getFontSize() * threshold
        # logging.debug('heightMargin '+ str(heightMargin))
        
        # whiteSpaceMargin = zone_objects[0].getWordSpace() # TODO what is the point of Word Space ???
        whiteSpaceMargin = zone_objects[0].getFontSize() * spacing
        # logging.debug('whiteSpaceMargin '+ str(whiteSpaceMargin))
        
        elements_dict = lineSort(zone_objects, zone_objects[0].orientation, heightMargin)
        reverses = lineReverses(zone_objects[0].orientation)
        
    except Exception, e:
        logging.warn("Returning nothing: zone has no text (out of range raised) OR orientation not supported: "+ str(e))
        # logging.debug("--- END VPF LINE PARSING ---")
        empty = ''
        if expectedLinesReturned > 0:
            empty = [''] * expectedLinesReturned
        return empty
    
    # using the sorted texts to create the lines
    lines_list = []
    indexes_list = sorted(elements_dict, reverse=reverses[0])
    for index in indexes_list :
        line = lineConcat(elements_dict[index], reverses[1], whiteSpaceMargin)
        lines_list.append(line)
    
    # if you defined an expected length
    if expectedLinesReturned > 0:
        if len(lines_list) > expectedLinesReturned:
            # trimming the list to expected length
            lines_list = lines_list[:expectedLinesReturned-1]
        
        elif len(lines_list) < expectedLinesReturned:
            # filling missing lines with blanks
            for i in range(len(lines_list), expectedLinesReturned):
                lines_list.append('')
    
    logging.debug("Returning: " + str(lines_list))
    logging.debug("--- END VPF LINE PARSING ---")
    return lines_list

############## lineSort
## objects_list: the list of objects to sort
## orientation: the orientation
## heightMargin: the margin where you consider the elements to be on the same line or not
## return a dict with the objects sorted
def lineSort(objects_list, orientation, heightMargin):
    elements_dict = {}
    heightMargin = int(heightMargin)
    
    if orientation == 0 :
        dim1 = 'y'
        dim2 = 'x'
        # logging.debug("orientation 0")
    elif orientation == 90 :
        dim1 = 'x'
        dim2 = 'y'
        # logging.debug("orientation 90")
    elif orientation == 180 :
        dim1 = 'y'
        dim2 = 'x'
        # logging.debug("orientation 180")
    elif orientation == 270 :
        dim1 = 'x'
        dim2 = 'y'
        # logging.debug("orientation 270")
    else :
        raise Exception("text orientation '" + str(orientation) + "' not supported")

    # sorting the texts according to their x and y
    for e in objects_list:
        placed = False
        if e.getText().strip() != '' :
            v1 = int(getattr(e, dim1))
            v2 = int(getattr(e, dim2))
            for i in range(v1 - heightMargin, v1 + heightMargin):
                if i in elements_dict.keys():
                    elements_dict[i][v2] = e
                    placed = True
                    break
            if not placed:
                elements_dict[v1] = {}
                elements_dict[v1][v2] = e
    
    return elements_dict

############## lineConcat
## objects_list: the list of objects to sort
## isReverse: does it have to be parsed in reverse
## whiteSpaceMargin: the margin where you consider that elements need a white space between them
## return the line
def lineConcat(objects_list, isReverse, whiteSpaceMargin):
    line = ""
    indexes = sorted(objects_list, reverse=isReverse)
    prevEnd = -1
    for index in indexes :
        if prevEnd != -1 and (isReverse and (prevEnd - whiteSpaceMargin) >= index or not isReverse and (prevEnd + whiteSpaceMargin) <= index) :
            line += " "
        # TOKNOW: actually, width and height are always "logically correct" (height will still be the height of the text, whether it's leaning or not; same for width)
        # TOKNOW: in the same idea, x and y will always refer to the beginning of the string (and not necessarily to the first corner found from the origin)
        # subindex <=> e.dim2 (x or y, depending on the orientation)
        if isReverse:
            prevEnd = index - objects_list[index].getWidth()
        else:
            prevEnd = index + objects_list[index].getWidth()
        line += objects_list[index].getText().strip()
    
    return line

def lineReverses(orientation):
    if orientation == 0 :
        reverses = [False, False]
        # logging.debug("orientation 0")
    elif orientation == 90 :
        reverses = [False, True]
        # logging.debug("orientation 90")
    elif orientation == 180 :
        reverses = [True, True]
        # logging.debug("orientation 180")
    elif orientation == 270 :
        reverses = [True, False]
        # logging.debug("orientation 270")
    else :
        raise Exception("text orientation '" + str(orientation) + "' not supported")
    
    return reverses
