from PIL import Image
from catcam.video_stream import VideoStream
from catcam.curses_image import CursesFrameRenderer
import pytest
import numpy as np
import http.server
from multiprocessing import Process
import io


def tiny_jpeg_bytes():
    white, black = (255, 255, 255), (0, 0, 0)
    image = Image.fromarray(np.array([[white, black]], np.uint8))
    jpeg_bytes = io.BytesIO()
    image.save(jpeg_bytes, 'JPEG')
    return jpeg_bytes.getvalue()


class MJPEGRequestHandler(http.server.BaseHTTPRequestHandler):
    jpeg_bytes = tiny_jpeg_bytes()
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

    
def test_end_to_end(video_stream_server):
    """
    End-to-end test to ensure that catcam is able to:
        
        a) stream a jpeg image
        b) map image's colors to xterm-256 colors
        c) map image pixel brightnesses to ascii characters
        d) image is rendered successfully as a CursesFrame

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
    curses_frame_renderer = CursesFrameRenderer((2, 1))
    curses_frame = curses_frame_renderer.render_frame(frame)
    test_image = Image.open(io.BytesIO(tiny_jpeg_bytes()))
    expected_curses_frame = curses_frame_renderer.render_frame(test_image)
    assert curses_frame == expected_curses_frame
