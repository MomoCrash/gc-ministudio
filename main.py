from texture import Assets
import settings
from editor import Editor
from startmenu import StartMenu
from game import Game
from pauseUI import Menu
from Music import Songs
import pygame

def init_game():
    pygame.display.init()

    pygame.mixer.pre_init(44100, -16, 2, 512)
    
    settings.SCREEN_WIDTH = 1920
    settings.SCREEN_HEIGHT = 1080

    pygame.init()

    pygame.mixer.init()
    settings.MUSIC = Songs()
    settings.GAME_FONT = pygame.font.Font("Assets/Font/Thunder.ttf", 40)


if __name__ == '__main__':

    init_game()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN,
                                     pygame.DOUBLEBUF)
    Assets.Init()

    editor = False
    # editor = True

    if not editor:
        menu = StartMenu(screen)

        pause_menu = Menu(screen)
        game = Game(screen, menu.chapter, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Ultimate Game of the Year", pause_menu)
    else:
        editor = Editor(screen, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
