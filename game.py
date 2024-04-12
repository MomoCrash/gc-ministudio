import pygame
import settings
from linkedlist import LinkedList
from vector import Vector2
from map import Map
from text import Text
from entity import Entity, Player, Mob
from texture import SpritesRef, SpriteSheetsRef, Sprite, SpriteSheet, Assets
from Music import Songs
from pauseUI import Menu

class Game:
    def __init__(self, screen, game_chapter, win_width, win_height, win_name, menu, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        self.dt = 1
        self.elementsOnScreen: LinkedList = LinkedList()
        self.elementsOffScreen: LinkedList = LinkedList()
        self.game_chapter = game_chapter
        self.menu = menu 

        self.map = Map("map" + str(game_chapter) + ".json", win_width, win_height)

        self.screen = screen
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 0

        self.player = Player(
                                position = Vector2( 400, 1700 ),
                                spriteDimensions = Vector2( 100, 200 )
                            )

        self.camera = Vector2( 0, 0 )

        self.text = Text(self.screen, settings.GAME_FONT, 30)

        self.loop()

    def load_next_map(self):
        self.game_chapter += 1
        self.map = Map( "map" + str(self.game_chapter) + ".json", self.width, self.height )
        self.player.transform.position = position = Vector2( 10, 1580 )

        # TODO : AJOUTER LE RESET DES MOBS

    def inputs(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if not self.map.is_showing_textbox:
                        self.map.is_showing_textbox = True
                    else:
                        self.map.is_showing_textbox = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2: 
                    self.player.Attack(self.camera)
                if event.button == 3:
                    self.player.Defence()
                if event.button == 1:
                    self.player.MeleeAttack()
            if event.type == pygame.MOUSEBUTTONUP:
                self.player.DesactivateDefence()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.menu_active = not self.menu.menu_active
        return True

    def update(self):
        pass

        
    def update_camera(self):
        self.camera.x = self.player.transform.position.x - self.width // len(self.map.background_sprites)
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width * (len(self.map.background_sprites) - 1)))
        self.camera.y = max(0, min(self.camera.y, self.height))
        

    def update_graphics(self):
        for i in range(len(self.map.background_sprites)):
            for j in range(1, len(self.map.background_sprites[i])):
                self.surface.blit(self.map.background_sprites[i][j].texture,
                                  ((i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[j]),
                                   0, self.width, self.height))
                


        self.map.draw(self.screen, self.player, self.camera)
        
        self.player.update( self.surface, self.camera, self.map.colliders, self.dt)

        self.map.update_mobs(self.screen, self.player, self.camera, self.dt)

        if self.player.getCollision(self.map.end_zone):
            self.load_next_map()
            pygame.display.flip()
            return

        self.update_camera()

        self.map.update_mobs_logic(self.screen, self.player, self.camera)

        self.player.DrawArrow(self.surface, self.camera)

        self.player.UpdateArrow(self.dt)

        for i in range(len(self.map.background_sprites)):
             if self.map.background_sprites[i][0] is not None:

                self.surface.blit(self.map.background_sprites[i][0].texture,
                                  ((i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[0]),
                                   0))

        Assets.GetSprite(SpritesRef.HP).draw(self.surface, Vector2(20, 30), Vector2(1, 1))
        if self.player.health == 6:
            Assets.GetSprite(SpritesRef.LIFE_6).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health == 5:
            Assets.GetSprite(SpritesRef.LIFE_5).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health == 4:
            Assets.GetSprite(SpritesRef.LIFE_4).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health == 3:
            Assets.GetSprite(SpritesRef.LIFE_3).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health == 2:
            Assets.GetSprite(SpritesRef.LIFE_2).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health == 1:
            Assets.GetSprite(SpritesRef.LIFE_1).draw(self.surface,Vector2(90,20),Vector2(1,1))
        elif self.player.health <= 0:
            Assets.GetSprite(SpritesRef.LIFE_0).draw(self.surface,Vector2(90,20),Vector2(1,1))

        self.text.draw_text("fps :" + str(self.fps), (255, 255, 255), 90, 100, 10, 10)
        #self.text.draw_text("Test de Text adaptatif !", (255, 255, 255), 100, 100, 10, 10)

        pygame.display.flip()

    def handle_pause_menu(self):
        menu = Menu(self.screen)
        paused = True

        while paused:
            action = menu.handle_input()
            if action == "CONTINUE":
                paused = False
            elif action == "QUIT":
                pygame.quit()
                quit()

            self.screen.fill((255, 255, 255))
            menu.draw()
            pygame.display.flip()

        return paused

    def loop(self):
        running = True
        paused = False

        while running:

            if not paused:
                running = self.inputs()
                self.update()  
                self.update_graphics()
            else:            
                self.menu.handle_input()  
                if self.menu.menu_active:
                    self.screen.blit(self.menu.book_background, (self.menu.book_x, self.menu.book_y))
                    menu_button_rect = self.screen.blit(self.menu.menu_button, (10, 10))
                    self.menu.continue_button_rect.draw()
                    self.menu.options_button_rect.draw()
                    self.menu.quit_button_rect.draw()
                else:
                    paused = False
                pygame.display.flip()

            self.clock.tick()
            self.dt = (self.clock.get_time()) / 1000.0

            self.fps = 1 / self.dt
            
            if self.menu.menu_active:
                paused = True
                
        pygame.quit()
