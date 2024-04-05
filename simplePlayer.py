from dataclasses import dataclass
import pygame
pygame.init()

@dataclass
class GameObject:
    position: pygame.Vector2
    scale: pygame.Vector2
    velocity: pygame.Vector2

screenSize = pygame.Vector2( 320, 240 )
screen = pygame.display.set_mode( ( screenSize.x, screenSize.y ) )
clock = pygame.time.Clock()
dt = 0

player = GameObject( pygame.Vector2( screenSize.x/2, screenSize.y/2 ), pygame.Vector2( 1, 1 ), pygame.Vector2( 0, 0 ) )

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill( ( 0, 0, 0 ) )
    
    pygame.draw.circle( screen, "red", player.position, 20 * player.scale.x )
    
    keys = pygame.key.get_pressed()
    # if keys[ pygame.K_z ]:
    #     player.position.y -= 300 * dt
    # if keys[ pygame.K_s ]:
    #     player.position.y += 300 * dt
    if keys[ pygame.K_q ]:
        player.velocity.x = -100
    if keys[ pygame.K_d ]:
        player.velocity.x = 100
    
    if player.velocity.x != 0:
        player.position.x += player.velocity.x * dt
        if 20 < player.position.x < screenSize.x - 20:
            player.velocity.x *= 0.8
        else:
            player.position.x -= player.velocity.x * dt
            player.velocity.x = 0
    
    
    pygame.display.flip()
    
    dt = clock.tick( 60 ) / 1000


pygame.quit()