import curses
import numpy as np
from catcam.transformations.characters import ImageToCharactersTransformer
from catcam.transformations.colors import ColorSchemeTransformer
from catcam.xterm_colors import xterm_256_colors


class CursesFrame(object):
    """ Holds character and color information for curses to display """
    def __init__(self, characters, colors):
        self.characters = characters
        self.colors = colors

    def __eq__(self, other):
        return (isinstance(other, CursesFrame) and
               np.array_equal(self.characters, other.characters) and
               np.array_equal(self.colors, other.colors))


class CursesFrameRenderer(object):
    """ Transforms images into CursesFrames """    
    def __init__(self, curses_shape):
        self.curses_shape = curses_shape
        self.character_transformer = ImageToCharactersTransformer()
        self.color_transformer = ColorSchemeTransformer(xterm_256_colors)

    def render_frame(self, image):
        """
        Takes in an Image object. Resizes to terminal window size,
        maps pixel darkness to characters, and matches pixel colors to
        closest colors available to xterm. Returns CursesFrame.
        """
        arr = np.array(image.resize(self.curses_shape))
        characters = self.character_transformer.map_pixels_to_characters(arr)
        colors = self.color_transformer.nearest_neighbors(arr)
        return CursesFrame(characters, colors)


class CursesWindow(object):
    """ An interface for drawing to curses """
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

    def __enter__(self):
        """ no additional setup needed """
        return self

    def __exit__(self, exception_type, exception, traceback):
        """ just proxy to regular close() """
        self.close()

    def use_black_text(self):
        """ Use black text in our curses colorpairs """ 
        black_foreground = 0
        for color in range(curses.COLORS):
            curses.init_pair(color, black_foreground, color)

    def draw(self, curses_frame):
        """ Takes in a CursesFrame, draws to terminal window """
        nrows, ncols = self.shape[1], self.shape[0]
        for row in range(nrows):
            for col in range(ncols):
                self.screen.addch(row, col,
                    curses_frame.characters[row][col],
                    curses.color_pair(curses_frame.colors[row][col]))
        self.screen.refresh()
