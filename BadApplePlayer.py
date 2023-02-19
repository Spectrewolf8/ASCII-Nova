import glob
import natsort
import time

import ImageToAscii as imageToAscii
import pyperclip
import os

os.system("xhost +")
import pyautogui

print("Starting in 3")
time.sleep(3)
frames = os.listdir("FramesToConvertToAscii")
# frames = sorted(filter(os.path.isfile, glob.glob("FramesToConvertToAscii/"+"*")))
# frames.sort(key=lambda f: int(filter(str.isdigit, f)))
frames = natsort.natsorted(frames, reverse=False)
print(frames)
# print(y)
# print(imageToAscii.convertImageToAscii(("FramesToConvertToAscii/" + "frame_500.jpg"), "hh"))
initial_time = time.time()
for frame in frames:
    wholeFrame = ""
    for ascii_rowns in imageToAscii.convertImageToAscii(("FramesToConvertToAscii/" + frame), "Test.txt"):
        wholeFrame += "\n" + ascii_rowns

    #time.sleep(1 / 14)
    # pyperclip.copy(wholeFrame)
    # pyautogui.hotkey('ctrl', 'v')
    # pyautogui.press('enter')

    print(wholeFrame)

final_time = time.time()

print("\n\n\n FPS :", end="")
print(len(frames) / (final_time - initial_time))
print("Total frames played :", len(frames), "in", (final_time - initial_time))
