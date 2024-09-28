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

        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(
                                position = Vector2( 0, 1580 ),
                                spriteDimensions = Vector2( 60, 190 ),
                                gravity=0,
            jumpHeight=2000

                            )
        self.camera = Vector2(self.player.transform.position.x, 0)

        self.drawing_collision = False
        self.drawing_end_zone = False
        self.collision_start = Vector2(0,0)
        self.end_zone_start = Vector2(0,0)
        
        self.selected_sprite = SpritesRef(1)

        self.map = Map("map0.json", win_width, win_height)
        self.dt = 0
        self.current_dt = 0

        self.loop()

    def inputs(self) -> bool:

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.map.is_showing_textbox:
                        self.map.is_showing_textbox = False
                    else:
                        self.map.is_showing_textbox = True
                if event.key == pygame.K_f:
                    if self.player.gravity == 0:
                        self.player.gravity = 170
                    else:
                        self.player.gravity = 0
                if event.key == pygame.K_m:
                    self.map.append_mob(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y)
                if event.key == pygame.K_t:
                    self.player.transform.position = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y)
                if event.key == pygame.K_s:
                    self.map.save_map()
                if event.type == pygame.K_ESCAPE :
                    return False
                if event.key == pygame.K_DELETE:
                    mouseObject = GameObject(position=Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y), spriteDimensions=Vector2(10, 10))
                    has_removed = False
                    for mob in self.map.mobs:
                        if mob.getCollision( mouseObject ):
                            self.map.remove_mob(mob)
                            break
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
                if event.button == 2:
                    self.drawing_end_zone = True
                    # print(self.mouse_x + self.camera.x)
                    self.end_zone_start = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y)
                if event.button == 3:
                    self.drawing_collision = True
                    # print(self.mouse_x + self.camera.x)
                    self.collision_start = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.drawing_end_zone = False

                    distance: Vector2 = Vector2(self.mouse_x + self.camera.x,
                                                self.mouse_y + self.camera.y) - self.end_zone_start

                    self.map.set_end(self.end_zone_start.x, self.end_zone_start.y,
                                             w=distance.x, h=distance.y)
                if event.button == 3:
                    self.drawing_collision = False

                    distance: Vector2 = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y) - self.collision_start

                    self.map.create_collider(self.collision_start.x, self.collision_start.y,
                                             w=distance.x, h=distance.y)

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value + 1) % len(SpritesRef) + 1)
                if event.y < 0:
                    self.selected_sprite = SpritesRef((self.selected_sprite.value - 2) % len(SpritesRef) + 1)

        return True

    def update_camera(self):
        self.camera.x = self.player.transform.position.x - self.width // len(self.map.background_sprites)
        self.camera.y = self.player.transform.position.y - self.height // 20

        self.camera.x = max(0, min(self.camera.x, self.width * (len(self.map.background_sprites) - 1)))
        self.camera.y = max(0, min(self.camera.y, self.height))

    def update(self):

        pygame.draw.rect(self.screen, (0,0,0),
                         pygame.Rect(0, 0, self.width, self.height))

        for i in range(len(self.map.background_sprites)):
            for j in range(1, len(self.map.background_sprites[i])):
                self.surface.blit(self.map.background_sprites[i][j].texture,
                                  ((i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[j]), 0))

        self.map.draw(self.surface, self.player, self.camera, True)
        self.map.end_zone.update(self.screen, self.camera)

        self.player.update( self.surface, self.camera, self.map.colliders, self.dt )

        self.map.update_mobs(self.screen, self.player, self.camera, self.dt)

        self.update_camera()
        
        Assets.GetSprite(self.selected_sprite).draw(self.surface, Vector2(self.mouse_x, self.mouse_y), Vector2(100, 100))
        
        if self.drawing_collision:
            distance: Vector2 = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y) - self.collision_start
            pygame.draw.rect(self.screen, (0, 200, 0, 120), (self.collision_start.x - self.camera.x, self.collision_start.y - self.camera.y, distance.x, distance.y))

        if self.drawing_end_zone:
            distance: Vector2 = Vector2(self.mouse_x + self.camera.x, self.mouse_y + self.camera.y) - self.end_zone_start
            pygame.draw.rect(self.screen, (0, 0, 255, 120), (self.end_zone_start.x - self.camera.x, self.end_zone_start.y - self.camera.y, distance.x, distance.y))

        for i in range(len(self.map.background_sprites)):
            if self.map.background_sprites[i][0] is not None:
                self.surface.blit(self.map.background_sprites[i][0].texture,
                                  ((i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[0]),
                                   0))


        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            running = self.inputs()

            self.update()

            self.dt = self.clock.tick() / 1000
            self.current_dt += self.dt

        self.map.save_map()
        pygame.quit()
        