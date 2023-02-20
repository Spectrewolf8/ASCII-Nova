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

running = True
i = 0
# game loop
while running:
    screen.fill(background_colour)
    textToRender = myfont.render(str(i), True, (255, 255, 255))
    i += 1
    screen.blit(textToRender, textToRender.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    display.flip()
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == QUIT:
            display.quit()
