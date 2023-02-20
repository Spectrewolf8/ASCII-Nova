import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, VIDEORESIZE, display

pygame.init()
pygame.font.init()

background_colour = (30, 30, 30)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('BadApplePlayer')
screen.fill(background_colour)
pygame.display.flip()
myfont = pygame.font.Font('courier.ttf', 32)
# myfont = pygame.font.SysFont('Courier Prime Regular', 32, bold=False, italic=False)

running = True

clock = pygame.time.Clock()


def show_fps():
    fps_text = str(int(clock.get_fps()))
    fps_surface = myfont.render(fps_text, True, (255, 255, 255))
    screen.blit(fps_surface, fps_surface.get_rect())


def mainloop():
    i = 0
    # game loop
    while running:
        i += 1
        screen.fill(background_colour)  # filling background on resize
        textToRender = myfont.render(str(i), True, (255, 255, 255))
        screen.blit(textToRender, textToRender.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        clock.tick(30)  # making fps constant 30
        show_fps()  # to display fps in top left
        display.flip()  # to update display
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == QUIT:
                display.quit()


mainloop()
