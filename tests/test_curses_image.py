from catcam.curses_image import CursesFrameRenderer
from numpy.testing import assert_array_equal
import numpy as np
from PIL import Image
from catcam.xterm_colors import xterm_256_colors


def test_render_frame():
    # Make tiny image with one black pixel and one white pixel
    white, black = (255, 255, 255), (0, 0, 0)
    image = Image.fromarray(np.array([[white, black]], np.uint8))
    curses_frame_renderer = CursesFrameRenderer((2, 1))
    frame = curses_frame_renderer.render_frame(image)
    
    character_gradient = curses_frame_renderer.character_transformer.character_gradient
    lightest_character = character_gradient[-1]
    darkest_character = character_gradient[0] 
    expected_colors = [[xterm_256_colors.index(white), xterm_256_colors.index(black)]]
    expected_characters = [[lightest_character, darkest_character]]
    
    assert_array_equal(expected_colors, frame.colors)
    assert_array_equal(expected_characters, frame.characters)
