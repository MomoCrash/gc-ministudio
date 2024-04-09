from __future__ import annotations
import pygame
import os
import json
from texture import Assets, SpritesRef, SpriteSheetsRef, SpriteSheet, Sprite
from vector import Vector2
from gameobject import GameObject


class SerializableMapObject( GameObject ):
    def __init__(
                    self,         
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spriteRef: SpritesRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    
                    interactable: bool = False
                ):
        super().__init__( position, rotation, scale, spriteDimensions, spriteRef, None, color )
        self.interatable = interactable


    def serialize(self):
        if self.spriteRenderer.spriteRef is None:
            return {'x': self.transform.position.x, 'y': self.transform.position.y, 'w': self.spriteRenderer.dimensions.x * self.transform.scale.x, "h": self.spriteRenderer.dimensions.y , 'ref': None, 'interactable': self.interatable, "text": "Default" }
        return {'x': self.transform.position.x, 'y': self.transform.position.y, 'w': self.spriteRenderer.dimensions.x * self.transform.scale.x, "h": self.spriteRenderer.dimensions.y * self.transform.scale.y, 'ref': self.spriteRenderer.spriteRef.value, 'interactable': self.interatable, "text": "Default" }

    @staticmethod
    def deserialize(json) -> SerializableMapObject:
        
        position = Vector2(json["x"], json["y"])
        dimensions = Vector2( json["w"], json["h"])
        ref = json["ref"]
        if ref is not None:
            spriteRef = SpritesRef(ref)
        else:
            spriteRef = ref

        interactable = json["interatable"]
        
        return SerializableMapObject(position, spriteDimensions=dimensions, spriteRef=spriteRef, interactable=interactable)


class Map:
    def __init__(self, map_data_file, map_w, map_h):
        self.width = map_w
        self.height = map_h

        self.background_refs: list[ int] = []
        self.colliders: list[ SerializableMapObject ] = []
        self.decors: list[ SerializableMapObject ] = []
        self.map_file = map_data_file
        self.background_sprites = []

        self.load_map()

        self.background_width = self.background_sprites[0].texture.get_width()

    def append_backgrounds(self, sprite_ref: int):
        self.background_refs.append(sprite_ref)
        self.background_sprites.append(Assets.GetSprite(SpritesRef(sprite_ref)))
        
    def create_collider(self, x, y, w, h):
        self.colliders.append( SerializableMapObject( position=Vector2( x, y ), scale=Vector2( 1, 1 ), spriteDimensions=Vector2(w, h) ) )

    def create_decoration(self, x, y, sprite_ref: SpritesRef):
        size = Assets.GetSprite(sprite_ref).size
        self.decors.append( SerializableMapObject( position=Vector2( x, y ), spriteDimensions=Vector2(size[0], size[1]), spriteRef=sprite_ref))

    def save_map(self):
        with open("Assets/Editor/" + self.map_file, "w") as file:
            json_map = {}
            json_map["backgrounds"] = [str(self.background_refs[0])]
            for i in range(1, len(self.background_refs)):
                json_map["backgrounds"].append(str(self.background_refs[i]))
            if len(self.colliders):
                json_map["colliders"] = [self.colliders[0].serialize()]
                for i in range(1, len(self.colliders)):
                    json_map["colliders"].append(self.colliders[i].serialize())
            if len(self.decors):
                json_map["gameobjects"] = [self.decors[0].serialize()]
                for i in range(1, len(self.decors)):
                    json_map["gameobjects"].append(self.decors[i].serialize())
            json.dump(json_map, file, indent=2, ensure_ascii=False)
            file.close()

    def load_map(self):
        if not os.path.exists("Assets/Editor/" + self.map_file):
            fp = open("Assets/Editor/" + self.map_file, 'x')
            fp.close()
        with open("Assets/Editor/" + self.map_file, "r") as file:
            try:
                jsonObjects = json.load(file)
            except json.decoder.JSONDecodeError:
                self.append_backgrounds(1)
                return

            print(jsonObjects)

            for backgroundRef in jsonObjects["backgrounds"]:
                self.append_backgrounds(int(backgroundRef))

            try:
                for gameObject in jsonObjects["gameobjects"]:
                    self.decors.append( SerializableMapObject.deserialize(gameObject) )
            except KeyError:
                print("No game object for map " + self.map_file)

            try:
                for colliders in jsonObjects["colliders"]:
                    self.colliders.append( SerializableMapObject.deserialize(colliders) )
            except KeyError:
                print("No colliders for map " + self.map_file)
        
    def draw( self, surface: pygame.Surface, camera: Vector2 ):
        for mapObject in self.decors:
            mapObject.update( surface, camera )
