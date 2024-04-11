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
        self.chapters = [ GameObject( Vector2(755, 567), spriteDimensions=Vector2(40,40), spriteRef=SpritesRef.CHECK_BUTTON ),
                          GameObject( Vector2(1143, 500), spriteDimensions=Vector2(40,40), spriteRef=SpritesRef.CHECK_BUTTON ),
                          GameObject( Vector2(1384, 600), spriteDimensions=Vector2(40,40), spriteRef=SpritesRef.CHECK_BUTTON ) ]
        self.current_menu_item = None
        self.start = GameObject(Vector2(0,0), Vector2(0,0), Vector2(1,1), spriteDimensions=Vector2(1920,1080), spriteRef=SpritesRef.START)
        self.textRenderer = Text(self.screen, settings.GAME_FONT, 30)

        self.chapter = self.main_menu()

    def draw_menu(self):
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255,255,255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)

    def draw_chapters(self):
        for i, chapter in enumerate(self.chapters):
            chapter.update(self.screen, Vector2(0,0))


    def main_menu(self) -> int:
        global current_menu_item
        selected = None
        clock = pygame.time.Clock()
        while selected is None:
            played = False
            while not played:

                Assets.GetSprite(SpritesRef.BG_LEVEL_1_1).draw(self.screen, Vector2(0, 0),
                                                          Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
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
                        Assets.GetSprite(SpritesRef.BG_LEVEL_1_1).draw(self.screen, Vector2(0, 0),
                                                                  Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
                        Assets.GetSprite(SpritesRef.BOOK).draw(self.screen, Vector2(0, 0),
                                                                  Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
                        self.draw_chapters()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                print(mouse_x, mouse_y)
                                for j, chapter in enumerate(self.chapters):
                                    if chapter.getCollision(Vector2(mouse_x, mouse_y)):
                                        selected = j
                        pygame.display.flip()
            clock.tick(60)
            pygame.display.flip()
        print(selected)
        return selected
