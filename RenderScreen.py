import pygame
from pygame import DOUBLEBUF, RESIZABLE, HWSURFACE, QUIT, VIDEORESIZE

background_colour = (30, 30, 30)

# screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE, vsync=1)
screen = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('BadApplePlayer')
screen.fill(background_colour)

pygame.display.flip()

running = True

# game loop
while running:
    screen.fill(background_colour)
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == QUIT:
            pygame.display.quit()
        elif event.type == VIDEORESIZE:
            pygame.display.flip()
