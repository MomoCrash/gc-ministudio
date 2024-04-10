import pygame

import settings
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from texture import SpritesRef, Assets
from vector import Vector2
from text import Text


class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.chapters = [Vector2(0,0), Vector2(0,0), Vector2(0,0), ]
        self.current_menu_item = None
        self.backgroundRef = SpritesRef.BACKGROUND_1
        self.textRenderer = Text(self.screen, settings.GAME_FONT, 20)

        self.chapter = self.main_menu()

    def draw_background(self):
        Assets.GetSprite(self.backgroundRef).draw(self.screen, Vector2(0,0), Vector2(1,1))

    def draw_chapters(self):
        chapters = []
        for i, chapter in enumerate(self.chapters):
            chapter_text = self.textRenderer.draw_text(chapter, (255,255,255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50, 10, 10)
            chapters.append((i, chapter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))))

        return_text = self.textRenderer.draw_text("Retour", (255,255,255), SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2 + len(self.chapters) * 50, 10, 10)
        return return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + len(self.chapters) * 50)), chapters

    def main_menu(self) -> int:
        self.draw_background()
        selected = None
        while selected is None:
            self.draw_chapters()
            pygame.display.flip()
            returned = False
            while selected is None and not returned:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        print(mouse_x, mouse_y)
                        chapters_data = self.draw_chapters()
                        if chapters_data[0].collidepoint(mouse_x, mouse_y):
                            returned = True
                            continue
                        for j, chapter_collider in chapters_data[1]:
                            if chapter_collider.collidepoint(mouse_x, mouse_y):
                                selected = j

            self.draw_background()
            pygame.display.flip()
        print(selected)
        return selected