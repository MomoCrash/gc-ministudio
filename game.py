import pygame

import settings
from linkedlist import LinkedList
from vector import Vector2
from map import Map
from text import Text
from entity import Entity, Player, Mob
from texture import SpritesRef, SpriteSheetsRef, Sprite, SpriteSheet, Assets
from Music import Songs


class Game:
    def __init__(self, screen, game_chapter, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        self.dt = 0
        self.current_dt = 0
        self.elementsOnScreen: LinkedList = LinkedList()
        self.elementsOffScreen: LinkedList = LinkedList()
        self.game_chapter = game_chapter
        self.music_manager = Songs()

        self.map = Map( "map" + str(game_chapter) + ".json", win_width, win_height )
        
        pygame.init()
        self.screen = screen
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(
                                position = Vector2( 400, 1700 ),
                                spriteDimensions = Vector2( 100, 200 )
                            )
        self.mob = Mob( 
            position=Vector2( 400, 1500 ),
            spriteDimensions = Vector2( 100, 200 )
            )
        self.camera = Vector2( 0, 0 )

        self.text = Text(self.screen, settings.GAME_FONT, 21)

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
                if event.button == 1: 
                    self.player.Attack(self.camera)
                if event.button == 3:
                    self.player.Defence()
                if event.button == 2:
                    self.player.MeleeAttack()
            if event.type == pygame.MOUSEBUTTONUP:
                self.player.DesactivateDefence()

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
                                   self.height - self.camera.y, self.width, self.height))
                


        self.map.draw(self.screen, self.player, self.camera)

        self.mob.DamagePlayer(self.player, self.map.colliders)
        
        self.player.update( self.surface, self.camera, self.map.colliders, self.dt)


        if self.player.getCollision(self.map.end_zone):
            self.load_next_map()
            pygame.display.flip()
            return

        self.update_camera()

        # Develop in progress
     

        self.mob.tryThrow(self.player, self.camera)
        self.mob.tryAttack(self.player)
        self.mob.tryDefence(self.player)
        self.player.DamageEnnemy(self.mob)
        self.mob.update(self.dt, self.surface, self.camera, self.map.colliders, self.player)
        self.mob.drawHammer(self.surface, self.player, self.camera)

        self.player.DrawArrow(self.surface, self.camera)

        self.player.UpdateArrow(self.dt)

        self.text.draw_text("fps :" + str(self.clock.get_fps()), (255, 255, 255), 100, 100, 10, 10)

        for i in range(len(self.map.background_sprites)):
             if self.map.background_sprites[i][0] is not None:
                self.surface.blit(self.map.background_sprites[i][0].texture,
                                  ((i * self.map.background_width) - (self.camera.x * self.map.parralax_speed[0]),
                                   self.height - self.camera.y))
            
        if self.player.health == 6:
            Assets.GetSprite(SpritesRef.LIFE_6).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health == 5:
            Assets.GetSprite(SpritesRef.LIFE_5).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health == 4:
            Assets.GetSprite(SpritesRef.LIFE_4).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health == 3:
            Assets.GetSprite(SpritesRef.LIFE_3).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health == 2:
            Assets.GetSprite(SpritesRef.LIFE_2).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health == 1:
            Assets.GetSprite(SpritesRef.LIFE_1).draw(self.surface,Vector2(20,20),Vector2(1,1))
        elif self.player.health <= 0:
            Assets.GetSprite(SpritesRef.LIFE_0).draw(self.surface,Vector2(20,20),Vector2(1,1))

        #self.text.draw_text("Test de Text adaptatif !", (255, 255, 255), 100, 100, 10, 10)

        pygame.display.flip()

    def loop(self):
        
        running = True

        self.music_manager.Play_Level()
        while running:
            dt_start = pygame.time.get_ticks()
            running = self.inputs()
            
            # element = self.elementsOnScreen.first
            # amountOfElementsOnScreen = self.elementsOnScreen.count
            # for elementIndex in range( amountOfElementsOnScreen ):
            #     if ( not element.value.isOnScreen ):
                    
            #         if ( amountOfElementsOnScreen == 1 ): self.elementsOnScreen.first = None
            #         else:
            #             element.previous.next = element.next
            #             element.next.previous = element.previous
            #             if ( elementIndex == 0 ):
            #                 self.elementsOnScreen.first = element.next
                    
            #         self.elementsOnScreen.count -= 1
            #         element.value.isVisible = False
            #     element.value.update( self.surface )
            #     element = element.next #! I think this won't work because it's not a "pointer" copy, but a real copy that creates a new Node

            self.update_graphics()

            self.clock.tick(60)
            dt_end = pygame.time.get_ticks()
            self.dt =self.clock.get_time() / 1000
            self.current_dt += self.dt
        
        pygame.quit()

        