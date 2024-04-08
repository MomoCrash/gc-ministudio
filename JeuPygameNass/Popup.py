import pygame
from pygame.locals import *

pygame.init()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision Detection")

class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Hitbox:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = self.rect.inflate(50, 50)
        self.color = color
        self.show_popup = False
        self.big_popup = False

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.show_popup:
            if not self.big_popup:
                popup_rect = pygame.Rect(self.rect.x, self.rect.y - 80, self.rect.width + 100, 100)
                pygame.draw.rect(screen, BLACK, popup_rect)
                font = pygame.font.Font(None, 16) 
                description_text = "Appuyez sur E pour ouvrir la description"
                text_x = popup_rect.x + 10
                text_y = popup_rect.y + 10
                max_width = popup_rect.width - 20
                words = description_text.split()
                space_width = font.size(' ')[0]
                space_count = 0
                char_count = 0
                line = ''
                for word in words:
                    word_width = font.size(word)[0]
                    char_count += len(word)
                    if char_count * font.size('A')[0] + space_count * space_width >= max_width:
                        screen.blit(font.render(line, True, WHITE), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, WHITE), (text_x, text_y))
            else:
                popup_width = 600  
                popup_height = 300  
                popup_x = (SCREEN_WIDTH - popup_width) // 2  
                popup_y = (SCREEN_HEIGHT - popup_height) // 2 + 50  
                popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                pygame.draw.rect(screen, BLACK, popup_rect)
                font = pygame.font.Font(None, 24)  
                description_text = "DESCRIPTION DE L'OBJET : description etc etc du rectangle"
                text_x = popup_rect.x + 20
                text_y = popup_rect.y + 20
                max_width = popup_rect.width - 40
                words = description_text.split()
                space_width = font.size(' ')[0]
                space_count = 0
                char_count = 0
                line = ''
                for word in words:
                    word_width = font.size(word)[0]
                    char_count += len(word)
                    if char_count * font.size('A')[0] + space_count * space_width >= max_width:
                        screen.blit(font.render(line, True, WHITE), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, WHITE), (text_x, text_y))



    def toggle_popup(self, show):
        self.show_popup = show


def check_collision(player, hitbox_rect):
    return player.rect.colliderect(hitbox_rect.hitbox)

player = Player(50, 300, 50, 50, BLUE)
hitbox_rect = Hitbox(600, 300, 100, 100, RED)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_e:
                if check_collision(player, hitbox_rect):
                    hitbox_rect.toggle_popup(True)
                    hitbox_rect.big_popup = not hitbox_rect.big_popup

    dt = clock.tick(60) / 1000.0

    keys = pygame.key.get_pressed()
    player_speed = 200
    if keys[K_LEFT]:
        player.rect.x -= player_speed * dt
    if keys[K_RIGHT]:
        player.rect.x += player_speed * dt
    if keys[K_UP]:
        player.rect.y -= player_speed * dt
    if keys[K_DOWN]:
        player.rect.y += player_speed * dt

    if check_collision(player, hitbox_rect):
        hitbox_rect.toggle_popup(True)
    else:
        hitbox_rect.toggle_popup(False)

    screen.fill(WHITE)

    player.draw(screen)
    hitbox_rect.draw(screen)

    pygame.display.flip()

pygame.quit()
