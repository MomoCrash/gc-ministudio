import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Plateformer")

player_width = 50
player_height = 50
player_x = 0
player_y = SCREEN_HEIGHT - player_height
player_speed = 5
jump_height = 10
jump_speed = 5
gravity = 0.5
is_jumping = False
jump_count = jump_height
background_color = BLACK
image1 = pygame.transform.scale(pygame.image.load('render.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
image2 = pygame.transform.scale(pygame.image.load('render1.jfif'), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_segments = [image1, image2]
segment_width = background_segments[0].get_width()
camera_x = 0
camera_y = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True

   #when the camera starts moving 
    camera_x = player_x - SCREEN_WIDTH // 5
    camera_y = player_y - SCREEN_HEIGHT // 5


    camera_x = max(0, min(camera_x, segment_width))
    camera_y = max(0, min(camera_y, SCREEN_HEIGHT))

    SCREEN.fill(BLACK)
    for i, segment in enumerate(background_segments):
        SCREEN.blit(segment, (i * segment_width - camera_x, 0))
    pygame.draw.rect(SCREEN, BLACK, (player_x - camera_x, player_y - camera_y, player_width, player_height))

    pygame.display.flip()

    clock.tick(60)