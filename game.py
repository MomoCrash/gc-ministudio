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
        self.dt = 0
        self.current_dt = 0
        self.elementsOnScreen: LinkedList = LinkedList()
        self.elementsOffScreen: LinkedList = LinkedList()
        self.game_chapter = game_chapter
        self.menu = menu 

        self.map = Map("map" + str(game_chapter) + ".json", win_width, win_height)

        pygame.init()
        self.screen = screen
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(
                                position = Vector2( 1000, 500 ),
                                spriteDimensions = Vector2( 40, 80 )
                            )
        self.mob = Mob( 
            position=Vector2( 500, 500 ),
            spriteDimensions = Vector2( 40, 80 )
            )
        self.camera = Vector2( 0, 0 )

        self.text = Text(self.screen, settings.GAME_FONT, 21)

        self.loop()

    def load_next_map(self):
        self.game_chapter += 1
        self.map = Map("map" + str(self.game_chapter) + ".json", self.width, self.height)
        self.player.transform.position = position = Vector2(10, 1580)

    def inputs(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.player.Attack()
                if event.button == 3:
                    self.player.Defence()
                if event.button == 2:
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
        self.camera.x = self.player.transform.position.x - self.width // 4
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))

    def update_graphics(self):
        for i in range(len(self.map.background_sprites)):
            for j in range(1, len(self.map.background_sprites[i])):
                self.surface.blit(
                    self.map.background_sprites[i][j].texture,
                    (
                        (i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[j]),
                        self.height - self.camera.y,
                        self.width,
                        self.height
                    )
                )

        self.map.draw(self.screen, self.camera)

        self.mob.DamagePlayer(self.player)
        self.player.update(self.surface, self.camera, self.map.colliders, self.dt)

        self.update_camera()

        self.mob.movement(self.player, self.dt, self.map.colliders)


        self.mob.tryThrow(self.player)
        self.mob.tryAttack(self.player)
        self.mob.tryDefence(self.player)
        self.player.DamageEnnemy(self.mob)
        self.mob.update(self.dt, self.surface, self.camera, self.map.colliders)
        self.mob.draw(self.surface, self.player)

        self.player.DrawArrow(self.surface, self.camera)

        self.player.UpdateArrow(self.dt)

        self.text.draw_text("fps :" + str(self.clock.get_fps()), (255, 255, 255), 100, 100, 10, 10)

        for i in range(len(self.map.background_sprites)):
            self.surface.blit(
                self.map.background_sprites[i][0].texture,
                (
                    (i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[0]),
                    self.height - self.camera.y
                )
            )

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
            dt_start = pygame.time.get_ticks()
            
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

            self.clock.tick(60)
            dt_end = pygame.time.get_ticks()
            self.dt = self.clock.get_time() / 1000
            self.current_dt += self.dt
            
            if self.menu.menu_active:
                paused = True
                
        pygame.quit()

