from catcam.video_stream import VideoStream
from catcam.curses_image import CursesWindow, CursesFrameRenderer
import time, curses, sys, os, signal


def report_framerate_and_exit(signal, frame):
    curses.endwin()
    print("%.2f FPS at window size (%d, %d)" % (
        (nframes / (time.time() - t)),
        curses.COLS,
        curses.LINES))
    sys.exit()
    
if __name__ == "__main__":
    nframes = 0
    t = time.time()
    signal.signal(signal.SIGINT, report_framerate_and_exit)
    with CursesWindow() as curses_window:
        url = os.getenv('CATCAM_URL')
        video_stream = VideoStream(url)
        curses_renderer = CursesFrameRenderer(curses_window.shape)
        for frame in video_stream.iter_frames():
            curses_frame = curses_renderer.render_frame(frame)
            curses_window.draw(curses_frame)
            nframes += 1
