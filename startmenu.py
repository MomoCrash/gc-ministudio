import pygame
from text import Text
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from gameobject import GameObject
from vector import Vector2

def StartMenu():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.menu_items = ["JOUER", "CHAPITRES"]
        self.chapters = ["CHAPITRE 1", "CHAPITRE 2", "CHAPITRE 3", "CHAPITRE 4", "CHAPITRE 5", ]
        self.current_menu_item = None
        self.image = pygame.transform.scale(pygame.image.load("nordics.jfif"), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_menu(self):
        self.screen.fill((0,0,0))
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255,255,255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)

    def draw_background(self):
        self.screen.fill((0,0,0))

    def draw_chapters(self):
        self.screen.fill((0,0,0))
        for i, chapter in enumerate(self.chapters):
            text = self.font.render(chapter, True, (255,255,255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)
        back_button = self.screen.render("RETOUR", True, (255,255,255))
        back_rect = back_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_button, back_rect)
        return back_rect


    def main_menu(self):
        global current_menu_item
        draw_background()
        draw_menu()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, item in enumerate(self.menu_items):
                        text_rect = self.font.render(item, True, (255,255,255)).get_rect(
                            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            current_menu_item = item
                            if current_menu_item == "JOUER":
                                play_game()
                            elif current_menu_item == "CHAPITRES":
                                draw_chapters()
                                pygame.display.flip()
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                        elif event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            back_rect = draw_chapters()
                                            if back_rect.collidepoint(mouse_x, mouse_y):
                                                return
                                            for j, chapter in enumerate(self.chapters):
                                                text_rect = self.font.render(chapter, True, self.WHITE).get_rect(
                                                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + j * 50))
                                                if text_rect.collidepoint(mouse_x, mouse_y):
                                                    print(f"chapitre {j + 1} sélectionné ")
                                                    return
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, item in enumerate(self.menu_items):
                        text_rect = self.font.render(item, True, self.WHITE).get_rect(
                            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            self.menu_items[i] = item.upper()
                        else:
                            self.menu_items[i] = item
            draw_background()
            draw_menu()
            pygame.display.flip()

    def play_game(self):
        print("jeu lancé")

    def main(self):
        main_menu()