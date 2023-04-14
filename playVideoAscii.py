import compress_json
import time
import pygame
import RenderScreen

gzippedJsonfile_path = "BadAppleForPython2.json.gz"  # change to your own video path
asciiVideoDict = compress_json.load(gzippedJsonfile_path) # loads json as a dictionary

FPS_LOCK_VALUE = asciiVideoDict['fps']
clock = pygame.time.Clock()
initial_time = time.time()
asciiFramesBuffer = []
i = 0
print(len(asciiVideoDict['base64Audio']))
RenderScreen.renderFramesOnScreen(asciiVideoDict, showFpsSwitch=True)
final_time = time.time()

# print(asciiFramesBuffer)
print("\n\n\n FPS :", end="")
print(i / (final_time - initial_time))
print("Total frames generated :", i, "in", (final_time - initial_time))
