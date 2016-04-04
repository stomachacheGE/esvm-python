# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:44:17 2016

@author: liangfu
"""
import configparser as cp
import json

config = cp.RawConfigParser()
config.read('../config.cfg')

visualize = config.getboolean("hog", "visualize")
normalize = config.getboolean("hog", "normalize")
anno_directory = config.get("paths", "anno_directory")
imagesets_directory = config.get("paths", "imagesets_directory")
images_directory = config.get("paths", "images_directory")
results_directory = config.get("paths", "results_directory")
threshold = config.getfloat("nms", "threshold")

#hog feature extraction
min_wdw_sz = json.loads(config.get("hog","min_wdw_sz"))
step_size = json.loads(config.get("hog", "step_size"))
orientations = config.getint("hog", "orientations")
pixels_per_cell = json.loads(config.get("hog", "pixels_per_cell"))
cells_per_block = json.loads(config.get("hog", "cells_per_block"))
sbin = config.getint("hog", "sbin")
goal_ncells = config.getint("hog", "goal_ncells")
maxdim = config.getint("hog", "MAXDIM")
detect_levels_per_octave = config.getint("hog", "detect_levels_per_octave")