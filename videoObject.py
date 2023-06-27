import os
import cv2


class VideoObject:
    def __init__(self, path, renderTextWidth=0):
        self.path = path
        self.filename = os.path.basename(path)
        cap = cv2.VideoCapture(path)
        self.numberOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = float(cap.get(cv2.CAP_PROP_FPS))
        self.frames = []
        self.renderChars = ''
        self.renderTextWidth = int(renderTextWidth)
        self.base64Audio = ''
