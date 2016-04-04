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

def expand_bbox(bbox, img_size):
    """
    Expand region such that is still within image and tries to satisfy
    these constraints best requirements: each dimension is at least 
    50 pixels, and max aspect ratio os (.25,4)
    """
    for expandloop in range(10000):
        #get initial dimensions
        w = bbox[2] - bbox[0] + 1
        h = bbox[3] - bbox[1] + 1
        
        if h > w*4 or w < 50:
            #make wider
            bbox[2] = bbox[2] + 1
            bbox[0] = bbox[0] - 1
        elif w > h*4 or h < 50:
            #make taller
            bbox[3] = bbox[3] + 1
            bbox[1] = bbox[1] - 1
        else:
            break
        
    clamp = lambda n, minn, maxn: max(min(maxn,n), minn)
    #make sure that bbox is still inside the image
    clamp(bbox[0], 1, img_size[1])
    clamp(bbox[1], 1, img_size[0])
    clamp(bbox[2], 1, img_size[1])
    clamp(bbox[3], 1, img_size[0])
    
    return bbox

def feature_pyramid(img):
    """
    Compute feature pyramid for different image scales
    
    Returns:
    -------
    tuple
        -np.array, each element is a np.array which represents HoG feature
        -np.array, each element is double-precision number which re
    
    """
        