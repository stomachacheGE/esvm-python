# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:20:24 2016

@author: liangfu
"""
import os

from config import *

import numpy as np

from utils import xml_to_cls_bboxs, expand_bbox, feature_pyramid,
                  get_matching_mask
from skimage.io import imread

class Exemplar(object):
    """
    This is the class representing an exemplar.    
    """
    def __init__(self, cls, img_id, img_path, img_size, bbox, anno_path):
        self.cls = cls
        self.img_id = img_id
        self.img_path = img_path
        self.img_size = img_size
        self.bbox = bbox
        self.anno_path = anno_path
    
    def initialize(self):
        """
        Initialize an exemplar to get HOG features,
        as well as to initialize a svm model 
        corresponding to this exemplar.
        """
        img_path = imagesets_directory + '/' + str(self.img_id) + '.jpg'
        img = imread(img_path)
        
        #Expand the bbox to have some minimum and maximum aspect ratio
        #constraints (if it it too horizontal, expand vertically, etc)
        self.bbox = expand_bbox(self.bbox, self.img_size)
        #create a blank image with the exemplar inside
        Ibox = np.zeros((self.img_size[0], self.img_size[1]),
                         dtype=np.int)
        Ibox[self.bbox[1]:self.bbox[3], self.bbox[0]:self.bbox[2]] = 1
        #get the Hog feature pyramid for the entire image
        (feat, scale) = feature_pyramid(img)
        #extract the regions most overlapping with Ibox 
        #from each level in the pyramid
        

    @staticmethod
    def load(cls_name, img_id):
        """
        Load exemplars from an image.

        Returns:
        -------
        List with element being Exemplar object, if any
        """
        
        exemplars = []
        
        anno_path = anno_directory + '/' + str(img_id) + '.xml'
        bboxs = xml_to_cls_bboxs(cls_name, anno_path)
        
        #if no object found in that image, return empty list
        if len(bboxs) == 0:
            return []

        img_path = '{}/{}.jpg'.format(images_directory, img_id)
        img = imread(img_path)
        img_size = img.shape
              
        for bbox in bboxs:
            exemplar = Exemplar(cls_name, img_id, img_path, img_size, bbox, anno_path)
            exemplars.append(exemplar)
        
        return exemplars