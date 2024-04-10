import pygame
import os
import settings
from vector import Vector2
from enum import Enum, auto

class SpritesRef(Enum):

    BOOK = auto()
    START = auto()

    BG_LEVEL_1_1 = auto()
    BG_LEVEL_1_2 = auto()
    BG_LEVEL_1_COLOR = auto()
    BG_LEVEL_1_4 = auto()

    BG_LEVEL_1_5 = auto()
    BG_LEVEL_1_6 = auto()
    BG_LEVEL_1_7 = auto()

    BG_LEVEL_1_8 = auto()
    BG_LEVEL_1_9 = auto()
    BG_LEVEL_1_10 = auto()

    BG_LEVEL_1_11 = auto()
    BG_LEVEL_1_12 = auto()
    BG_LEVEL_1_13 = auto()

    LVL1_LOG = auto()
    LVL1_ROCK_1 = auto()
    LVL1_ROCK_2 = auto()
    LVL1_ROCK_3 = auto()
    LVL1_ROCK_4 = auto()
    LVL1_ROCK_SIDE = auto()
    LVL1_ROCK_FACE = auto()
    LVL1_TOMBSTONE = auto()
    LVL1_STUMP = auto()
    TEST = auto()

    TOMAHAWK = auto()


class SpriteSheetsRef(Enum):
    ENNEMY_ATTACK_LEFT = auto()
    ENNEMY_ATTACK_RIGHT = auto()
    ENNEMY_GET_HIT_LEFT = auto()
    ENNEMY_GET_HIT_RIGHT = auto()
    ENNEMY_WALK_LEFT = auto()
    ENNEMY_WALK_RIGHT = auto()
    ENNEMY_SHIELD_LEFT = auto()
    ENNEMY_SHIELD_RIGHT = auto()


    PLAYER_ATTACK_LEFT = auto()
    PLAYER_ATTACK_RIGHT = auto()
    PLAYER_GET_HIT_LEFT = auto()
    PLAYER_GET_HIT_RIGHT = auto()
    PLAYER_WALK_LEFT = auto()
    PLAYER_WALK_RIGHT = auto()
    PLAYER_SHIELD_LEFT = auto()
    PLAYER_SHIELD_RIGHT = auto()





class Sprite:
    def __init__(self, path_to_texture, width, height):
        self.texture_path = path_to_texture
        self.texture = pygame.image.load(path_to_texture).convert_alpha()
        self.size = (width, height)
        self.texture = pygame.transform.scale(self.texture, self.size)
        
    def draw( self, surface: pygame.Surface, position: Vector2, scale: Vector2 ):
        surface.blit( self.texture, ( position.x, position.y, scale.x, scale.y ) )
        

class SpriteSheet:
    def __init__(self, textures: list[Sprite]):
        self.frame_count = len(textures)
        self.frame_per_image = settings.ANIMATION_DURATION // self.frame_count
        self.textures = textures
        self.current_index = 0
        self.time = pygame.time.get_ticks()
        self.callback: function = None

    # TODO: RANDOM FIRST FRAME / DELAY
    def draw( self, ticks, surface: pygame.Surface, position: Vector2, scale: Vector2, func = lambda: 0 ):
        self.callback = func
        if self.is_next_frame(ticks):
            self.current_index += 1
            if self.current_index >= self.frame_count:
                self.callback()
                self.current_index = 0


        self.textures[self.current_index].draw( surface, position, scale )
    
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

                texture_param = mainFolderSheet + "/" + animationPartFolder + '/' + "param.txt"
                params = {}
                with open(texture_param, "r") as file:
                    lines = file.readlines()
                    if len(lines) == 0:
                        print(("CRITICAL ERROR : PLEASE ADD PARAM FILE IN " + animationPartFolder))
                        break
                    for line in lines:
                        splited = line.split(":")
                        params[splited[0]] = splited[1]

                for animationFiles in os.listdir(mainFolderSheet + "/" + animationPartFolder):
                    if not animationFiles.endswith(".txt"):
                        sprite = Sprite(mainFolderSheet + "/" + animationPartFolder + "/" + animationFiles, int(params["w"]), int(params["h"]))
                        sprites.append(sprite)
                if len(sprites) < 1:
                    continue
                Assets.SpriteSheets.append(SpriteSheet(sprites))

        for textureFolderName in textureFolders:

            texture_param = textureFolderName + '/' + "param.txt"
            params = {}
            with open(texture_param, "r") as file:
                lines = file.readlines()
                if len(lines) == 0:
                    print(("CRITICAL ERROR : PLEASE ADD PARAM FILE IN " + textureFolderName))
                    break
                for line in lines:
                    splited = line.split(":")
                    params[splited[0]] = splited[1]

            for textureFile in os.listdir(textureFolderName):
                if not textureFile.endswith(".txt"):
                    Assets.Sprites.append(Sprite(textureFolderName + '/' + textureFile, int(params["w"]), int(params["h"])))

    @staticmethod
    def GetSprite(ref: Enum) -> Sprite:
        return Assets.Sprites[ref.value - 1]
    
    @staticmethod
    def GetSpriteSheet(ref: Enum) -> SpriteSheet:
        # print(ref)
        return Assets.SpriteSheets[ref.value - 1]