import shutil
import cv2
import sys
import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display, K_ESCAPE

from RendererAndPlayer import ptext
from RendererAndPlayer import ImageToAscii
from RendererAndPlayer.VideoObject import VideoObject
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
lineHeight = 1
showFpsSwitch = True
ascii_render_font_name = "./fonts/courier.ttf"
ascii_Chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
renderTextWidth = 120
videoPath = ""


######################
def RTplayVideoAscii():
    videoToRenderInAscii = VideoObject(videoPath)
    print(videoToRenderInAscii.path)
    pygame.init()
    print("Init")
    renderFrames(videoToRenderInAscii)


# Track double-click event
last_click_time = 0
double_click_interval = 400  # milliseconds
fullScreen = False


def renderFrames(videoObject):
    print("Splitting Frames")
    # recreating temp directory to clear everything from last session
    if os.path.exists('../temp'):
        shutil.rmtree('../temp')
    os.mkdir('../temp')
    capture = cv2.VideoCapture(videoObject.path)
    frameNr = 0

    global fontColorHex, playback_paused, fontSize, lineHeight, showFpsSwitch, ascii_render_font_name
    global screen, fullScreen, last_click_time, double_click_interval, SCREEN_WIDTH, SCREEN_HEIGHT
    try:
        while True:

            if playback_paused is False:
                success, frame = capture.read()
                # print(type(frame), frame)
                if success:
                    cv2.imwrite(f'../temp/{frameNr}.jpg', frame)
                    frame = ImageToAscii.convert_Image_To_Ascii(f'../temp/{frameNr}.jpg', renderTextWidth,
                                                                ASCII_CHARS=ascii_Chars)
                    renderFrameOnScreen(frame, videoObject.fps, fontColorHex, fontSize, lineHeight, showFpsSwitch,
                                        ascii_render_font_name)
                    os.remove(f'../temp/{frameNr}.jpg')
                else:
                    break

                frameNr = frameNr + 1

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
                        # resize screen on key events
                    if event.key == K_ESCAPE and fullScreen:
                        pygame.display.quit()
                        pygame.init()
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE,
                                                         HWSURFACE | DOUBLEBUF | RESIZABLE, vsync=1)
                        fullScreen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # resize screen on key events
                    if event.button == 1:
                        print("click registered")
                        if pygame.time.get_ticks() - last_click_time < double_click_interval:
                            if not fullScreen:
                                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,
                                                                 HWSURFACE | DOUBLEBUF, vsync=1)
                                fullScreen = True
                        last_click_time = pygame.time.get_ticks()

                        # Check for QUIT event

                # Check for QUIT event
                if event.type == QUIT:
                    pygame.display.quit()
                    return
    except pygame.error as e:
        if e.args[0] == 'video system not initialized':
            print("Error: Video system not initialized")
            sys.exit(0)
        elif e.args[0] == 'display Surface quit':
            print("Error: Display windows was quit")
            sys.exit(0)
    finally:
        capture.release()
        return


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

    if not fullScreen:
        if show_fps_switch:
            overlay_surface = pygame.Surface((140, 40))
        else:
            overlay_surface = pygame.Surface((140, 20))
    else:
        if show_fps_switch:
            overlay_surface = pygame.Surface((300, 40))
        else:
            overlay_surface = pygame.Surface((300, 20))

    overlay_surface.set_colorkey((0, 0, 0))  # Set the background color of the overlay as transparent
    pygame.draw.rect(overlay_surface, (30, 30, 20), overlay_surface.get_rect(),
                     border_radius=6)  # Set the color and border radius

    if not fullScreen:
        media_controls_text = 'K - Pause/Unpause'
    else:
        media_controls_text = 'K - Pause/Unpause    Esc - Exit Full screen'
    media_controls_surface = media_controls_render_font.render(media_controls_text, True, (255, 255, 255))
    overlay_surface.blit(media_controls_surface, (5, 5))  # Customize the position of the media controls text

    if show_fps_switch:
        fps_text = str(int(clock.get_fps()))
        fps_surface = fps_count_render_font.render('fps: ' + fps_text, True, (255, 255, 255))
        overlay_surface.blit(fps_surface, (5, 20))  # Customize the position of the FPS text

    screen.blit(overlay_surface, (screen.get_rect().left + 10, 10))


def renderFrameOnScreen(asciiFrameString, fpsLockValue=30, fontColorHex="#FFFFFF", fontSize=14, lineheight=1,
                        showFpsSwitch=True,
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
    except pygame.error as e:
        if e.args[0] == 'display Surface quit':
            print("Error: Display windows was quit")
            sys.exit(0)
