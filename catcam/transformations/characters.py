import numpy as np


class ImageToCharactersTransformer(object):
    def __init__(self, characters='@&B9#SGHMh352AXsri;:,. ', contrast_factor=3):
        self.character_gradient = np.asarray(list(characters))
        self.character_resolution = len(self.character_gradient)
        self.contrast_factor = contrast_factor

    def normalize(self, arr):
        return (arr - arr.min()) / (arr.max() - arr.min())

    def scale_contrast(self, arr, contrast_factor):
        return arr ** contrast_factor

    def bin_characters(self, intensities):
        indices = (intensities * (self.character_resolution - 1)).round().astype(int)
        return self.character_gradient[indices]

    def map_pixels_to_characters(self, pixels):
        intensities = self.normalize(np.sum(pixels, axis=2))
        intensities = self.scale_contrast(intensities, self.contrast_factor) 
        return self.bin_characters(intensities)
