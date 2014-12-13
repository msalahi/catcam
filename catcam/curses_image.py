import curses
import numpy as np
from transformations.characters import ImageToCharactersTransformer
from transformations.colors import ColorSchemeTransformer
from xterm_colors import xterm_256_colors


class CursesFrame(object):
    def __init__(self, characters, colors):
        self.characters = characters
        self.colors = colors


class CursesFrameRenderer(object):
    def __init__(self, curses_shape):
        self.curses_shape = curses_shape
        self.character_transformer = ImageToCharactersTransformer()
        self.color_transformer = ColorSchemeTransformer(xterm_256_colors)

    def render_frame(self, image):
        arr = np.array(image.resize(self.curses_shape))
        characters = self.character_transformer.map_pixels_to_characters(arr)
        colors = self.color_transformer.nearest_neighbors(arr)
        return CursesFrame(characters, colors)


class CursesWindow(object):
    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        self.use_black_text()
        self.shape = (curses.COLS - 1, curses.LINES - 1)

    def close(self):
        """ Terminates the curses application. """
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def use_black_text(self):
        for i in range(curses.COLORS):
            curses.init_pair(i, 0, i)

    def draw(self, curses_frame):
        nrows, ncols = self.shape[1], self.shape[0]
        for row in range(nrows):
            for col in range(ncols):
                self.screen.addch(
                    row,
                    col,
                    curses_frame.characters[row][col],
                    curses.color_pair(curses_frame.colors[row][col]))
            self.screen.addch(row, ncols, "\n")
        self.screen.refresh()
