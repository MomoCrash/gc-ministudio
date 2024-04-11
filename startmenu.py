import pygame

import settings
from gameobject import GameObject
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from texture import SpritesRef, Assets
from vector import Vector2
from text import Text


class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.chapters = ["CHAPITRE 1", "CHAPITRE 2", "CHAPITRE 3", "CHAPITRE 4", "CHAPITRE 5", ]
        self.current_menu_item = None
        self.backgroundRef = SpritesRef.BACKGROUND_0
        self.start = GameObject(Vector2(0,0), Vector2(0,0), Vector2(1,1), spriteDimensions=Vector2(1920,1080), spriteRef=SpritesRef.START)
        self.textRenderer = Text(self.screen, settings.GAME_FONT, 20)

        self.chapter = self.main_menu()

    def draw_menu(self):
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255,255,255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)

    def draw_background(self):
        Assets.GetSprite(self.backgroundRef).draw(self.screen, Vector2(0,0), Vector2(SCREEN_WIDTH,SCREEN_HEIGHT))

    def draw_chapters(self):
        chapters = []
        for i, chapter in enumerate(self.chapters):
            chapter_text = self.textRenderer.draw_text(chapter, (255,255,255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50, 10, 10)
            chapters.append((i, chapter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))))

        return_text = self.textRenderer.draw_text("Retour", (255,255,255), SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2 + len(self.chapters) * 50, 10, 10)
        return return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + len(self.chapters) * 50)), chapters


    def main_menu(self) -> int:
        global current_menu_item
        selected = None
        clock = pygame.time.Clock()
        while selected is None:
            played = False
            while not played:

                self.start.update(self.screen, Vector2(0,0))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            played = True
                            self.screen.fill((0, 0, 0))
                clock.tick(60)

                returned = False
                if played:
                    while selected is None and not returned:
                        chapters_data = self.draw_chapters()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                if chapters_data[0].collidepoint(mouse_x, mouse_y):
                                    returned = True
                                    continue
                                for j, chapter_collider in chapters_data[1]:
                                    if chapter_collider.collidepoint(mouse_x, mouse_y):
                                        selected = j
                        pygame.display.flip()
            clock.tick(60)
            pygame.display.flip()
        print(selected)
        return selected
