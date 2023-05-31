import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

#constants
screen_width = 800
screen_height = 600
white_hex = '#ffffff'
WHITE = pygame.Color(white_hex)

#Game variables
number_of_lanes = 10
lane_width = 100
starting_lane = number_of_lanes // 2

min_spawn_interval = 100 
max_spawn_interval = 300
min_spawn_quantity = 3
max_spawn_quantity = 7

obstacle_size = 50

hitbox_offset = 20

horizontal_speed_const = 6
speed_const = 9

horizontal_speed = horizontal_speed_const
speed = speed_const

#functions
def generateLaneX(number_of_lane):
    return lane_width * number_of_lane

#Surfaces
laneSurface = pygame.Surface((lane_width*number_of_lanes, screen_height))

laneSurfaceWidth = laneSurface.get_width()
laneSurfaceHeight = laneSurface.get_height()
gameSurface = pygame.Surface((laneSurfaceWidth, laneSurfaceHeight))

test_surface = pygame.Surface((laneSurfaceWidth, laneSurfaceHeight))
#Classes
class Lane:

    def __init__(self,number_of_lane, color, x):
        self.number_of_lane = number_of_lane
        self.color = color
        self.x = x

    def draw(self):
        pygame.draw.rect(laneSurface, self.color, (self.x, 0 , lane_width, screen_height))

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
        screen.blit(self.image, (self.x,self.y))
        #pygame.draw.rect(screen, self.rect_color, self.rect)

class Player:
    def __init__(self, image_path, desired_height):
        self.image = pygame.image.load(image_path)
        self.desired_height = desired_height
        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.desired_width = int(self.desired_height * self.aspect_ratio)
        self.image = pygame.transform.scale(self.image, (self.desired_width, self.desired_height))
        self.x = screen_width // 2 - lane_width // 2
        self.y = screen_height // 2 - lane_width // 2

        #create rect as hitbox
        self.rect = Rect(self.x, self.y, self.desired_width - hitbox_offset, self.desired_height - hitbox_offset)
        self.rect.center = (self.x + self.desired_width // 2, self.y + self.desired_height // 2)
        self.rect_color = pygame.Color(0, 255, 0)

    def render(self, screen, rotation):
        screen.blit(pygame.transform.rotate(self.image, rotation), (self.x, self.y))
        self.rect.center = (self.x + self.desired_width // 2, self.y + self.desired_height // 2)
        #pygame.draw.rect(screen, self.rect_color, self.rect)
        



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

for i in range(number_of_lanes):
    x_position = generateLaneX(i)
    current_lane_color = lane_colors[i % len(lane_colors)]
    if i == 0 or i == number_of_lanes - 1:
        current_lane_color = tire_lane_color
    lane = Lane(i, current_lane_color, x_position)
    lanes.append(lane)

#Lane rendering
for lane in lanes:
    lane.draw()

laneSurfaceX = lane_width // 2

#Obstacles
obstacles = []

#Dynamic variables
spawn_interval = random.randint(200, max_spawn_interval)
spawn_quantity = random.randint(1, max_spawn_quantity)

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
        laneSurfaceX += horizontal_speed
        player_rotation = 15
    elif keys[pygame.K_RIGHT]:
        laneSurfaceX -= horizontal_speed
        player_rotation = -15
    else:
        player_rotation = 0
    
    # Spawn obstacles
    spawn_timer += clock.get_rawtime()
    if spawn_timer >= spawn_interval:
        for i in range(spawn_quantity):
            current_obstacle_x = generateLaneX(random.randint(0, number_of_lanes - 1)) + obstacle_size // 2
            obstacle = Obstacle("./assets/obstacle1.png", current_obstacle_x, -obstacle_size, obstacle_size)
            obstacles.append(obstacle)
        
        spawn_timer = 0

        spawn_interval = random.randint(min_spawn_interval, max_spawn_interval)
        spawn_quantity = random.randint(1, max_spawn_quantity)

    # Update obstacles
    for obstacle in obstacles:
        if obstacle.y > screen_height:
            obstacles.remove(obstacle)
        obstacle.update(speed)
        # if obstacle.rect.colliderect(player.rect):
        #     collision_detected = True
        #     print("Collision detected")
        #     break

    # Drawing on the screen
    screen.fill(WHITE)
    #screen.blit(background, (0, 0))
    gameSurface.blit(laneSurface, (0, 0))
    for obstacle in obstacles:
        obstacle.render(gameSurface)
    screen.blit(gameSurface, (laneSurfaceX, 0))
    screen.blit(background, (0, 0))
    player.render(screen, player_rotation)
    pygame.draw.rect(test_surface, player.rect_color, player.rect, 5)
    test_surface.set_alpha(30)
    gameSurface.blit(test_surface, (0, 0))

    if collision_detected:
        speed = 0
        horizontal_speed = 0
        if keys[pygame.K_SPACE]:
            speed = speed_const
            horizontal_speed = horizontal_speed_const
            collision_detected = False
            obstacles.clear()
            laneSurfaceX = lane_width // 2

    # Update the screen
    pygame.display.flip()
    clock.tick(60)


# Quit the game
pygame.quit()