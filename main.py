from texture import Assets
import settings
from startmenu import StartMenu
from game import Game
from pauseUI import Menu  
import pygame

def init_game():
    pygame.display.init()
    
    settings.SCREEN_WIDTH = 1920
    settings.SCREEN_HEIGHT = 1080

    pygame.init()
    settings.GAME_FONT = pygame.font.Font("Assets/Font/Thunder.ttf", 21)


if __name__ == '__main__':
    Assets.Init()

    init_game()

    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN)

    menu = StartMenu(screen)

    pause_menu = Menu(screen) 
    game = Game(screen, menu.chapter, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Ultimate Game of the Year", pause_menu)  
    
    #editor = Editor(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
