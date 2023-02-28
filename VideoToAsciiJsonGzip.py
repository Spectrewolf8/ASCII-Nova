import os

import cv2
import ImageToAscii as imageToAscii


def renderVideoToAsciiFramesList(path, renderTextWidth, renderTextHeight):
    capture = cv2.VideoCapture('BadAppleForPython.mp4')

    frameNr = 0
    asciiFramesBuffer = []
    while True:

        success, frame = capture.read()
        print(type(frame), frame)

        if success:
            cv2.imwrite(f'FramesToConvertToAscii/{frameNr}.jpg', frame)
        else:
            break
        wholeFrame = ""
        for ascii_rowns in imageToAscii.convert_Image_To_Ascii(f'temp/{frameNr}.jpg',
                                                               (round(60), round(30))):
            wholeFrame += "\n" + ascii_rowns  # splitting lines onto next lines
        asciiFramesBuffer.append(wholeFrame)
        os.remove(f'FramesToConvertToAscii/{frameNr}.jpg')
    capture.release()
    return asciiFramesBuffer


def makeJsonGzip(videoObject):
