import pygame
from map import Map
from texture import *
from player import *
import json


class SerializableObject:
    def __init__(self,x,y,ref: Enum,is_trigger):
        self.x: int = x
        self.y: int = y
        self.sprite_ref = ref
        self.is_trigger = is_trigger
        
    def to_json(self):
        return json.dumps({'x': self.x, 'y':self.y, 'ref':self.sprite_ref.value, 'is_trigger': self.is_trigger})
        

class Editor:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps

        self.map = Map(self, win_width, win_height)
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(100, 100, 40, 80)
        self.camera = pygame.Vector2(0, 0)
        
        self.decal_x = self.player.rect_transform.x
        self.game_objects: list[SerializableObject] = []
        
        self.selected_sprite = SpritesRef.BACKGROUND_1
        
        self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]

        self.loop()
        
    def write_to_file(self):
        f = open("Assets/Editor/map1.txt", "w")
        f.write("{[")
        f.write(self.game_objects[0].to_json())
        for i in range(1, len(self.game_objects)):
            f.write("," + self.game_objects[i].to_json())
        f.write("]}")
        f.close()

    def inputs(self) -> bool:
        
        pressed_key = pygame.key.get_pressed()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
        if pressed_key[pygame.K_s]:
            self.write_to_file()
        
        if pressed_key[pygame.K_RIGHT]:
            self.player.rect_transform.x += 5
            if self.decal_x >= (self.width // 4):
                self.decal_x += 5
        elif  pressed_key[pygame.K_LEFT]:
            self.player.rect_transform.x -= 5
            if self.decal_x >= (self.width // 4):
                self.decal_x -= 5
        elif  pressed_key[pygame.K_DOWN]:
            self.player.rect_transform.y += 5
        elif  pressed_key[pygame.K_UP]:
            self.player.rect_transform.y -= 5


        self.camera.x = self.player.rect_transform.x - self.width // 4
        self.camera.y = self.player.rect_transform.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))
        
        for mapObject in self.map.elements:
            mapObject.rect_transform.x = mapObject.position.x - self.camera.x

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    object = SerializableObject(self.decal_x + self.mouse_x, self.mouse_y, self.selected_sprite, 1)
                    self.game_objects.append(object)
                if event.button == 0:
                    pass
            
            if event.type == pygame.MOUSEWHEEL:
                print(event.y)
                if event.y > 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value + 1) % len(SpritesRef) + 1)
                if event.y < 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value - 1) % len(SpritesRef) + 1)
                
        return True

    def update_graphics(self):

        self.map.draw(self.surface)
        pygame.draw.rect(self.screen, (0,0,0),
                         pygame.Rect(0, 0, self.width, self.height))

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))
       
        # Draw the player flipped on the good side
        if self.player.IsFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)

        Assets.GetResizedSprite(self.selected_sprite, 100, 100).draw(self.surface, (self.mouse_x, self.mouse_y, 100, 100))

        for object in self.game_objects:
            Assets.GetResizedSprite(object.sprite_ref, 100, 100).draw(self.surface, (object.x - self.decal_x, object.y, 100, 100))


        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            running = self.inputs()

            for mapObject in self.map.elements:
                self.player.check_collision(mapObject.rect_transform)

            self.update_graphics()

            self.clock.tick(60)
            
        pygame.quit()
        