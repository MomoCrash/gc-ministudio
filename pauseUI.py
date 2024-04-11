import pygame
from pygame.locals import *


class Button:
    def __init__(self, screen, image, position):
        self.screen = screen
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        self.visible = False

    def draw(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)

    def set_position(self, position):
        self.position = position
        self.rect.topleft = position

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def resize(self, max_width, max_height):
        if self.rect.width > max_width or self.rect.height > max_height:
            self.image = pygame.transform.scale(self.image, (max_width, max_height))
            self.rect = self.image.get_rect(topleft=self.position)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_active = False
        self.menu_button = pygame.image.load('menubutton.png').convert_alpha()
        self.book_background = pygame.image.load('menubackground.png').convert_alpha()
        self.continue_button = pygame.image.load('continuer.png').convert_alpha()
        self.options_button = pygame.image.load('option.png').convert_alpha()
        self.quit_button = pygame.image.load('quitter.png').convert_alpha()
        self.book_x = (1920 - self.book_background.get_width()) // 2
        self.book_y = (1080 - self.book_background.get_height()) // 2

      
        self.menu_button_rect = self.screen.blit(self.menu_button, (10, 10))
        self.continue_button_rect = Button(screen, self.continue_button, (200, 200))
        self.options_button_rect = Button(screen, self.options_button, (200, 300))
        self.quit_button_rect = Button(screen, self.quit_button, (200, 400))

       
        max_button_width = 1000
        max_button_height = 250
        self.continue_button_rect.resize(max_button_width, max_button_height)
        self.options_button_rect.resize(max_button_width, max_button_height)
        self.quit_button_rect.resize(max_button_width, max_button_height)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_active = not self.menu_active
            elif self.menu_active:  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.continue_button_rect.rect.collidepoint(mouse_pos):
                        self.menu_active = False  
                        return "CONTINUE"
                    elif self.options_button_rect.rect.collidepoint(mouse_pos):
                        print("Afficher les options")
                        return "OPTIONS"
                    elif self.quit_button_rect.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()
        return None



