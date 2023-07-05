import base64
import os
import sys
from math import floor

import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display, K_ESCAPE, K_F11

import ptext

pygame.init()
pygame.font.init()

background_colour = (30, 30, 30)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE, vsync=1)
screen.fill(background_colour)

pygame.display.set_caption('ASCII Nova')
pygame.display.flip()

fps_count_render_font = pygame.font.Font('./fonts/courier.ttf', 16)
media_controls_render_font = pygame.font.Font('./fonts/courier.ttf', 12)

clock = pygame.time.Clock()


def initializeMediaControls(asciiVideoDict):
    try:
        file = open("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3', 'wb')
        file.write(base64.b64decode(asciiVideoDict['base64Audio']))
        file.close()
    except Exception as e:
        print(e)
        sys.exit(0)

    pygame.mixer.music.load("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1.0)


# incorporated this into renderOverlay:
# def show_fps(showFpsSwitch=True):
#     if showFpsSwitch is True:
#         fps_text = str(int(clock.get_fps()))
#         fps_surface = fps_count_render_font.render('', showFpsSwitch, (255, 255, 255))
#         fps_surface.fill(background_colour)
#         fps_surface = fps_count_render_font.render(('fps: ' + fps_text), showFpsSwitch, (255, 255, 255))
#         screen.blit(fps_surface, fps_surface.get_rect())

# def showMediaControls():
#     media_controls_surface = media_controls_render_font.render(
#         'J - FastBackward(10s)     L - FastForward(10s)   K - Pause/Unpause   M - Mute/Unmute   R - Replay', True,
#         (255, 255, 255))
#     screen.blit(media_controls_surface, (screen.get_rect().left, 12.5))


def render_overlay(show_fps_switch=True):
    if not fullScreen:
        if show_fps_switch:
            overlay_surface = pygame.Surface((700, 40))
        else:
            overlay_surface = pygame.Surface((700, 20))
    else:
        if show_fps_switch:
            overlay_surface = pygame.Surface((870, 40))
        else:
            overlay_surface = pygame.Surface((870, 20))

    overlay_surface.set_alpha(200)
    overlay_surface.set_colorkey((0, 0, 0))  # Set the background color of the overlay as transparent
    pygame.draw.rect(overlay_surface, (30, 30, 20), overlay_surface.get_rect(),
                     border_radius=8)  # Set the color and border radius

    if not fullScreen:
        media_controls_text = 'J - FastBackward(10s)     L - FastForward(10s)   K - Pause/Unpause   M - Mute/Unmute   R - Replay'
    else:
        media_controls_text = 'J - FastBackward(10s)     L - FastForward(10s)   K - Pause/Unpause   M - Mute/Unmute   R - Replay    Esc - Exit Full screen'
    media_controls_surface = media_controls_render_font.render(media_controls_text, True, (255, 255, 255))
    overlay_surface.blit(media_controls_surface, (5, 5))  # Customize the position of the media controls text

    if show_fps_switch:
        fps_text = str(int(clock.get_fps()))
        fps_surface = fps_count_render_font.render('fps: ' + fps_text, True, (255, 255, 255))
        overlay_surface.blit(fps_surface, (5, 20))  # Customize the position of the FPS text

    screen.blit(overlay_surface,
                (screen.get_rect().left + 10, 10))  # Customize the position of the overlay surface on the screen


#
# pygame.mixer.music.unload()

# Track double-click event
last_click_time = 0
double_click_interval = 400  # milliseconds
fullScreen = False


def renderFramesOnScreen(asciiVideoDict, fontColorHex="#FFFFFF", fontSize=14, lineheight=1, showFpsSwitch=True,
                         ascii_render_font_name="fonts/courier.ttf"):
    music_length = pygame.mixer.Sound("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3').get_length()
    print(music_length)
    FPS_LOCK_VALUE = asciiVideoDict['fps']
    frameIndex = 0

    initializeMediaControls(asciiVideoDict)
    global screen, fullScreen, last_click_time, double_click_interval, SCREEN_WIDTH, SCREEN_HEIGHT
    running = True
    playback_paused = False
    try:
        # game loop
        while running:
            if playback_paused is True:
                pass
            elif playback_paused is False:
                screen.fill(background_colour)  # filling background on resize/refresh
                if frameIndex < len(asciiVideoDict['AsciiFrames']):
                    frameIndex += 1

            screen.fill(background_colour)  # filling background on resize/refresh

            if frameIndex < len(asciiVideoDict['AsciiFrames']):
                ptext.draw_in_exact_center(asciiVideoDict['AsciiFrames'][frameIndex], screen, 0, 10, (500, 100),
                                           fontname=ascii_render_font_name,
                                           fontsize=fontSize,
                                           lineheight=lineheight, width=10, color=fontColorHex)

            clock.tick(FPS_LOCK_VALUE)  # making fps constant(synced to original video's fps)
            render_overlay(showFpsSwitch)

            display.flip()  # to update display

            # keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                # Check for media control key events
                pygame.event.pump()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # mute/unmute
                        print("M pressed")
                        print(pygame.mixer.music.get_volume())
                        if pygame.mixer.music.get_volume() == 0.0:
                            pygame.mixer.music.set_volume(1.0)
                            print('Unmuted')
                        elif pygame.mixer.music.get_volume() == 1.0:
                            pygame.mixer.music.set_volume(0.0)
                            print('Muted')
                    if event.key == pygame.K_j:  # fast-backward
                        frameIndex = frameIndex - int(FPS_LOCK_VALUE) * 10
                        newPos = floor(frameIndex / FPS_LOCK_VALUE) - 10
                        print("back by: ", newPos)
                        if frameIndex < 0:
                            newPos = 0
                            pygame.mixer.music.set_pos(newPos)
                            frameIndex = 0
                        else:
                            pygame.mixer.music.set_pos(newPos)
                        print("Fast Backwarded 10s")
                        print('J')
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
                    if event.key == pygame.K_l:  # fast-forward
                        frameIndex = frameIndex + int(FPS_LOCK_VALUE) * 10
                        newPos = floor(frameIndex / FPS_LOCK_VALUE) + 10
                        print("forward by: ", newPos)
                        if frameIndex > len(asciiVideoDict['AsciiFrames']):
                            pygame.mixer.music.unload()
                            frameIndex = len(asciiVideoDict['AsciiFrames'])
                        else:
                            pygame.mixer.music.set_pos(newPos)

                        print("Fast Forwarded 10s")
                        print('L')
                    if event.key == pygame.K_r:  # replay
                        frameIndex = 0
                        pygame.mixer.music.set_pos(0)
                        print('Replayed')

                    # resize screen on key events
                    if event.key == K_ESCAPE and fullScreen:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                         HWSURFACE | DOUBLEBUF | RESIZABLE, vsync=1)
                        fullScreen = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # resize screen on key events
                    if event.button == 1:
                        print("click registered")
                        if pygame.time.get_ticks() - last_click_time < double_click_interval:
                            if not fullScreen:
                                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,
                                                                 HWSURFACE | DOUBLEBUF | RESIZABLE, vsync=1)
                                fullScreen = True
                        last_click_time = pygame.time.get_ticks()
                # Check for QUIT event
                if event.type == QUIT:
                    display.quit()
            if frameIndex >= len(asciiVideoDict['AsciiFrames']):
                break
    except pygame.error as e:
        if e.args[0] == 'video system not initialized':
            print("Error: Video system not initialized")
            sys.exit(0)
        elif e.args[0] == 'display Surface quit':
            print("Error: Display windows was quit")
            sys.exit(0)
    finally:
        pygame.mixer.music.unload()
        os.remove("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3')
