import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import cv2
from natsort import natsort
import ImageToAscii
import compress_json


def renderVideoToAsciiJson(videoObject):
    renderedFrames = []
    numberOfThreads = 64
    submittedThreads = []

    splitVideoIntoFrames(videoObject)

    threadPool = ThreadPoolExecutor(numberOfThreads)
    tempFrames = os.listdir("temp")
    tempFrames = natsort.natsorted(tempFrames, reverse=False)

    frameChunks = splitFramesList(tempFrames, numberOfThreads)

    x = 0
    while x < len(frameChunks):
        submittedThreads.append(

            threadPool.submit(renderFramesToAscii, frameChunks[x], videoObject.renderTextWidth,
                              videoObject.renderTextHeight))
        x += 1

    print(submittedThreads)

    for x in submittedThreads:
        renderedFrames.extend(x.result())

    print(len(renderedFrames))
    videoObject.frames = renderedFrames
    makeJsonGzip(videoObject)


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


def splitFramesList(framesList, number_of_parts_to_split_in=1):
    length = len(framesList)
    return [framesList[i * length // number_of_parts_to_split_in: (i + 1) * length // number_of_parts_to_split_in]
            for i in range(number_of_parts_to_split_in)]


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
