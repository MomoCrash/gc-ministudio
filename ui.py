import pygame
from text import Text
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from gameobject import GameObject
from vector import Vector2

#Pop up box
class Hitbox:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = self.rect.inflate(50, 50)
        self.color = color
        self.show_popup = False
        self.big_popup = False

    def draw(self, screen, bg_color: pygame.Color, ft_color: pygame.Color):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.show_popup:
            if not self.big_popup:
                popup_rect = pygame.Rect(self.rect.x, self.rect.y - 80, self.rect.width + 100, 100)
                pygame.draw.rect(screen, bg_color, popup_rect)
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
                        screen.blit(font.render(line, True, ft_color), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, ft_color), (text_x, text_y))
            else:
                popup_width = 600  
                popup_height = 300  
                popup_x = (SCREEN_WIDTH - popup_width) // 2
                popup_y = (SCREEN_HEIGHT - popup_height) // 2 + 50  
                popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                pygame.draw.rect(screen, bg_color, popup_rect)
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
                        screen.blit(font.render(line, True, ft_color), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, ft_color), (text_x, text_y))


# Info box
class InfoBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.gameobject = GameObject( Vector2(x, y), spriteDimensions=Vector2(width, height))
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.font = pygame.font.Font(None, 24)
        self.text = Text()
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.text = "Appuyez sur E pour les infos"
        else:
            self.text = ""
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

class DescriptionBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300, 200))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.font = pygame.font.Font(None, 24)
        self.text = "Description : C'est un rectangle blanc"
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)