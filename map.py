from __future__ import annotations
import pygame
import os
import json

import settings
from texture import Assets, SpritesRef, SpriteSheetsRef, SpriteSheet, Sprite
from vector import Vector2
from gameobject import GameObject
from ui import InfoBox
from entity import Mob

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
        super().__init__( position, rotation, scale, spriteDimensions, spriteRef=spriteRef, color=color )
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

        interactable = json["interactable"]
        
        return SerializableMapObject(position, spriteDimensions=dimensions, spriteRef=spriteRef, interactable=interactable)


class Map:
    def __init__(self, map_data_file, map_w, map_h):
        self.width = map_w
        self.height = map_h

        self.colliders: list[ SerializableMapObject ] = []
        self.decors: list[ SerializableMapObject ] = []
        self.map_file = map_data_file

        self.background_refs: list[list[int]] = [[]]
        self.background_sprites: list[list[Sprite]] = [[]]

        self.end_zone = SerializableMapObject( Vector2(0,0), Vector2(0,0), Vector2(1,1), spriteDimensions=Vector2(0,0) )
        self.is_showing_textbox = False

        self.parralax_speed = []
        self.mobs = [Mob(
            position=Vector2( 400, 1810 ),
            spriteDimensions = Vector2( 100, 200 )
            ),
            Mob(
                position=Vector2(1100, 1810),
                spriteDimensions=Vector2(100, 200)
            )
        ]

        self.load_map()

        self.background_width = self.background_sprites[0][1].texture.get_width()

    def append_mob(self, x, y):
        self.mobs.append(Mob[Mob(
            position=Vector2(x, y),
            spriteDimensions=Vector2(100, 200)
        )])

    def remove_mob(self, mob: Mob):
        self.mobs.remove(mob)

    def append_backgrounds(self, layer, sprite_ref: str):
        if len(self.background_refs) <= layer: self.background_refs.append([])
        if len(self.background_sprites) <= layer: self.background_sprites.append([])
        if sprite_ref is None:
            self.background_refs[layer].append(None)
            self.background_sprites[layer].append(None)
            return
        self.background_refs[layer].append(int(sprite_ref))
        self.background_sprites[layer].append(Assets.GetSprite(SpritesRef(int(sprite_ref))))

    def create_collider(self, x, y, w, h):
        self.colliders.append( SerializableMapObject( position=Vector2( x, y ), scale=Vector2( 1, 1 ), spriteDimensions=Vector2(w, h) ) )

    def set_end(self, x, y, w, h):
        self.end_zone = SerializableMapObject( position=Vector2( x, y ), scale=Vector2( 1, 1 ), spriteDimensions=Vector2(w, h) )

    def create_decoration(self, x, y, sprite_ref: SpritesRef):
        size = Assets.GetSprite(sprite_ref).size
        # print(sprite_ref)
        self.decors.append( SerializableMapObject( position=Vector2( x, y ), spriteDimensions=Vector2(size[0], size[1]), spriteRef=sprite_ref))

    def save_map(self):
        with open("Assets/Editor/" + self.map_file, "w") as file:
            json_map = {}
            json_map["parralax_speed"] = self.parralax_speed
            json_map["end_zone"] = self.end_zone.serialize()
            json_map["backgrounds"] = self.background_refs

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
                self.append_backgrounds(0, 1)
                return

            if "parralax_speed" in jsonObjects:
                self.parralax_speed = jsonObjects["parralax_speed"]
            else:
                self.parralax_speed = [0.4, 0.5, 0.8, 1, 1]

            # print(jsonObjects)
            if "end_zone" in jsonObjects:
                self.end_zone = SerializableMapObject.deserialize(jsonObjects["end_zone"])

            for i in range(len(jsonObjects["backgrounds"])):
                for backgroundRef in jsonObjects["backgrounds"][i]:
                    self.append_backgrounds(i, backgroundRef)

            try:
                for gameObject in jsonObjects["gameobjects"]:
                    # print(gameObject)
                    self.decors.append( SerializableMapObject.deserialize(gameObject) )
            except KeyError:
                print("No game object for map " + self.map_file)

            try:
                for colliders in jsonObjects["colliders"]:
                    self.colliders.append( SerializableMapObject.deserialize(colliders) )
            except KeyError:
                print("No colliders for map " + self.map_file)

    def update_mobs(self, screen: pygame.surface, player, camera: Vector2, dt):
        for mob in self.mobs:
            mob.DamagePlayer(player, self.colliders)
            mob.update(dt, screen, camera, self.colliders, player)

    def update_mobs_logic(self, screen: pygame.surface, player, camera: Vector2):
        deadMobs = []
        for i, mob in enumerate(self.mobs):
            mob.tryThrow(player, camera)
            mob.tryAttack(player)
            mob.tryDefence(player)
            player.DamageEnnemy(mob)

            if mob.IsDead and mob.hammer is None:
                deadMobs.append(i)
                continue

            mob.drawHammer(screen, player, camera)

        for i in deadMobs:
            self.mobs.pop(i)
        
    def draw( self, screen: pygame.Surface, player, camera: Vector2, editor: bool = False ):
        for mapObject in self.decors:
            # print(mapObject.spriteRenderer.spriteSheetRef)
            mapObject.update( screen, camera )
        if editor:
            for collider in self.colliders:
                collider.update( screen, camera )

        infos_box = [InfoBox(screen, 200, 1580, 400, 400)]

        for box in infos_box:
            if box.is_on_player(player):
                box.show_popup = True
                if self.is_showing_textbox:
                    box.big_popup = True
                    box.draw("Petit text en sblit", (0,0,0), (255,255,255))
                else:
                    box.big_popup = False
                    box.text.draw_text("Appuie sur E pour découvrir l'histoire", (255, 255, 255), 800, 500, 20, 20)
            else:
                box.show_popup = False
                self.is_showing_textbox = False
