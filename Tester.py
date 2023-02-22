import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display

import natsort
import time
import ImageToAscii as imageToAscii
import os
import cv2
import ptext  # https://github.com/cosmologicon/pygame-text

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.font.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

background_colour = (30, 30, 30)
text_colour = (255, 255, 255)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('BadApplePlayer')
screen.fill(background_colour)
pygame.display.flip()
ascii_render_font = pygame.font.Font('courier.ttf', 12)
fps_count_render_font = pygame.font.Font('courier.ttf', 20)
center_of_screen = screen.get_rect().center

# myfont = pygame.font.SysFont('Courier Prime Regular', 32, bold=False, italic=False)

running = True

clock = pygame.time.Clock()

FPS_LOCK_VALUE = 30


def show_fps():
    fps_text = str(int(clock.get_fps()))
    fps_surface = fps_count_render_font.render(('fps: ' + fps_text), True, (255, 255, 255))
    screen.blit(fps_surface, fps_surface.get_rect())


file_path = "BadAppleForPython.mp4"  # change to your own video path
vid = cv2.VideoCapture(file_path)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
print("Starting in 2 seconds")
time.sleep(2)
frames = os.listdir("FramesToConvertToAscii")
frames = natsort.natsorted(frames, reverse=False)
print(frames)

initial_time = time.time()
asciiFramesBuffer = []

ptext.draw("hello world", centery=50, right=300)


def mainloop():
    i = 0
    # game loop
    while running:

        screen.fill(background_colour)  # filling background on resize
        # textToRender = ascii_render_font.render(str(message), True, (255, 255, 255))
        # screen.blit(textToRender, textToRender.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        wholeFrame = ""
        for ascii_rowns in imageToAscii.convert_Image_To_Ascii(("FramesToConvertToAscii/" + frames[i]),
                                                               (round(110), round(80))):
            wholeFrame += "\n" + ascii_rowns
        asciiFramesBuffer.append(wholeFrame)
        message2 = wholeFrame

        ptext.draw(wholeFrame, (500, 100), fontname="courier.ttf", fontsize=12,
                   lineheight=0.7, color=text_colour)
        # print_multiline_text(screen, message2, (0, 10), ascii_render_font)
        print(wholeFrame)
        print("frame#", i)
        clock.tick(FPS_LOCK_VALUE)  # making fps constant 30
        show_fps()  # to display fps in top left
        display.flip()  # to update display

        if i >= len(frames):
            break
        i += 1
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == QUIT:
                display.quit()


mainloop()
