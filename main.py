from game import Game
import texture
import settings
<<<<<<< Updated upstream
=======
import text
from game import Game 
from pygame import display
from editor import Editor
>>>>>>> Stashed changes

if __name__ == '__main__':
    texture.Assets.Init()
    game = Game(settings.SCREEN_WIDHT, settings.SCREEN_HEIGHT, "Utltimate game of the Year")