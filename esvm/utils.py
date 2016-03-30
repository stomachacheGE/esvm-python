# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:29:01 2016

@author: liangfu
"""

"""Utility Functions"""

def xml_to_cls_bboxs(cls, file_path):
    
    import xmltodict
    
    bbox_list = []
    #parse .xml into a ordered dict
    with open(file_path, 'r') as file:
        xml_dict = xmltodict.parse(file.read())
        
    for cls_object in xml_dict['annotation']['object']:
        #only return specified class objects which are not
        #considered to be difficult
        cls_object_dict = cls_object
        if (cls_object_dict['name'] == cls) and (cls_object_dict['difficult'] == '0'):
            bndbox = dict(cls_object_dict['bndbox'])
            #order of bbox is: xmin, ymin, xmax, ymax
            bbox = [int(bndbox['xmin']), int(bndbox['ymin']), 
                    int(bndbox['xmax']), int(bndbox['ymax'])]
            bbox_list.append(bbox)
        else:
            continue
    
    return bbox_list