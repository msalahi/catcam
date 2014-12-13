from video_stream import VideoStream
from video_config import config
from curses_image import CursesWindow, CursesFrameRenderer
import time
import curses
import sys
import signal


def exit_gracefully(signal, frame):
    curses.endwin()
    print(curses.COLS, curses.LINES)
    print("%.2f FPS" % (nframes / (time.time() - t)))
    sys.exit()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    curses_window = CursesWindow()
    curses_renderer = CursesFrameRenderer(curses_window.shape)
    url = config['url']
    auth = (config['user'], config['password'])
    video_stream = VideoStream(url, auth)
    nframes = 0
    t = time.time()
    for frame in video_stream.iter_frames():
        curses_frame = curses_renderer.render_frame(frame)
        curses_window.draw(curses_frame)
        nframes += 1
    
