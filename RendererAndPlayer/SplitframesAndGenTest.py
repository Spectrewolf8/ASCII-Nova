import time

import VideoToAsciiJsonGzip
from VideoObject import VideoObject

inittime = time.time()
videoObjectx = VideoObject('E:\ASCII-Nova Full\BadAppleZero\RendererAndPlayer\BadAppleForPython2.mp4')
ASCII_CHARS = ["@", "#", "＄", "%", "?", "*", "+", ";", ":", ",", "."]
VideoToAsciiJsonGzip.videoPath = videoObjectx.path
VideoToAsciiJsonGzip.renderVideoToAsciiJsonGzip()
print('Time take:', time.time() - inittime)
