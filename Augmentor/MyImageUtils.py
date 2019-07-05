from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import os
import glob
import numbers
import random
import warnings
import numpy as np
import sys
from os.path import join, abspath, exists, basename
try:
    from imutils import paths
except:
    raise ImportError('Imutils package not installed, please use "pip install imutils"')
from .ImageUtilities import AugmentorImage


def scan(image_paths, output_directory):
    output_directory = abspath(output_directory)
    print(output_directory)

    augmentor_images = []
    for image_path in image_paths:
        if exists(image_path):
            a = AugmentorImage(image_path=image_path, output_directory=output_directory)
            a.file_format=os.path.splitext(image_path)[1].split(".")[1]
            augmentor_images.append(a)
    return augmentor_images



