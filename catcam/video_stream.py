import requests
from io import BytesIO
from PIL import Image

JPG_START_MARKER = b'\xff\xd8'
JPG_END_MARKER = b'\xff\xd9'

class VideoStream(object):
    def __init__(self, stream_url, auth=None):
        self.url = stream_url
        self.auth = auth

    def image_from_bytes(self, img_bytes):
        frame_io = BytesIO(img_bytes)
        return Image.open(frame_io)

    def iter_frames(self):
        response = requests.get(self.url, auth=self.auth, stream=True)
        video_stream_chunks = response.iter_content(1024)
        frame_bytes = b''
        for chunk in video_stream_chunks:
            frame_bytes += chunk
            frame_start_index = frame_bytes.find(JPG_START_MARKER)
            frame_end_index = frame_bytes.find(JPG_END_MARKER)
            if frame_start_index != -1 and frame_end_index != -1:
                image = frame_bytes[frame_start_index: frame_end_index + 2]
                frame_bytes = frame_bytes[frame_end_index + 2:]
                image = self.image_from_bytes(image)
                yield image
