from catcam.transformations.characters import *
from numpy.testing import assert_array_equal
import numpy as np
import pytest


@pytest.fixture
def character_transformer():
    return ImageToCharactersTransformer(contrast_factor=1)


def test_normalize(character_transformer):
    arr = np.array([0, .25, .5, .75, 1])
    normalized = character_transformer.normalize(arr)
    assert_array_equal(arr, normalized)


def test_scale_contrast(character_transformer):
    arr = np.arange(5)
    sqrt_arr = np.sqrt(arr)
    identity_result = character_transformer.scale_contrast(arr, 1)
    sqrt_result = character_transformer.scale_contrast(arr, .5)
    assert_array_equal(arr, identity_result)
    assert_array_equal(sqrt_arr, sqrt_result)


def test_bin_characters(character_transformer):
    nshades = character_transformer.character_resolution
    gradient = character_transformer.character_gradient
    arr = np.arange(nshades).astype(float) / (nshades - 1)
    binned_range = character_transformer.bin_characters(arr)
    assert_array_equal(binned_range, gradient)
    

def test_map_pixels_to_characters(character_transformer):
    nshades = character_transformer.character_resolution
    gradient = character_transformer.character_gradient
    arr = [[[i, i, i]] for i in range(nshades)]
    chars = character_transformer.map_pixels_to_characters(arr)
    assert_array_equal(chars.reshape((nshades)), gradient)
