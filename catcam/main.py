from video_stream import VideoStream
from video_config import config
from curses_image import CursesWindow, CursesFrameRenderer

if __name__ == "__main__":
    curses_window = CursesWindow()
    try:
        url = config['url']
        auth = (config['user'], config['password'])
        video_stream = VideoStream(url, auth)
        curses_renderer = CursesFrameRenderer(curses_window.shape)
        for frame in video_stream.iter_frames():
            curses_frame = curses_renderer.render_frame(frame)
            curses_window.draw(curses_frame)
    finally:
        curses_window.close()
