import os
import cv2
import ImageToAscii as imageToAscii
from videoObject import VideoObject
import compress_json


def renderVideoToAsciiJson(videoObject):
    capture = cv2.VideoCapture(videoObject.path)

    frameNr = 0
    asciiFramesBuffer = []
    while True:

        success, frame = capture.read()
        print(type(frame), frame)

        if success:
            cv2.imwrite(f'temp/{frameNr}.jpg', frame)
        else:
            break
        wholeFrame = ""
        for ascii_rowns in imageToAscii.convert_Image_To_Ascii(f'temp/{frameNr}.jpg',
                                                               (round(96), round(72))):
            wholeFrame += "\n" + ascii_rowns  # splitting lines onto next lines
        asciiFramesBuffer.append(wholeFrame)
        os.remove(f'temp/{frameNr}.jpg')
    capture.release()
    videoObject.frames = asciiFramesBuffer
    makeJsonGzip(videoObject)
    return asciiFramesBuffer


def makeJsonGzip(videoObjectToWrite):
    vidJsonObject = {
        'path': videoObjectToWrite.path,
        'filename': videoObjectToWrite.filename,
        'totalFrames': videoObjectToWrite.frames,
        'fps': videoObjectToWrite.fps,
        'renderChars': videoObjectToWrite.renderChars,
        'renderTextWidth': videoObjectToWrite.renderTextWidth,
        'renderTextHeight': videoObjectToWrite.renderTextHeight
    }

    # creating a file at same destination and same with a different extension
    videoFilePath = videoObjectToWrite.path
    base = os.path.splitext(videoFilePath)[0]
    compress_json.dump(vidJsonObject, base + '.json.gz')
