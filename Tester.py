import base64
import sys

import moviepy.editor as mvEditor
import pygame

video = mvEditor.VideoFileClip(r"BadAppleForPython2.mp4")
video.audio.write_audiofile("temp/" + r"BadAppleForPython2_audio.mp3")

with open("temp/" + "BadAppleForPython2_audio.mp3", 'rb') as f:
   b = base64.b64encode(f.read())
print(sys.getsizeof(b))
f.close()

try:
   file = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'wb')
   file.write(b)
   file.close()
except Exception as e:
   print(e)
   sys.exit(0)

f = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'rb')
b = base64.b64decode(f.read())
f.close()

try:
   file = open("temp/" + "BadAppleForPython2_audio_decoded" + '.mp3', 'wb')
   file.write(b)
   file.close()
except Exception as e:
   print(e)
   sys.exit(0)


