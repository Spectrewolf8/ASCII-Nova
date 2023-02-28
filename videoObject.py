import os


class VideoObject:
    def __init__(self, path):
        self.filename = os.path.basename(path)
        self.numberOfFrames = int(cv2.VideoCapture(path).get(cv2.CAP_PROP_FRAME_COUNT))
