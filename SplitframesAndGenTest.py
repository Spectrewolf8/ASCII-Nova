import time

import VideoToAsciiJsonGzip
from videoObject import VideoObject

inittime = time.time()
videoObjectx = VideoObject('BadAppleForPython2.mp4', 0)
ASCII_CHARS = ['.', ',', ':', ';']
VideoToAsciiJsonGzip.renderVideoToAsciiJson(videoObjectx, 240, 64, ASCII_CHARS)
print('Time take:', time.time() - inittime)
