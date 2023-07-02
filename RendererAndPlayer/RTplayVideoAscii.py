import shutil
import cv2
import sys
import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display

import ImageToAscii
import ptext
from VideoObject import VideoObject
import os

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

fps_count_render_font = pygame.font.Font('../fonts/courier.ttf', 16)
media_controls_render_font = pygame.font.Font('../fonts/courier.ttf', 12)

clock = pygame.time.Clock()

playback_paused = False

fps_lock = 30

######################
fontColorHex = "#FFFFFF"
fontSize = 14
showFpsSwitch = True
ascii_render_font_name = "fonts/courier.ttf"
ascii_Chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']


######################
def RTplayVideoAscii(videoPath, renderWidth):
    videoToRenderInAscii = VideoObject(videoPath, renderWidth)
    renderFrames(videoToRenderInAscii)


def renderFrames(videoObject):
    print("Splitting Frames")
    # recreating temp directory to clear everything from last session
    if os.path.exists('../temp'):
        shutil.rmtree('../temp')
    os.mkdir('../temp')
    capture = cv2.VideoCapture(videoObject.path)
    frameNr = 0
    global fontColorHex, playback_paused
    global fontSize
    global showFpsSwitch
    global ascii_render_font_name
    while True:
        if playback_paused is False:
            success, frame = capture.read()
            print(type(frame), frame)
            if success:
                cv2.imwrite(f'temp/{frameNr}.jpg', frame)
                frame = ImageToAscii.convert_Image_To_Ascii(f'temp/{frameNr}.jpg', videoObject.renderTextWidth,
                                                            ASCII_CHARS=ascii_Chars)
                renderFrameOnScreen(frame, videoObject.fps, fontColorHex, fontSize, showFpsSwitch,
                                    ascii_render_font_name)
                os.remove(f'temp/{frameNr}.jpg')
            else:
                break
            frameNr = frameNr + 1
        try:
            # keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                # Check for media control key events
                pygame.event.pump()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:  # pause/upause
                        if playback_paused is False:
                            playback_paused = True
                            pygame.mixer.music.pause()
                            print("Paused")
                        elif playback_paused is True:
                            playback_paused = False
                            pygame.mixer.music.unpause()
                            print("UnPaused")
                        print('K')

                # Check for QUIT event
                if event.type == QUIT:
                    display.quit()
        except pygame.error as e:
            if e.args[0] == 'video system not initialized':
                print("Error: Video system not initialized")
                sys.exit(0)
    capture.release()
    print("frames split")


# incorporated in renderOverlay:
# def show_fps(showFpsSwitch=True):
#     if showFpsSwitch is True:
#         fps_text = str(int(clock.get_fps()))
#         fps_surface = fps_count_render_font.render('', showFpsSwitch, (255, 255, 255))
#         fps_surface.fill(background_colour)
#         fps_surface = fps_count_render_font.render(('fps: ' + fps_text), showFpsSwitch, (255, 255, 255))
#         screen.blit(fps_surface, fps_surface.get_rect())
#
#
# def showMediaControls():
#     media_controls_surface = media_controls_render_font.render(
#         'K - Pause/Unpause', True,
#         (255, 255, 255))
#     screen.blit(media_controls_surface, (screen.get_rect().left, 12.5))

def render_overlay(show_fps_switch=True):
    if show_fps_switch:
        overlay_surface = pygame.Surface((140, 40))
    else:
        overlay_surface = pygame.Surface((140, 20))

    overlay_surface.set_colorkey((0, 0, 0))  # Set the background color of the overlay as transparent
    pygame.draw.rect(overlay_surface, (30, 30, 20), overlay_surface.get_rect(),
                     border_radius=6)  # Set the color and border radius

    media_controls_text = 'K - Pause/Unpause'
    media_controls_surface = media_controls_render_font.render(media_controls_text, True, (255, 255, 255))
    overlay_surface.blit(media_controls_surface, (5, 5))  # Customize the position of the media controls text

    if show_fps_switch:
        fps_text = str(int(clock.get_fps()))
        fps_surface = fps_count_render_font.render('fps: ' + fps_text, True, (255, 255, 255))
        overlay_surface.blit(fps_surface, (5, 20))  # Customize the position of the FPS text

    screen.blit(overlay_surface, (screen.get_rect().left + 10, 10))


def renderFrameOnScreen(asciiFrameString, fpsLockValue=30, fontColorHex="#FFFFFF", fontSize=14, showFpsSwitch=True,
                        ascii_render_font_name="fonts/courier.ttf"):
    try:
        # game loop
        global playback_paused

        if playback_paused is True:
            pass
        elif playback_paused is False:
            screen.fill(background_colour)  # filling background on resize/refresh
            ptext.draw_in_exact_center(asciiFrameString, screen, 0, 10, (500, 100),
                                       fontname=ascii_render_font_name,
                                       fontsize=fontSize,
                                       lineheight=1, width=10, color=fontColorHex)

            clock.tick(fpsLockValue)  # making fps constant(synced to original video's fps)

            render_overlay(showFpsSwitch)

            display.flip()  # to update display

        # keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Check for media control key events
            pygame.event.pump()
            # Check for QUIT event
            if event.type == QUIT:
                display.quit()
    except pygame.error as e:
        if e.args[0] == 'display Surface quit':
            print("Error: Display windows was quit")
            sys.exit(0)
