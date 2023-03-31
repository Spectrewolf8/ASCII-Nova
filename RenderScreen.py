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

fps_count_render_font = pygame.font.Font('fonts/courier.ttf', 20)

clock = pygame.time.Clock()


def show_fps(showFpsSwitch=True):
    fps_text = str(int(clock.get_fps()))
    fps_surface = fps_count_render_font.render(('fps: ' + fps_text), showFpsSwitch, (255, 255, 255))
    screen.blit(fps_surface, fps_surface.get_rect())


def renderFramesOnScreen(asciiVideoJson, showFpsSwitch=True, ascii_render_font_name="fonts/courier.ttf"):
    FPS_LOCK_VALUE = asciiVideoJson['fps']
    i = 0

    running = True
    # game loop
    while running:

        screen.fill(background_colour)  # filling background on resize
        # textToRender = ascii_render_font.render(str(message), True, (255, 255, 255))
        # screen.blit(textToRender, textToRender.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        if i < len(asciiVideoJson['totalFrames']):
            ptext.draw_in_exact_center(asciiVideoJson['totalFrames'][i], screen, (500, 100),
                                       fontname=ascii_render_font_name,
                                       fontsize=14,
                                       lineheight=1, width=10, color=(255, 255, 255))

        i += 1
        clock.tick(FPS_LOCK_VALUE)  # making fps constant 30
        show_fps(showFpsSwitch)  # to display fps in top left
        display.flip()  # to update display

        for event in pygame.event.get():
            # Check for QUIT event
            if event.type == QUIT:
                display.quit()

