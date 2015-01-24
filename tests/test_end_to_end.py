from PIL import Image
from catcam.video_stream import VideoStream
from catcam.curses_image import CursesFrameRenderer, CursesFrame
import pytest
import numpy as np
import http.server
from multiprocessing import Process
import io


def jpeg_encode_image(image):
    jpeg_bytes = io.BytesIO()
    image.save(jpeg_bytes, 'JPEG')
    return jpeg_bytes.getvalue()


@pytest.fixture
def jpeg_and_curses_test_data():
    data = {}
    white, black = (255, 255, 255), (0, 0, 0)
    image = Image.fromarray(np.array([[white, black]], np.uint8))
    curses_colors, curses_chars = np.array([[15, 16]]), np.array([[' ', '@']])
    data = {
        'image': image,
        'jpeg_bytes': jpeg_encode_image(image),
        'curses_frame': CursesFrame(curses_chars, curses_colors)}
    return data


class MJPEGRequestHandler(http.server.BaseHTTPRequestHandler):
    jpeg_bytes = jpeg_and_curses_test_data()['jpeg_bytes']
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(MJPEGRequestHandler.jpeg_bytes)
        return


@pytest.fixture
def video_stream_server():
    address = ('127.0.0.1', 55555)
    return http.server.HTTPServer(address, MJPEGRequestHandler)

    
def test_end_to_end(video_stream_server, jpeg_and_curses_test_data):
    """
    End-to-end test to ensure that catcam is able to:
        
        a) stream a jpeg image over http
        b) map image's colors to xterm-256 colors
        c) map image pixel brightnesses to ascii characters
        d) successfully render image as a CursesFrame

    Test sets up a toy http server process to serve a small jpeg image on GET
    request. Server process is destroyed after streaming a single frame.
    """

    # start test http server to serve up a small, static image
    video_url = "http://{}:{}".format(*video_stream_server.server_address)
    video_stream_server_process = Process(target=video_stream_server.serve_forever)
    video_stream_server_process.start()

    # stream a single frame from http server, terminate server process
    frame = next(VideoStream(video_url).iter_frames())
    video_stream_server_process.terminate()
    
    # render received image and expected image as curses frames and assert equal.
    curses_frame = CursesFrameRenderer(frame.size).render_frame(frame)
    assert curses_frame == jpeg_and_curses_test_data['curses_frame']
