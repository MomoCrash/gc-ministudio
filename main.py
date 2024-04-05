from game import Game
from editor import Editor
import texture
import settings
import text

if __name__ == '__main__':
    texture.Assets.Init()
    
    game = Game(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "Utltimate game of the Year")
    text = text.draw_text("Hello World !", "Arial", (255,255,255),200,500,15,30)
    
    #game = Game(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "Utltimate game of the Year")
    editor = Editor(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "EDITEUR DE JEU")
