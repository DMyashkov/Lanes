import pygame
from pygame.locals import *
import random
from moviepy.editor import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE_HEX = '#ffffff'
WHITE = pygame.Color(WHITE_HEX)

# Game variables
NUMBER_OF_LANES = 10
LANE_WIDTH = 100
STARTING_LANE = NUMBER_OF_LANES // 2

MIN_SPAWN_INTERVAL = 100
MAX_SPAWN_INTERVAL = 300
MIN_SPAWN_QUANTITY = 3
MAX_SPAWN_QUANTITY = 7

OBSTACLE_SIZE = 50

HITBOX_OFFSET = 20

HORIZONTAL_SPEED_CONST = 6
SPEED_CONST = 7

HORIZONTAL_SPEED = HORIZONTAL_SPEED_CONST
SPEED = SPEED_CONST

# Functions
def generate_lane_x(number_of_lane):
    return LANE_WIDTH * number_of_lane

# Surfaces
lane_surface = pygame.Surface((LANE_WIDTH * NUMBER_OF_LANES, SCREEN_HEIGHT))

lane_surface_width = lane_surface.get_width()
lane_surface_height = lane_surface.get_height()
game_surface = pygame.Surface((lane_surface_width, lane_surface_height))

test_surface = pygame.Surface((lane_surface_width, lane_surface_height))

# Classes
class Lane:
    def __init__(self, number_of_lane, color, x):
        self.number_of_lane = number_of_lane
        self.color = color
        self.x = x

    def draw(self):
        pygame.draw.rect(lane_surface, self.color, (self.x, 0, LANE_WIDTH, SCREEN_HEIGHT))

class Obstacle:
    def __init__(self, image_path, x, y, size):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.size = size

        self.rect = Rect(self.x, self.y, size, size)
        self.rect.center = (self.x + size // 2, self.y + size // 2)
        self.rect_color = pygame.Color(255, 0, 0)
    
    def update(self, speed):
        self.y += speed
        self.rect.center = (self.x + self.size // 2, self.y + self.size // 2)   

    def render(self, screen):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, image_path, desired_height):
        self.image = pygame.image.load(image_path)
        self.desired_height = desired_height
        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.desired_width = int(self.desired_height * self.aspect_ratio)
        self.image = pygame.transform.scale(self.image, (self.desired_width, self.desired_height))
        self.x = SCREEN_WIDTH // 2 - LANE_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2 - LANE_WIDTH // 2

        # Create rect as hitbox
        self.rect = Rect(self.x, self.y, self.desired_width - HITBOX_OFFSET, self.desired_height - HITBOX_OFFSET)
        self.rect.center = (self.x + self.desired_width // 2, self.y + self.desired_height // 2)
        self.rect_color = pygame.Color(0, 255, 0)

    def render(self, screen, surface, rotation):
        screen.blit(pygame.transform.rotate(self.image, rotation), (self.x, self.y))
        self.rect.center = (self.x + self.desired_width // 2 - lane_surface_x, self.y + self.desired_height // 2)
        # Draw rect onto surface
        pygame.draw.rect(surface, self.rect_color, self.rect)


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lanes")

# Background
texture_image = pygame.image.load("./assets/texture.png")
texture_image = pygame.transform.scale(texture_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.Surface(screen.get_size()).convert()
background.blit(texture_image, (0, 0))
background.set_alpha(50)

# Player
player_height = 100
player_image = pygame.image.load("./assets/red-car.png")
desired_height_player = 100
aspect_ratio_player = player_image.get_width() / player_image.get_height()
desired_width_player = int(desired_height_player * aspect_ratio_player)
player_image = pygame.transform.scale(player_image, (desired_width_player, desired_height_player))

# Player variables
player_rotation = 0

# Lanes
lane_width = 100
tire_lane_color = (128, 128, 128)
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

for i in range(NUMBER_OF_LANES):
    x_position = generate_lane_x(i)
    current_lane_color = lane_colors[i % len(lane_colors)]
    if i == 0 or i == NUMBER_OF_LANES - 1:
        current_lane_color = tire_lane_color
    lane = Lane(i, current_lane_color, x_position)
    lanes.append(lane)

# Lane rendering
for lane in lanes:
    lane.draw()

lane_surface_x = LANE_WIDTH // 2

# Obstacles
obstacles = []

# Dynamic variables
spawn_interval = random.randint(200, MAX_SPAWN_INTERVAL)
spawn_quantity = random.randint(1, MAX_SPAWN_QUANTITY)

# Game loop
player = Player("./assets/red-car.png", 100)
clock = pygame.time.Clock()
running = True
spawn_timer = 0
collision_detected = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        lane_surface_x += HORIZONTAL_SPEED
        player_rotation = 15
    elif keys[pygame.K_RIGHT]:
        lane_surface_x -= HORIZONTAL_SPEED
        player_rotation = -15
    else:
        player_rotation = 0
    
    # Spawn obstacles
    spawn_timer += clock.get_rawtime()
    if spawn_timer >= spawn_interval:
        for i in range(spawn_quantity):
            current_obstacle_x = generate_lane_x(random.randint(0, NUMBER_OF_LANES - 1)) + OBSTACLE_SIZE // 2
            obstacle = Obstacle("./assets/obstacle1.png", current_obstacle_x, -OBSTACLE_SIZE, OBSTACLE_SIZE)
            obstacles.append(obstacle)
        
        spawn_timer = 0

        spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)
        spawn_quantity = random.randint(1, MAX_SPAWN_QUANTITY)

    # Update obstacles
    for obstacle in obstacles:
        if obstacle.y > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
        obstacle.update(SPEED)
        if obstacle.rect.colliderect(player.rect):
            collision_detected = True
            print("Collision detected")
            break

    # Drawing on the screen
    screen.fill(WHITE)
    # screen.blit(background, (0, 0))
    game_surface.blit(lane_surface, (0, 0))
    for obstacle in obstacles:
        obstacle.render(game_surface)
    screen.blit(game_surface, (lane_surface_x, 0))
    screen.blit(background, (0, 0))
    player.render(screen, game_surface, player_rotation)
    pygame.draw.rect(test_surface, player.rect_color, player.rect, 5)
    test_surface.set_alpha(30)
    game_surface.blit(test_surface, (0, 0))

    if collision_detected:
        SPEED = 0
        HORIZONTAL_SPEED = 0
        boom_gif = pygame.image.load("./assets/explode-boom.gif")
        gif_rect = boom_gif.get_rect()
        center_x = (SCREEN_WIDTH - gif_rect.width) // 2
        center_y = (SCREEN_HEIGHT - gif_rect.height) // 2
        gif_rect.x = center_x
        gif_rect.y = center_y
        screen.blit(boom_gif, gif_rect)
        if keys[pygame.K_SPACE]:
            SPEED = SPEED_CONST
            HORIZONTAL_SPEED = HORIZONTAL_SPEED_CONST
            collision_detected = False
            obstacles.clear()
            lane_surface_x = LANE_WIDTH // 2

    # Update the screen
    pygame.display.flip()
    clock.tick(60)


# Quit the game
pygame.quit()
