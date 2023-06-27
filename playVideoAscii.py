import base64
import sys

import compress_json
import time
import pygame
import RenderScreen


def renderAudio():
    # f = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'rb')
    b = base64.b64decode(asciiVideoDict['base64Audio'])
    # f.close()

    try:
        file = open("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3', 'wb')
        file.write(b)
        file.close()
    except Exception as e:
        print(e)
        sys.exit(0)


gzippedJsonfile_path = "BadAppleForPython2.json.gz"  # change to your own video path
asciiVideoDict = compress_json.load(gzippedJsonfile_path)  # loads json as a dictionary

FPS_LOCK_VALUE = asciiVideoDict['fps']
clock = pygame.time.Clock()
initial_time = time.time()
asciiFramesBuffer = []
i = 0
print(len(asciiVideoDict['base64Audio']))
renderAudio()
RenderScreen.renderFramesOnScreen(asciiVideoDict, "#FFFF00", 8, showFpsSwitch=True)
final_time = time.time()
