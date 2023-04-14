import base64
import sys

import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display
import ptext

pygame.init()
pygame.font.init()

background_colour = (30, 30, 30)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
screen.fill(background_colour)

pygame.display.set_caption('ASCII Nova')
pygame.display.flip()

fps_count_render_font = pygame.font.Font('fonts/courier.ttf', 16)
media_controls_render_font = pygame.font.Font('fonts/courier.ttf', 12)

clock = pygame.time.Clock()


def show_fps(showFpsSwitch=True):
    if showFpsSwitch is True:
        fps_text = str(int(clock.get_fps()))
        fps_surface = fps_count_render_font.render(('fps: ' + fps_text), showFpsSwitch, (255, 255, 255))
        screen.blit(fps_surface, fps_surface.get_rect())


def initializeMediaControls(asciiVideoDict):
    file = open("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3', 'wb')
    file.write(base64.b64decode(asciiVideoDict['base64Audio']))
    file.close()
    # try:
    #    file = open("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3', 'wb')
    #    file.write(bytes(asciiVideoDict['base64Audio']))
    #    file.close()
    # except Exception as e:
    #    print(e)
    #    sys.exit(0)

    pygame.mixer.music.load("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3')
    pygame.mixer.music.play()
    #pygame.mixer.music.set_pos(30)
    #pygame.mixer.music.set_volume(0.0)
    i = 0
    # while i <= 50000000:
    #     print(i)
    #     if 300000 < i < 4000000:
    #         pygame.mixer.music.pause()
    #     else:
    #         pygame.mixer.music.unpause()
    #     i += 1
    #pygame.mixer.music.stop()


def showMediaControls():
    media_controls_surface = media_controls_render_font.render(
        'J - FastBackward(10s)     L - FastForward(10s)   K - Pause/Unpause   M - Mute/Unmute', True,
        (255, 255, 255))
    screen.blit(media_controls_surface, (screen.get_rect().left, 12.5))


#
# pygame.mixer.music.unload()


def renderFramesOnScreen(asciiVideoDict, showFpsSwitch=True, ascii_render_font_name="fonts/courier.ttf"):
    FPS_LOCK_VALUE = asciiVideoDict['fps']
    i = 0

    initializeMediaControls(asciiVideoDict)

    running = True
    # game loop
    while running:

        screen.fill(background_colour)  # filling background on resize
        if i < len(asciiVideoDict['AsciiFrames']):
            ptext.draw_in_exact_center(asciiVideoDict['AsciiFrames'][i], screen, 0, 10, (500, 100),
                                       fontname=ascii_render_font_name,
                                       fontsize=14,
                                       lineheight=1, width=10, color=(255, 255, 255))

        i += 1
        clock.tick(FPS_LOCK_VALUE)  # making fps constant 30
        show_fps(showFpsSwitch)  # to display fps in top left
        showMediaControls()

        display.flip()  # to update display
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Check for QUIT event
            if event.type == QUIT:
                display.quit()
            # Check for media control key events
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.mod == pygame.KMOD_NONE:
                    print('No modifier keys were in a pressed state when this '
                          'event occurred.')
                else:
                    if event.mod & pygame.KMOD_LSHIFT:
                        print('Left shift was in a pressed state when this event '
                              'occurred.')
                    if event.mod & pygame.KMOD_RSHIFT:
                        print('Right shift was in a pressed state when this event '
                              'occurred.')
                    if event.mod & pygame.KMOD_SHIFT:
                        print('Left shift or right shift or both were in a '
                              'pressed state when this event occurred.')
