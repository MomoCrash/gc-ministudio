import pygame
from map import Map
from texture import *
from player import *
import json


class SerializableObject:
    def __init__(self,x,y,w=0,h=0,ref: Enum=1,is_trigger=True):
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
        self.sprite_ref = ref
        self.is_trigger = is_trigger
        
    def to_json(self):
        if self.sprite_ref is None:
            return json.dumps({'x': self.x, 'y':self.y, 'ref':None, 'is_trigger': self.is_trigger})
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

        self.player = Player(self.width//2, self.height//2, 40, 80)
        self.camera = pygame.Vector2(0, 0)
        
        self.decal_x = self.player.position.x
        self.game_objects: list[SerializableObject] = []
        
        self.drawing_collision = False
        self.collision_start = (0, 0)
        
        self.selected_sprite = SpritesRef.EDITOR_BACKGROUND_0
        
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
            if self.player.rect_transform.x >= (self.width // 4):
                self.decal_x += 5
        elif  pressed_key[pygame.K_LEFT]:
            self.player.rect_transform.x -= 5
            if self.player.rect_transform.x >= (self.width // 4):
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
                    object = SerializableObject(self.decal_x + self.mouse_x, self.mouse_y, ref=self.selected_sprite, is_trigger=True)
                    self.game_objects.append(object)
                if event.button == 3:
                    self.drawing_collision = True
                    self.collision_start = (self.mouse_x, self.mouse_y)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.drawing_collision = False
                    
                    collider_w = self.mouse_x - self.collision_start[0]
                    collider_h = self.mouse_y - self.collision_start[1]
                    
                    object = SerializableObject(self.decal_x + self.collision_start[0], self.collision_start[1], w=collider_w, h=collider_h, ref=None, is_trigger=True)
                    self.game_objects.append(object)
                    
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value//2 + 1) % len(SpritesRef)//2 + len(SpritesRef)//2 + 1)
                if event.y < 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value//2 - 1) % len(SpritesRef)//2 + len(SpritesRef)//2 + 1)
                
        return True

    def update_graphics(self):

        self.map.draw(self.surface)
        pygame.draw.rect(self.screen, (0,0,0),
                         pygame.Rect(0, 0, self.width, self.height))

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))
            
        Assets.GetSprite(self.selected_sprite).draw(self.surface, (self.mouse_x, self.mouse_y, 100, 100))
        
        for object in self.game_objects:
            if object.sprite_ref is not None:
                Assets.GetSprite(object.sprite_ref).draw(self.surface, (object.x - self.decal_x, object.y, 100, 100))
            else:
                pygame.draw.rect(self.screen, (0, 255, 0), (object.x - self.decal_x, object.y, object.x + object.w, object.y + object.h))
       
        # Draw the player flipped on the good side
        if self.player.IsFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)
            
        
        if self.drawing_collision:
            print("Draw")
            pygame.draw.rect(self.screen, (0, 255, 0), (self.collision_start[0], self.collision_start[1], self.mouse_x - self.collision_start[0], self.mouse_y - self.collision_start[1]))

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
        