import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

#constants
screen_width = 800
screen_height = 600
white_hex = '#ffffff'
WHITE = pygame.Color(white_hex)

#Game variables
max_number_of_lanes = 10
lane_width = screen_width / 3

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lanes")


#Background
texture_image = pygame.image.load("./assets/texture.png")
texture_image = pygame.transform.scale(texture_image, (screen_width, screen_height))
texture_image.set_alpha(50)

background = pygame.Surface(screen.get_size()).convert()
background.blit(texture_image, (0, 0))

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    
    # Drawing on the screen
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
