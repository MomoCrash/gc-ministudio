import pygame

import settings
from gameobject import GameObject
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from texture import SpritesRef, Assets
from vector import Vector2
from text import Text
from Music import Songs


class StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.chapters = [ GameObject( Vector2(739, 545), spriteDimensions=Vector2(80,80), spriteRef=SpritesRef.UNCHECK_BUTTON ),
                          GameObject( Vector2(1124, 473), spriteDimensions=Vector2(80,80), spriteRef=SpritesRef.UNCHECK_BUTTON ),
                          GameObject( Vector2(1374, 580), spriteDimensions=Vector2(80,80), spriteRef=SpritesRef.UNCHECK_BUTTON ) ]
        self.current_menu_item = None
        self.start = GameObject(Vector2(0,0), Vector2(0,0), Vector2(1,1), spriteDimensions=Vector2(1920,1080), spriteRef=SpritesRef.START)
        self.textRenderer = Text(self.screen, settings.GAME_FONT, 30)

        self.music_manager = Songs()

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
        settings.MUSIC.Play_Menu()
        while selected is None:
            played = False
            while not played:

                Assets.GetSprite(SpritesRef.KEY_ART).draw(self.screen, Vector2(0, 0),
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
                        Assets.GetSprite(SpritesRef.KEY_ART).draw(self.screen, Vector2(0, 0),
                                                                  Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
                        Assets.GetSprite(SpritesRef.BOOK).draw(self.screen, Vector2(0, 0),
                                                                  Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
                        self.draw_chapters()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                for j, chapter in enumerate(self.chapters):
                                    if chapter.getCollision(Vector2(mouse_x, mouse_y)):
                                        selected = j
                            elif event.type == pygame.MOUSEMOTION:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                for j, chapter in enumerate(self.chapters):
                                    if chapter.getCollision(Vector2(mouse_x, mouse_y)):
                                        chapter.spriteRenderer.spriteRef = SpritesRef.CHECK_BUTTON
                                    else:
                                        chapter.spriteRenderer.spriteRef = SpritesRef.UNCHECK_BUTTON

                        pygame.display.flip()
            clock.tick(60)
            pygame.display.flip()

        return selected
