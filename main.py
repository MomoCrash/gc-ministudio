import texture
import settings
import text
from game import Game
from pygame import display
from editor import Editor

if __name__ == '__main__':
    texture.Assets.Init()

    display.init()
    display_info = display.Info()
    settings.SCREEN_WIDTH = display_info.current_w
    settings.SCREEN_HEIGHT = display_info.current_h

    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "Utltimate game of the Year")
    
    #editor = Editor(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
