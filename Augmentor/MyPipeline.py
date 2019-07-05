from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from PIL.Image import Image
from builtins import *
import sys
sys.path.append('repo/Augmentor')
from .Operations import *
from .ImageUtilities import AugmentorImage
from .MyImageUtils import scan

import os
import sys
import random
import warnings
import uuid
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from os.path import join, abspath, exists, basename
from .Pipeline import Pipeline as OriginalPipeline


class Pipeline(OriginalPipeline):

    def __init__(self, image_paths=None,output_directory='output',save_format=None):
        self.image_counter = 0
        self.augmentor_images = []
        self.distinct_dimensions = set()
        self.distinct_formats = set()
        self.operations = []
        self.class_labels = []


        if image_paths is not None:
            self._populate(image_paths=image_paths,
                           output_directory=output_directory)

    def _populate(self, image_paths, output_directory):
        abs_output_directory = abspath(output_directory)
        self.augmentor_images = scan(image_paths, abs_output_directory)
        self._check_images(abs_output_directory)

    def _execute(self, augmentor_image, save_to_disk=True):
        images = []

        if augmentor_image.image_path is not None:
            images.append(Image.open(augmentor_image.image_path))

        for operation in self.operations:
            r = round(random.uniform(0, 1), 1)
            if r <= operation.probability:
                images = operation.perform_operation(images)
        if save_to_disk:
            for i in range(len(images)):
                _id = str(uuid.uuid4())
                save_name = 'aug.{}.{}'.format(_id, augmentor_image.image_path)
                images[i].save(join(augmentor_image.output_directory, save_name.replace('/', '.')))
        return images[0]

    def process(self, rounds=1):
        if len(self.augmentor_images) == 0:
            raise IndexError("There are no images in the pipeline. "
                             "Add a directory using add_directory(), "
                             "pointing it to a directory containing images.")

        if len(self.operations) == 0:
            raise IndexError("There are no operations associated with this pipeline.")

        for _ in range(rounds):
            with tqdm(total=len(self.augmentor_images), desc="Executing Pipeline", unit=" Samples") as progress_bar:
                    with ThreadPoolExecutor(max_workers=None) as executor:
                        for result in executor.map(self._execute,self.augmentor_images):
                            progress_bar.update(1)



























