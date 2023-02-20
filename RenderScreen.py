import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, display

pygame.init()
pygame.font.init()

background_colour = (30, 30, 30)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('BadApplePlayer')
screen.fill(background_colour)
pygame.display.flip()
ascii_render_font = pygame.font.Font('courier.ttf', 32)
fps_count_render_font = pygame.font.Font('courier.ttf', 20)

# myfont = pygame.font.SysFont('Courier Prime Regular', 32, bold=False, italic=False)

running = True

clock = pygame.time.Clock()

FPS_LOCK_VALUE = 500


def show_fps():
    fps_text = str(int(clock.get_fps()))
    fps_surface = fps_count_render_font.render(('fps: ' + fps_text), True, (255, 255, 255))
    screen.blit(fps_surface, fps_surface.get_rect())


def mainloop():
    i = 0
    # game loop
    while running:
        i += 1
        screen.fill(background_colour)  # filling background on resize
        textToRender = ascii_render_font.render(str(i), True, (255, 255, 255))
        screen.blit(textToRender, textToRender.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        clock.tick(FPS_LOCK_VALUE)  # making fps constant 30
        show_fps()  # to display fps in top left
        display.flip()  # to update display
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == QUIT:
                display.quit()


mainloop()
