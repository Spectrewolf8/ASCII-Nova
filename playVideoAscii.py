import compress_json
import time
import pygame
import RenderScreen
gzippedJsonfile_path = "BadAppleForPython.json.gz"  # change to your own video path
asciiVideoJson = compress_json.load("BadAppleForPython.json.gz")

FPS_LOCK_VALUE = asciiVideoJson['fps']
clock = pygame.time.Clock()
initial_time = time.time()
asciiFramesBuffer = []
i = 0
RenderScreen.renderFramesOnScreen(asciiVideoJson)
final_time = time.time()

# print(asciiFramesBuffer)
print("\n\n\n FPS :", end="")
print(i / (final_time - initial_time))
print("Total frames generated :", i, "in", (final_time - initial_time))
