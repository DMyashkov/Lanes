import pygame

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

lane_width = 100
lane_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Example colors for three lanes

class Lane:
    def __init__(self, y, color):
        self.y = y
        self.color = color

    def move(self, speed):
        self.y += speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (0, self.y, screen_width, lane_width))

class Player:
    def __init__(self):
        self.lane_index = 1

    def switch_lane(self, direction):
        self.lane_index += direction
        self.lane_index %= len(lane_colors)

    def draw(self):
        lane_color = lane_colors[self.lane_index]
        pygame.draw.rect(screen, lane_color, (screen_width // 2 - lane_width // 2, screen_height // 2 - lane_width // 2, lane_width, lane_width))

lanes = [Lane(i * lane_width, lane_colors[i % len(lane_colors)]) for i in range(3)]
player = Player()

game_over = False
lane_speed = 5

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.switch_lane(-1)
            elif event.key == pygame.K_RIGHT:
                player.switch_lane(1)

    screen.fill((255, 255, 255))  # Clear the screen

    for lane in lanes:
        lane.move(lane_speed)
        lane.draw()

    player.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
