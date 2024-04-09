import pygame
from vector import Vector2
from map import Map
from entity import Player
from gameobject import GameObject
from texture import SpritesRef, SpriteSheetsRef, Assets
        

class Editor:
    def __init__(self, screen, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(
                                position = Vector2( 0, 0 ),
                                walkingLeftSpriteSheetRef = SpriteSheetsRef.PLAYER_WALK_LEFT,
                                walkingRightSpriteSheetRef = SpriteSheetsRef.PLAYER_WALK_RIGHT,
                                spriteDimensions = Vector2( 40, 80 ),
                                gravity=0
                            )
        self.camera = Vector2(self.player.transform.position.x, 0)

        self.drawing_collision = False
        self.collision_start = Vector2(0,0)
        
        self.selected_sprite = SpritesRef(1)

        self.map = Map("map1.json", win_width, win_height)

        self.loop()

    def inputs(self) -> bool:

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.gravity = 5
                if event.key == pygame.K_s:
                    self.map.save_map()
                if event.key == pygame.K_DELETE:
                    mouseObject = GameObject(position=Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y), spriteDimensions=Vector2(10, 10))
                    has_removed = False
                    for mapObject in self.map.colliders:
                        if mapObject.getCollision( mouseObject ):
                            self.map.colliders.remove(mapObject)
                            has_removed = True
                            break
                    if has_removed: break
                    for mapObject in self.map.decors:
                        if mapObject.getCollision(mouseObject):
                            self.map.decors.remove(mapObject)
                            break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.map.create_decoration(self.camera.x + self.mouse_x, self.mouse_y + self.camera.y, self.selected_sprite)
                if event.button == 3:
                    self.drawing_collision = True
                    print(self.mouse_x + self.camera.x)
                    self.collision_start = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.drawing_collision = False

                    distance: Vector2 = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y).removeToNew(self.collision_start)

                    self.map.create_collider(self.collision_start.x, self.collision_start.y,
                                             w=distance.x, h=distance.y)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value + 1) % len(SpritesRef) + 1)
                if event.y < 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value - 2) % len(SpritesRef) + 1)

        return True

    def update_camera(self):
        self.camera.x = self.player.transform.position.x - self.width // 4
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))

    def update(self):

        pygame.draw.rect(self.screen, (0,0,0),
                         pygame.Rect(0, 0, self.width, self.height))

        for i, segment in enumerate(self.map.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, self.height - self.camera.y))

        self.map.draw(self.surface, self.camera, True)
        
        self.player.update( self.surface, self.camera, self.map.colliders )

        self.update_camera()
        
        Assets.GetSprite(self.selected_sprite).draw(self.surface, Vector2(self.mouse_x, self.mouse_y), Vector2(100, 100))
        
        if self.drawing_collision:
            distance: Vector2 = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y).removeToNew(self.collision_start)
            pygame.draw.rect(self.screen, (0, 200, 0, 120), (self.collision_start.x - self.camera.x, self.collision_start.y - self.camera.y, distance.x, distance.y))

        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            running = self.inputs()

            self.update()

            self.clock.tick(60)
            
        pygame.quit()
        