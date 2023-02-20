import natsort
import time
import ImageToAscii as imageToAscii
import os
import cv2

file_path = "BadAppleForPython.mp4"  # change to your own video path
vid = cv2.VideoCapture(file_path)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
print("Starting in 3")
time.sleep(3)
frames = os.listdir("FramesToConvertToAscii")
frames = natsort.natsorted(frames, reverse=False)
print(frames)

initial_time = time.time()
asciiFramesBuffer = []

for frame in frames:
    wholeFrame = ""
    for ascii_rowns in imageToAscii.convert_Image_To_Ascii(("FramesToConvertToAscii/" + frame),
                                                           (round(48), round(36))):
        wholeFrame += "\n" + ascii_rowns
    asciiFramesBuffer.append(wholeFrame)

    print(wholeFrame)
    print('Generated ' + str(frames.index(frame)) + "th frame")

final_time = time.time()

# print(asciiFramesBuffer)
print("\n\n\n FPS :", end="")
print(len(frames) / (final_time - initial_time))
print("Total frames generated :", len(frames), "in", (final_time - initial_time))
