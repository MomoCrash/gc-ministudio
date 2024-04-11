import pygame

import settings
from text import Text
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from gameobject import GameObject
from vector import Vector2

# Info box
class InfoBox():
    def __init__(self, screen, x, y, width, height):
        self.gameobject = GameObject( Vector2(x, y), spriteDimensions=Vector2(width, height) )
        self.color = pygame.Color(0, 0, 0)
        self.text: Text = Text(screen, settings.GAME_FONT, 21)
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = self.rect.inflate(50, 50)
        self.show_popup = False
        self.big_popup = False
        self.screen = screen

    def is_on_player(self, player) -> bool:
        if self.gameobject.getCollision(player):
            return True
        return False

    def draw(self, desc_text, bg_color: pygame.Color, ft_color: pygame.Color):
        pygame.draw.rect(self.screen, self.color, self.rect)
        if self.show_popup:
            if not self.big_popup:
                popup_rect = pygame.Rect(self.rect.x, self.rect.y - 80, self.rect.width + 100, 100)
                pygame.draw.rect(self.screen, bg_color, popup_rect)
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
                        self.screen.blit(font.render(line, True, ft_color), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                self.screen.blit(font.render(line, True, ft_color), (text_x, text_y))
            else:
                popup_width = 600
                popup_height = 300
                popup_x = (SCREEN_WIDTH - popup_width) // 2
                popup_y = (SCREEN_HEIGHT - popup_height) // 2 + 50
                popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                pygame.draw.rect(self.screen, bg_color, popup_rect)
                font = pygame.font.Font(None, 24)
                description_text = desc_text
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
                        self.screen.blit(font.render(line, True, ft_color), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                self.screen.blit(font.render(line, True, ft_color), (text_x, text_y))