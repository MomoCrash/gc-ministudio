import pygame
import settings
import os
from enum import Enum
from enum import auto


class SpritesRef(Enum):
    BACKGROUND_0 = auto()
    BACKGROUND_1 = auto()
    LIGHT = auto()


class SpriteSheetsRef(Enum):
    PLAYER_WALK_LEFT = auto()
    PLAYER_WALK_RIGHT = auto()


class Sprite:
    def __init__(self, path_to_texture, width, height):
        self.texture_path = path_to_texture
        self.texture = pygame.image.load(path_to_texture)
        self.size = (width, height)
        self.texture = pygame.transform.scale(self.texture, self.size)
        
    def draw(self, surface: pygame.Surface, pos: pygame.Rect):
        surface.blit(self.texture, pos)
        

class SpriteSheet:
    def __init__(self, textures: list[Sprite]):
        self.frame_count = len(textures)
        self.frame_per_image = settings.ANIMATION_DURATION // self.frame_count
        self.textures = textures
        self.current_index = 0
        self.time = pygame.time.get_ticks()

    # TODO: RANDOM FIRST FRAME / DELAY
    def draw(self, ticks, surface: pygame.Surface, pos: pygame.Rect):
        if self.is_next_frame(ticks):
            self.current_index += 1
            if self.current_index >= self.frame_count:
                self.current_index = 0
        self.textures[self.current_index].draw(surface, pos)
    
    def is_next_frame(self, current_ticks) -> bool:
        if current_ticks - self.time > self.frame_per_image:
            self.time = current_ticks
            return True
        return False


class Assets:

    Sprites: list[Sprite] = []
    SpriteSheets: list[SpriteSheet] = []

    AssetFolder = os.path.dirname(os.path.realpath(__file__)) + "/Assets/"

    @staticmethod
    def Init():

        spriteSheetsFolder = [f.path for f in os.scandir(Assets.AssetFolder + "SpriteSheets/") if f.is_dir()]
        textureFolders = [f.path for f in os.scandir(Assets.AssetFolder + "Textures/") if f.is_dir()]

        for mainFolderSheet in spriteSheetsFolder:
            for animationPartFolder in os.listdir(mainFolderSheet):
                sprites = []
                for animationFiles in os.listdir(mainFolderSheet + "/" + animationPartFolder):
                    sprite = Sprite(mainFolderSheet + "/" + animationPartFolder + "/" + animationFiles, 60, 100)
                    sprites.append(sprite)
                if len(sprites) < 1:
                    continue
                Assets.SpriteSheets.append(SpriteSheet(sprites))

        for textureFolderName in textureFolders:
            for textureFile in os.listdir(textureFolderName):
                Assets.Sprites.append(Sprite(textureFolderName + '/' + textureFile, 1920, 1080))

    @staticmethod
    def GetSprite(ref: Enum) -> Sprite:
        return Assets.Sprites[ref.value - 1]
    
    @staticmethod
    def GetSpriteSheet(ref: Enum) -> SpriteSheet:
        return Assets.SpriteSheets[ref.value - 1]