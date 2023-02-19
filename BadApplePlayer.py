import time

import ImageToAscii as imageToAscii
import pyperclip
import os

os.system("xhost +")
import pyautogui

print("Starting in 3")
time.sleep(3)
frameFolder = os.listdir("FramesToConvertToAscii")
print(frameFolder)

# print(y)
print(imageToAscii.convertImageToAscii(("FramesToConvertToAscii/" + "frame_500.jpg"), "hh"))
for frame in frameFolder:
    wholeFrame = ""
    for ascii_rowns in imageToAscii.convertImageToAscii(("FramesToConvertToAscii/" + frame), "Test.txt"):
        wholeFrame += "\n" + ascii_rowns

    pyperclip.copy(wholeFrame)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
