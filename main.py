from texture import Assets
import settings
from editor import Editor
from startmenu import StartMenu
from game import Game
import pygame

def init_game():
    pygame.display.init()

    pygame.mixer.pre_init(44100, -16, 2, 512)
    
    settings.SCREEN_WIDTH = 1920
    settings.SCREEN_HEIGHT = 1080

    pygame.init()

    pygame.mixer.init()
    settings.GAME_FONT = pygame.font.Font("Assets/Font/Thunder.ttf", 21)


if __name__ == '__main__':

    init_game()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN,
                                     pygame.DOUBLEBUF)
    Assets.Init()

    #menu = StartMenu(screen)

    #game = Game(screen, menu.chapter, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Utltimate game of the Year")

    editor = Editor(screen, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
