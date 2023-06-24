import shutil
import time
import cv2
import os
from natsort import natsort
import VideoToAsciiJsonGzip
from videoObject import VideoObject
from concurrent.futures import ThreadPoolExecutor
import ImageToAscii

widthX = 150
heightY = 100
videoObjectx = VideoObject('BadAppleForPython2.mp4', widthX, heightY)

video1 = cv2.VideoCapture('BadAppleForPython2.mp4')
frames1 = video1.get(cv2.CAP_PROP_FRAME_COUNT)
print(frames1)

frameCount = 0

renderedFrames = []
initTime = time.time()
numberOfThreads = 64
submittedThreads = []
print(submittedThreads)


def splitFramesList(framesList, number_of_parts_to_split_in=1):
    length = len(framesList)
    return [framesList[i * length // number_of_parts_to_split_in: (i + 1) * length // number_of_parts_to_split_in]
            for i in range(number_of_parts_to_split_in)]


def renderFramesToAscii(submittedFrames, renderTextWidth, renderTextHeight):
    print(submittedFrames)
    asciiFramesBuffer = []
    for frame in submittedFrames:
        print('current frame', frame)

        wholeFrame = ""
        for ascii_rowns in ImageToAscii.convert_Image_To_Ascii(f'temp/' + frame,
                                                               (round(renderTextWidth),
                                                                round(renderTextHeight))):
            wholeFrame += "\n" + ascii_rowns  # splitting lines onto next lines
        asciiFramesBuffer.append(wholeFrame)
        os.remove(f'temp/' + frame)
    return asciiFramesBuffer


def splitVideoIntoFrames(videoObject):
    print("Splitting Frames")
    # recreating temp directory to clear everything from last session
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')
    capture = cv2.VideoCapture(videoObject.path)
    frameNr = 0
    while True:
        success, frame = capture.read()
        print(type(frame), frame)
        if success:
            cv2.imwrite(f'temp/{frameNr}.jpg', frame)

        else:
            break
        frameNr = frameNr + 1
    capture.release()
    print("frames split")


splitVideoIntoFrames(videoObjectx)

threadPool = ThreadPoolExecutor(numberOfThreads)
tempFrames = os.listdir("temp")
tempFrames = natsort.natsorted(tempFrames, reverse=False)

frameChunks = splitFramesList(tempFrames, numberOfThreads)

x = 0
while x < len(frameChunks):
    submittedThreads.append(

        threadPool.submit(renderFramesToAscii, frameChunks[x], videoObjectx.renderTextWidth,
                          videoObjectx.renderTextHeight))
    x += 1

print(submittedThreads)

for x in submittedThreads:
    renderedFrames.extend(x.result())

print(len(renderedFrames))
videoObjectx.frames = renderedFrames
VideoToAsciiJsonGzip.makeJsonGzip(videoObjectx)

print(time.time() - initTime, 'seconds taken')

print("done!")
