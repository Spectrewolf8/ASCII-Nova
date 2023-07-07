# import base64
# import sys
#
# import moviepy.editor as mvEditor
# import pygame
#
# video = mvEditor.VideoFileClip(r"BadAppleForPython2.mp4")
# video.audio.write_audiofile("temp/" + r"BadAppleForPython2.mp4_audio_decoded.mp3")
#
# with open("temp/" + "BadAppleForPython2.mp4_audio_decoded.mp3", 'rb') as f:
#     b = base64.b64encode(f.read())
# print(sys.getsizeof(b))
# f.close()
#
# try:
#     file = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'wb')
#     file.write(b)
#     file.close()
# except Exception as e:
#     print(e)
#     sys.exit(0)
#
# f = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'rb')
# b = base64.b64decode(f.read())
# f.close()
#
# try:
#     file = open("temp/" + "BadAppleForPython2_audio_decoded" + '.mp3', 'wb')
#     file.write(b)
#     file.close()
# except Exception as e:
#     print(e)
#     sys.exit(0)
# from ImageToAscii import convert_Image_To_Ascii
#
# print(convert_Image_To_Ascii("temp/500.jpg", ASCII_CHARS=None))
import RendererAndPlayer.RTplayVideoAscii as RTplayVideoAscii
RTplayVideoAscii.videoPath=f"./RendererAndPlayer/BadAppleForPython2.mp4"
RTplayVideoAscii.RTplayVideoAscii()

# from tkinter import Tk     # from tkinter import Tk for Python 3.x
# from tkinter.filedialog import askopenfilename
#
# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)

# import easygui
#
# filepath = easygui.fileopenbox("Choose a json.gz file to play", "ASCII Nova",
#                                filetypes=["*.json.gz"], default="*.json.gz", multiple=False)
# print(filepath)

stringo = "@  f                 "
# x = 1
# while x < len(stringo):
#     if stringo[x] == " ":
#         pass
#     else:
#         print("incorrect format")
#         break
#     x += 2

