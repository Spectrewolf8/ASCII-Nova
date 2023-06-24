import time

import VideoToAsciiJsonGzip
from videoObject import VideoObject

inittime = time.time()
videoObjectx = VideoObject('BadAppleForPython2.mp4', 0)
VideoToAsciiJsonGzip.renderVideoToAsciiJson(videoObjectx, 120, 64)
print('Time take:', time.time() - inittime)
