import pytest
from numpy.testing import assert_array_equal
import numpy as np
from catcam.transformations.colors import *


@pytest.fixture
def color_transformer():
    color_scheme = [
        (255, 0  , 0  ),
        (0  , 255, 0  ),
        (0  ,   0, 255)]
    return ColorSchemeTransformer(color_scheme)


def test_color_nearest_neighbors(color_transformer):
    # indices of colors as they appear in our color scheme
    red, green, blue = 0, 1, 2

    # test colors
    mostly_red = (250, 1, 1)
    mostly_green = (10, 255, 2)
    mostly_blue = (50, 1, 249)
    
    # image of dimensions: nrows x ncols x nchannels (rgb)
    pixels =  np.array([mostly_red, mostly_green, mostly_blue])
    pixels = pixels.reshape((3, 1, 3))
    expected_result = np.array([red, green, blue])

    # reshape to match expected output shape
    expected_result = expected_result.reshape((3, 1))
    matched_colors = color_transformer.nearest_neighbors(pixels)
    assert_array_equal(matched_colors, expected_result)
