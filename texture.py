import pygame
import os
import settings
from vector import Vector2
from enum import Enum, auto

class SpritesRef(Enum):

    BOOK = auto()
    START = auto()

    # 2
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

    #15
    BG_LEVEL_2_1 = auto()
    BG_LEVEL_2_2 = auto()

    BG_LEVEL_2_3 = auto()
    BG_LEVEL_2_4 = auto()

    BG_LEVEL_2_5 = auto()
    BG_LEVEL_2_6 = auto()

    BG_LEVEL_2_7 = auto()
    BG_LEVEL_2_8 = auto()

    BG_LEVEL_2_9 = auto()
    BG_LEVEL_2_10 = auto()

    BG_LEVEL_3_1 = auto()
    BG_LEVEL_3_2 = auto()

    LIFE_5 = auto()
    LIFE_4 = auto()
    LIFE_3 = auto()
    LIFE_2 = auto()
    LIFE_1 = auto()
    LIFE_0 = auto()
    LIFE_6 = auto()
    HP = auto()
    
    #25
    LVL1_LOG = auto()
    LVL1_ROCK_1 = auto()
    LVL1_ROCK_2 = auto()
    LVL1_ROCK_3 = auto()
    LVL1_ROCK_4 = auto()
    LVL1_ROCK_SIDE = auto()
    LVL1_ROCK_FACE = auto()
    LVL1_STUMP = auto()
    TEST = auto()

    LVL2_BARIL = auto()
    LVL2_CAISSE = auto()

    LVL3_OS = auto()
    LVL3_SKULL = auto()
    LVL3_SKULL_2 = auto()
    LVL3_STATUE = auto()
    LVL1_TOMBSTONE = auto()
    LVL3_SWORD = auto()
    LVL3_SWORD_1 = auto()

    TOMAHAWK = auto()

    KEY_ART = auto()
    POPUP = auto()

    CHECK_BUTTON = auto()
    UNCHECK_BUTTON = auto()


class SpriteSheetsRef(Enum):
    ENNEMY_ATTACK_LEFT = auto()
    ENNEMY_ATTACK_RIGHT = auto()
    ENNEMY_GET_HIT_LEFT = auto()
    ENNEMY_GET_HIT_RIGHT = auto()
    ENNEMY_IDLE_LEFT = auto()
    ENNEMY_IDLE_RIGHT = auto()
    ENNEMY_WALK_LEFT = auto()
    ENNEMY_WALK_RIGHT = auto()
    ENNEMY_SHIELD_LEFT = auto()
    ENNEMY_SHIELD_RIGHT = auto()


    PLAYER_ATTACK_LEFT = auto()
    PLAYER_ATTACK_RIGHT = auto()
    DEAD_LEFT = auto()
    DEAD_RIGHT = auto()
    DEATH_LEFT = auto()
    DEATH_RIGHT = auto()
    PLAYER_GET_HIT_LEFT = auto()
    PLAYER_GET_HIT_RIGHT = auto()
    PLAYER_IDLE_LEFT = auto()
    PLAYER_IDLE_RIGHT = auto()
    PLAYER_JUMP_LEFT = auto()
    PLAYER_JUMP_RIGHT = auto()
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
        self.frame_per_image = settings.ANIMATION_DURATION / self.frame_count
        self.textures = textures
        self.current_index = 0

        self.total_ticks = 0
        self.next_image = 0

        self.callback: function = None

    # TODO: RANDOM FIRST FRAME / DELAY
    def draw( self, ticks, surface: pygame.Surface, position: Vector2, scale: Vector2, func = lambda: 0 ):
        self.callback = func
        self.total_ticks += ticks
        if self.is_next_frame(ticks):
            self.current_index += 1
            if self.current_index >= self.frame_count:
                self.callback()
                self.current_index = 0
            self.next_image = self.total_ticks + self.frame_per_image


        self.textures[self.current_index].draw( surface, position, scale )
    
    def is_next_frame(self, current_ticks) -> bool:
        if self.total_ticks > self.next_image:
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