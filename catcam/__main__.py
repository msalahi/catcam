from catcam.video_stream import VideoStream
from catcam.curses_image import CursesWindow, CursesFrameRenderer
import time, curses, sys, os, signal

NFRAMES = 0
START_TIME = None

def report_framerate_and_exit(signal, frame):
    global START_TIME 
    global NFRAMES
    curses.endwin()
    print("%.2f FPS at window size (%d, %d)" % (
        (NFRAMES / (time.time() - START_TIME)),
        curses.COLS,
        curses.LINES))
    sys.exit()


def main():
    global START_TIME 
    global NFRAMES
    url = sys.argv[1] if len(sys.argv) > 1 else os.getenv('CATCAM_URL')
    
    if not url:
        print("Usage: catcam mjpeg_url")
        exit(1)

    START_TIME = time.time()
    signal.signal(signal.SIGINT, report_framerate_and_exit)

    with CursesWindow() as curses_window:
        video_stream = VideoStream(url)
        curses_renderer = CursesFrameRenderer(curses_window.shape)
        for frame in video_stream.iter_frames():
            curses_frame = curses_renderer.render_frame(frame)
            curses_window.draw(curses_frame)
            NFRAMES += 1


if __name__ == "__main__":
    main()
