import base64
import os
import shutil
import sys
from math import floor

import cv2
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
        fps_surface = fps_count_render_font.render('', showFpsSwitch, (255, 255, 255))
        fps_surface.fill(background_colour)
        fps_surface = fps_count_render_font.render(('fps: ' + fps_text), showFpsSwitch, (255, 255, 255))
        screen.blit(fps_surface, fps_surface.get_rect())


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

    # pygame.mixer.music.set_pos(30)
    # i = 0
    # while i <= 50000000:
    #     print(i)
    #     if 300000 < i < 4000000:
    #         pygame.mixer.music.pause()
    #     else:
    #         pygame.mixer.music.unpause()
    #     i += 1
    # pygame.mixer.music.stop()


def showMediaControls():
    media_controls_surface = media_controls_render_font.render(
        'J - FastBackward(10s)     L - FastForward(10s)   K - Pause/Unpause   M - Mute/Unmute   R - Replay', True,
        (255, 255, 255))
    screen.blit(media_controls_surface, (screen.get_rect().left, 12.5))


#
# pygame.mixer.music.unload()


def renderFramesOnScreen(asciiVideoDict, showFpsSwitch=True, ascii_render_font_name="fonts/courier.ttf"):
    music_length = pygame.mixer.Sound("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3').get_length()
    print(music_length)
    FPS_LOCK_VALUE = asciiVideoDict['fps']
    frameIndex = 0

    initializeMediaControls(asciiVideoDict)

    running = True
    playback_paused = False
    # game loop
    try:
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
                                           fontsize=14,
                                           lineheight=1, width=10, color=(255, 255, 255))

            clock.tick(FPS_LOCK_VALUE)  # making fps constant(synced to original video's fps)
            show_fps(showFpsSwitch)  # to display fps in top left
            showMediaControls()

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
                    if event.key == pygame.K_j:  # fast backward
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
                    if event.key == pygame.K_l:
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
                        if event.key == pygame.K_r:  # mute/unmute
                            frameIndex = 0
                            pygame.mixer.music.set_pos(0)
                            print('Replayed')
                # Check for QUIT event
                if event.type == QUIT:
                    display.quit()
            if frameIndex >= len(asciiVideoDict['AsciiFrames']):
                break
    except pygame.error as e:
        print(e)
        sys.exit(0)
    finally:
        os.remove("temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3')


def splitVideoIntoFrames(videoObject):
    print("Splitting Frames")
    # recreating temp directory to clear everything from last session
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')
    capture = cv2.VideoCapture(videoObject.path)
    frameNr = 0
    while True:
        success, frame = capture.read()
        print(type(frame), frame)
        if success:
            cv2.imwrite(f'temp/{frameNr}.jpg', frame)

        else:
            break
        frameNr = frameNr + 1
    capture.release()
    print("frames split")
