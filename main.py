from game import Game
from editor import Editor
import texture
import settings

if __name__ == '__main__':
    texture.Assets.Init()
    #game = Game(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "Utltimate game of the Year")
    editor = Editor(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")