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
lane_width = 100
starting_lane = max_number_of_lanes // 2
speed = 6

#functions
def generateLaneX(number_of_lane):
    return lane_width * number_of_lane

#Surfaces
laneSurface = pygame.Surface((lane_width*max_number_of_lanes, screen_height))

#Classes
class Lane:

    def __init__(self,number_of_lane, color, x):
        self.number_of_lane = number_of_lane
        self.color = color
        self.x = x

    def draw(self):
        pygame.draw.rect(laneSurface, self.color, (self.x, 0 , lane_width, screen_height))

class Player:
    def __init__(self, image_path, desired_height):
        self.image = pygame.image.load(image_path)
        self.desired_height = desired_height
        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.desired_width = int(self.desired_height * self.aspect_ratio)
        self.image = pygame.transform.scale(self.image, (self.desired_width, self.desired_height))

    def render(self, screen, x, y, rotation):
        screen.blit(pygame.transform.rotate(self.image, rotation), (x, y))



# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lanes")


#Background
texture_image = pygame.image.load("./assets/texture.png")
texture_image = pygame.transform.scale(texture_image, (screen_width, screen_height))

background = pygame.Surface(screen.get_size()).convert()
background.blit(texture_image, (0, 0))
background.set_alpha(50)

#Player
player_height = 100
player_image = pygame.image.load("./assets/red-car.png")
desired_height_player = 100
aspect_ratio_player = player_image.get_width() / player_image.get_height()
desired_width_player = int(desired_height_player * aspect_ratio_player)
player_image = pygame.transform.scale(player_image, (desired_width_player, desired_height_player))

#Player variables

player_rotation = 0

#Lanes
lane_width = 100
lane_colors = [
    (255, 77, 77),    # Red
    (255, 154, 77),   # Orange
    (255, 220, 77),   # Yellow
    (102, 255, 102),  # Green
    (77, 166, 255),   # Blue
    (143, 77, 255),   # Indigo
    (217, 77, 255)    # Violet
]

lanes = []

for i in range(max_number_of_lanes):
    x_position = generateLaneX(i)
    lane = Lane(i, lane_colors[i % len(lane_colors)], x_position)
    lanes.append(lane)

# Game loop
player = Player("./assets/red-car.png", 100)
clock = pygame.time.Clock()
running = True

for lane in lanes:
    lane.draw()

laneSurfaceX = lane_width // 2

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        laneSurfaceX += speed
        player_rotation = 15
    if keys[pygame.K_RIGHT]:
        laneSurfaceX -= speed
        player_rotation = -15
    else:
        player_rotation = 0

    # Drawing on the screen
    screen.fill(WHITE)
    #screen.blit(background, (0, 0))
    screen.blit(laneSurface, (laneSurfaceX, 0))
    screen.blit(background, (0, 0))
    player.render(screen, screen_width // 2 - lane_width // 2, screen_height // 2 - lane_width // 2, player_rotation)

    # Update the screen
    pygame.display.flip()
    clock.tick(60)


# Quit the game
pygame.quit()
