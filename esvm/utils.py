# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:29:01 2016

@author: liangfu
"""

"""Utility Functions"""

import numpy as np
from config import *

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
        -list, each element is a np.array which represents HoG feature
        -np.array, each element is double-precision number which represents scale
    
    """
    
    #import scipy.ndimage.interpolation as npimage
        #it seems that using npimage.zoom brings some artifitials,
        #Unfortunately, scipy.misc.imresize only return uint8 array.
    from scipy.misc import imresize #however, still use imresize,
                                    #since it's 30x faster 
    from pyhog import features_pedro
    
    #change data type to float64
    #img = img.astype(np.float64, copy=False)/255.0
    
    MAXLEVELS = 200
    MINIDIMENSION = 5 
    interval = detect_levels_per_octave
    sc = 2 ** (1 / interval)
    
    feat = []
    scale = np.zeros((MAXLEVELS), dtype=float)
    
    #Start at detect_max_scale, and keep going down by the increment sc, until
    #we reach MAXLEVELS or detect_min_scale
    for i in range(MAXLEVELS):
        scaler = detect_max_scale / (sc ** (i))
        
        if scaler < detect_min_scale:
            return (feat, scale)
        
        scale[i] = scaler
        scaled = imresize(img, scaler).astype(np.float64, copy=False)/255.0
    
        #if minimum dimensions is less than or equal to 5, return
        if min(scaled.shape[0], scaled.shape[1]) <= MINIDIMENSION:
            scale = scale[np.where(scale > 0.0)]
            return (feat, scale)
        
        feature = features_pedro(scaled, sbin)
    
        #if we get zero size feature, backtrack one, and dont produce any
        #more levels
        if min(feature.shape[0], feature.shape[1]) == 0:
            scale = scale[:,:i]
            return (feat, scale)            

        #recover lost bin
        feature = np.lib.pad(feature,((1,1),(1,1),(0,0)),
                             'constant',constant_values=(0.0))
        feat.append(feature)
        
        #if max dimensions is less than or equal to 5, return
        if max(feature.shape[0], feature.shape[1]) <= MINIDIMENSION:
            scale = scale[np.where(scale > 0.0)]
            return (feat, scale)            
    
    return (feat, scale)
    
def get_matching_mask(f_real, Ibox):
    """
    Find the best matching region per level in the feature pyramid    
    """
    maskers = []
    sizers = []
    
    import numpy.ma as mask
    from scipy.misc import imresize
    
    for i in range(len(f_real)):
        feature_goods = mask.array(np.sum(np.square(f_real[i]), 2), dtype=np.bool_)
        Ibox_resize = imresize(Ibox, (f_real[i].shape[0], f_real[i].shape[1]))
        Ibox_resize = Ibox_resize.astype(np.float64) / 255.0
        Ibox_goods = Ibox_resize > 0.1
        
        masker = np.logical_and(feature_goods, Ibox_goods)
        
        max_indice = np.unravel_index(Ibox_resize.argmax(), Ibox_resize.shape)
        
        if np.where(masker == True)[0].size == 0:
            masker[max_indice[0], max_indice[1]] = True
            
        indices = np.where(masker == True)
        masker[np.amin(indices[0]):np.amax(indices[0]),
               np.amin(indices[1]):np.amax(indices[1])] = True
        sizer=[np.ptp(indices[0])+1, np.ptp(indices[1])+1]   
        maskers.append(masker)
        sizers.append(sizer)
        
    return(maskers, sizers)