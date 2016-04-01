# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:29:01 2016

@author: liangfu
"""

"""Utility Functions"""

def xml_to_cls_bboxs(cls, file_path):
    
    import xmltodict
    
    bbox_list = []
    #parse .xml into ordered dict
    with open(file_path, 'r') as file:
        xml_dict = xmltodict.parse(file.read())
    #if only one object is in picture, firsty
    #convert xml_dict to a list for later use
    objects = xml_dict['annotation']['object']
    if not isinstance(objects, list):
        objects_list = []
        objects_list.append(objects)
        objects = objects_list
        
    for cls_object in objects:
        #only return specified class objects which are not
        #considered to be difficult
        cls_object_dict = dict(cls_object)
        if (cls_object_dict['name'] == cls) and (cls_object_dict['difficult'] == '0'):
            bndbox = dict(cls_object_dict['bndbox'])
            #order of bbox is: xmin, ymin, xmax, ymax
            bbox = [int(bndbox['xmin']), int(bndbox['ymin']), 
                    int(bndbox['xmax']), int(bndbox['ymax'])]
            bbox_list.append(bbox)
        else:
            continue
    
    return bbox_list