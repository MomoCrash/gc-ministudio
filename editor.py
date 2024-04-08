import pygame
from vector import Vector2
from map import Map
from entity import Player
from gameobject import GameObject
from texture import SpritesRef, SpriteSheetsRef, Sprite, SpriteSheet, Assets
        

class Editor:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player( position=Vector2( 0, 0 ), scale=Vector2( 40, 80 ) )
        self.camera = pygame.Vector2(0, 0)
        
        self.decal_x = self.player.transform.position.x

        self.drawing_collision = False
        self.collision_start = (0, 0)
        
        self.selected_sprite = SpritesRef(1)

        self.map = Map("map1.txt", win_width, win_height)

        self.loop()

    def inputs(self) -> bool:
        
        pressed_key = pygame.key.get_pressed()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
        if pressed_key[pygame.K_RIGHT]:
            self.player.transform.position.x += 5
            if self.player.transform.position.x >= (self.width // 4):
                self.decal_x += 5
        elif  pressed_key[pygame.K_LEFT]:
            self.player.transform.position.x -= 5
            if self.player.transform.position.x >= (self.width // 4):
                self.decal_x -= 5
        elif  pressed_key[pygame.K_DOWN]:
            self.player.transform.position.y += 5
        elif  pressed_key[pygame.K_UP]:
            self.player.transform.position.y -= 5

        self.camera.x = self.player.transform.position.x - self.map.width // 4
        self.camera.y = self.player.transform.position.y - self.map.height // 4

        self.camera.x = max(0, min(self.camera.x, self.map.width))
        self.camera.y = max(0, min(self.camera.y, self.height))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.map.save_map()
                if event.key == pygame.K_DELETE:
                    mouseObject = GameObject(position=Vector2(self.mouse_x, self.mouse_y), spriteDimensions=Vector2(10, 10))
                    for mapObject in self.map.colliders:
                        if mapObject.getCollision( mouseObject ):
                            self.map.colliders.remove(mapObject)
                            break
                    for mapObject in self.map.decors:
                        print(mapObject.transform.position.x)
                        print(mouseObject.transform.position.x)
                        if mapObject.getCollision(mouseObject):
                            self.map.decors.remove(mapObject)
                            break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.map.create_decoration(self.decal_x + self.mouse_x, self.mouse_y, self.selected_sprite)
                if event.button == 3:
                    self.drawing_collision = True
                    self.collision_start = (self.mouse_x, self.mouse_y)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.drawing_collision = False
                    
                    collider_w = (self.mouse_x - self.decal_x) - (self.collision_start[0]-self.decal_x)
                    collider_h = self.mouse_y - self.collision_start[1]

                    self.map.create_collider(self.decal_x + self.collision_start[0], self.collision_start[1], w=collider_w, h=collider_h)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value + 1) % len(SpritesRef) + 1)
                if event.y < 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value - 2) % len(SpritesRef) + 1)

        for mapObject in self.map.decors:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        for mapObject in self.map.colliders:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        return True

    def update_graphics(self):

        pygame.draw.rect(self.screen, (0,0,0),
                         pygame.Rect(0, 0, self.width, self.height))

        for i, segment in enumerate(self.map.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))
        
        for mapDecor in self.map.decors:
            mapDecor.draw(self.screen, (0, 255, 0))

        for collider in self.map.colliders:
            collider.draw(self.screen, (0, 255, 0))

        # Draw the player flipped on the good side
        if self.player.isFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.player.transform.position, self.player.transform.scale)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.player.transform.position, self.player.transform.scale)

        self.map.draw(self.surface)

        Assets.GetSprite(self.selected_sprite).draw(self.surface, Vector2(self.mouse_x, self.mouse_y), Vector2(100, 100))
        
        if self.drawing_collision:
            pygame.draw.rect(self.screen, (0, 200, 0, 120), (self.collision_start[0], self.collision_start[1], self.mouse_x - self.collision_start[0], self.mouse_y - self.collision_start[1]))

        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            running = self.inputs()

            self.update_graphics()

            self.clock.tick(60)
            
        pygame.quit()
        