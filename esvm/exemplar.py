# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:20:24 2016

@author: liangfu
"""
import os

from config import *

import numpy as np

class Exemplar(object):
    """
    This is the class representing an exemplar.    
    """
    def __init__(self, cls, img_id, img_path, bbox, anno_path):
        self.cls = cls
        self.img_id = img_id
        self.img_path = img_path
        self.bbox = bbox
        self.anno_path = anno_path

    @staticmethod
    def load(cls_name, img_id):
        """
        Load exemplars from an image.

        Returns:
        -------
        List with element being Exemplar object
        """
        
        from utils import xml_to_cls_bboxs
        
        exemplars = []
        
        anno_path = anno_directory + '/' + str(img_id) + '.xml'
        bboxs = xml_to_cls_bboxs(cls_name, anno_path)
        
        #if no object found in that image, return empty list
        if len(bboxs) == 0:
            return []

        img_path = '{}/{}.jpeg'.format(images_directory, img_id)
        
        for bbox in bboxs:
            exemplar = Exemplar(cls_name, img_id, img_path, bbox, anno_path)
            exemplars.append(exemplar)
        
        return exemplars