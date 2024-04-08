from __future__ import annotations
import pygame
import json
from texture import Assets, SpritesRef, SpriteSheetsRef, SpriteSheet, Sprite
from vector import Vector2
from gameobject import GameObject


class SerializableMapObject(GameObject):
    def __init__(
            self,
            position: Vector2 = Vector2(0, 0),
            rotation: Vector2 = Vector2(0, 0),
            scale: Vector2 = Vector2(1, 1),
            dimensions: Vector2 = Vector2(10, 10),

            ref: SpritesRef = None,
    ):
        super().__init__(position, rotation, scale, spriteDimensions=dimensions)
        self.sprite_ref = ref
        if self.sprite_ref is not None:
            self.sprite = Assets.GetSprite(self.sprite_ref)
        self.is_trigger = False
        self.initial_position: Vector2 = Vector2(position.x, position.y)

    def serialize(self):
        if self.sprite_ref is None:
            return json.dumps(
                {'x': self.initial_position.x, 'y': self.initial_position.y, 'w': self.spriteDimensions.x, "h": self.spriteDimensions.y, 'ref': None, 'is_trigger': None})
        return json.dumps({'x': self.initial_position.x, 'y': self.initial_position.y, 'w': self.spriteDimensions.x, "h": self.spriteDimensions.y, 'ref': self.sprite_ref.value,
                           'is_trigger': None})

    @staticmethod
    def deserialize(mapobject: SerializableMapObject, json):
        mapobject.transform.position.x = json["x"]
        mapobject.transform.position.y = json["y"]

        mapobject.initial_position = Vector2( json["x"], json["y"])
        mapobject.spriteDimensions = Vector2( json["w"], json["h"])

        if json["ref"] is None:
            mapobject.sprite_ref = None
            mapobject.sprite = None
        else:
            mapobject.sprite_ref = SpritesRef(json["ref"])
            mapobject.sprite = Assets.GetSprite(mapobject.sprite_ref)
        mapobject.is_trigger = json["is_trigger"]


class Map:
    def __init__(self, map_data_file, map_w, map_h):
        self.width = map_w
        self.height = map_h

        self.background_refs: list[int] = []
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
        self.colliders.append( SerializableMapObject( position=Vector2( x, y ), scale=Vector2( 1, 1 ), dimensions=Vector2(w, h) ) )

    def create_decoration(self, x, y, sprite_ref: SpritesRef):
        size = Assets.GetSprite(sprite_ref).size
        self.decors.append( SerializableMapObject( position=Vector2( x, y ), dimensions=Vector2(size[0], size[1]), ref=sprite_ref))

    def save_map(self):
        with open("Assets/Editor/" + self.map_file, "w") as f:
            f.write('{"backgrounds": [')
            f.write(str(self.background_refs[0]))
            for i in range(1, len(self.background_refs)):
                f.write("," + str(self.background_refs[i]))
            if len(self.colliders):
                f.write('], "colliders": [')
                f.write(self.colliders[0].serialize())
                for i in range(1, len(self.colliders)):
                    f.write("," + self.colliders[i].serialize())
            if len(self.decors):
                f.write('], "gameobjects": [')
                f.write(self.decors[0].serialize())
                for i in range(1, len(self.decors)):
                    print(self.decors[i].serialize())
                    f.write("," + self.decors[i].serialize())
                f.write("]")
            f.write("}")
            f.close()

    def load_map(self):
        with open("Assets/Editor/" + self.map_file, "r") as txt_file:
            line = txt_file.readline()
            print(line)
            if line == "":
                self.append_backgrounds(1)
                return
            try:
                jsonObjects = json.loads(line)
            except json.decoder.JSONDecodeError:
                self.append_backgrounds(1)
                return

            for backgroundRef in jsonObjects["backgrounds"]:
                self.append_backgrounds(int(backgroundRef))

            try:
                for gameObject in jsonObjects["gameobjects"]:
                    object = SerializableMapObject()
                    SerializableMapObject.deserialize(object, gameObject)
                    print(object.serialize())
                    self.decors.append( object )
            except KeyError:
                print("No game object for map " + self.map_file)

            try:
                for colliders in jsonObjects["colliders"]:
                    object = SerializableMapObject()
                    SerializableMapObject.deserialize(object, colliders)
                    self.colliders.append( object )
            except KeyError:
                print("No colliders for map " + self.map_file)
        
    def draw(self, surface: pygame.Surface):
        for mapObject in self.decors:
            mapObject.draw(surface, (0, 0, 0))
