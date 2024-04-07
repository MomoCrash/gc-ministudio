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
            json_object=""
    ):
        super().__init__(position, rotation, scale, spriteDimensions=dimensions)
        self.sprite_ref = ref
        self.json_object = json_object
        self.is_trigger = False

    def serialize(self):
        if self.sprite_ref is None:
            return json.dumps(
                {'x': self.transform.position.x, 'y': self.transform.position.y, 'w': self.transform.scale.x, "h": self.transform.scale.y, 'ref': None, 'is_trigger': None})
        return json.dumps({'x': self.transform.position.x, 'y': self.transform.position.y, 'w': self.transform.scale.x, "h": self.transform.scale.y, 'ref': self.sprite_ref.value,
                           'is_trigger': None})

    def deserialize(self):
        self.transform.position.x = self.json_object["x"]
        self.transform.position.y = self.json_object["y"]
        self.transform.scale.x = self.json_object["w"]
        self.transform.scale.y = self.json_object["h"]
        if self.json_object["ref"] is None:
            self.sprite_ref = None
        else:
            self.sprite_ref = SpritesRef(self.json_object["ref"])
        self.is_trigger = self.json_object["is_trigger"]
        return self


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
        self.colliders.append( SerializableMapObject( position=Vector2( x, y ), scale=Vector2( w, h ) ) )

    def create_decoration(self, x, y, sprite_ref: SpritesRef):
        self.decors.append( SerializableMapObject( position=Vector2( x, y ), ref=sprite_ref))

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
                    print(i)
                    f.write("," + self.colliders[i].serialize())
            if len(self.decors):
                f.write('], "gameobjects": [')
                f.write(self.decors[0].serialize())
                for i in range(1, len(self.decors)):
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
                    self.decors.append( SerializableMapObject(json_object=gameObject).deserialize() )
            except KeyError:
                print("No game object for map " + self.map_file)

            try:
                for colliders in jsonObjects["colliders"]:
                    self.colliders.append( SerializableMapObject(json_object=colliders).deserialize() )
            except KeyError:
                print("No colliders for map " + self.map_file)
        
    def draw(self, surface: pygame.Surface):
        for mapObject in self.decors:
            mapObject.draw(surface, (0, 0, 0))
