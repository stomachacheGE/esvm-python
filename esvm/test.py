# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:02:37 2016

@author: liangfu
"""

import pyhog
import numpy as np
import matplotlib.pyplot as pl
from scipy.misc import imread, imrotate

import features_pedro_py

img = (imread('../VOC2007/JPEGImages/000015.jpg').astype(np.float64)/255.0)
pl.imshow(img)
pl.axis('off')



hog = pyhog.features_pedro(img, 30)
hog.shape

