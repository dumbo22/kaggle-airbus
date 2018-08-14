import math
from functools import partial

import numpy as np

from airbus.utils import get_images_in
from airbus.utils import get_mask_db
from airbus.utils import get_train_validation_holdout_split
from airbus.utils import pipeline

class DataGenerator:
    def __init__(self, records, batch_size, transform, shuffle=True):
        self.records = records
        self.batch_size = batch_size
        self.transform = transform
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle: np.random.shuffle(self.records)
        batch = []

        for output in map(self.transform, self.records):
            batch.append(output)

            if len(batch) >= self.batch_size:
                split_outputs = list(zip(*batch))
                yield map(np.stack, split_outputs)
                batch = []

        if len(batch) > 0:
            split_outputs = list(zip(*batch))
            yield map(np.stack, split_outputs)

    def __len__(self):
        return math.ceil(len(self.records) / self.batch_size)

def get_validation_generator(batch_size, limit=None):
    image_paths = get_images_in('data/train')
    _, image_paths, _ = get_train_validation_holdout_split(image_paths)
    mask_db = get_mask_db('data/train_ship_segmentations.csv')
    transform = partial(pipeline, mask_db)
    return DataGenerator(image_paths[:limit], batch_size, transform)

def get_train_generator(batch_size, limit=None):
    image_paths = get_images_in('data/train')
    image_paths, _, _ = get_train_validation_holdout_split(image_paths)
    mask_db = get_mask_db('data/train_ship_segmentations.csv')
    transform = partial(pipeline, mask_db)
    return DataGenerator(image_paths[:limit], batch_size, transform)