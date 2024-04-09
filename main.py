from texture import Assets
import settings
from editor import Editor
from startmenu import StartMenu
from game import Game
import pygame


def init_game():
    pygame.display.init()
    display_info = pygame.display.Info()
    settings.SCREEN_WIDTH = display_info.current_w
    settings.SCREEN_HEIGHT = display_info.current_h

    pygame.init()
    settings.GAME_FONT = pygame.font.Font("Assets/Font/Thunder.ttf", 21)


if __name__ == '__main__':
    Assets.Init()

    init_game()

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    menu = StartMenu(screen)

    game = Game(screen, menu.chapter, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Utltimate game of the Year")
    
    #editor = Editor(screen, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
