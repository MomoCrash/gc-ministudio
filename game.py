import pygame
from linkedlist import LinkedList
from vector import Vector2
from map import Map
from text import Text
from entity import Entity, Player, Mob
from texture import SpritesRef, SpriteSheetsRef, Sprite, SpriteSheet, Assets


class Game:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        self.dt = 0
        self.current_dt = 0
        self.elementsOnScreen: LinkedList = LinkedList()
        self.elementsOffScreen: LinkedList = LinkedList()

        self.map = Map( "map1.json", win_width, win_height )
        self.map.load_map()
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((win_width, win_height))
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

        self.text = Text(self.screen, "Arial")
        
        self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]

        self.loop()

    def inputs(self) -> bool:

        self.camera.x = self.player.transform.position.x - self.width // 4
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))

        for mapObject in self.map.decors:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        for mapObject in self.map.colliders:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.player.Attack()
                if event.button == 3:
                    self.player.Defence()
            if event.type == pygame.MOUSEBUTTONUP:
                self.player.DesactivateDefence()

        return True
    
    
    def update(self):
        pass

    def update_graphics(self):

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))

        self.mob.DamagePlayer(self.player)
        self.player.update( self.surface, self.camera, self.map.colliders )


        self.map.draw(self.screen, self.camera)

        #REMOVE LATER
        for collider in self.map.colliders:
            collider.draw(self.screen, self.camera, (0, 255, 0))

        # Develop in progress
        self.mob.movement(self.player, self.dt)


        self.mob.tryThrow(self.player)
        self.mob.tryAttack(self.player)
        self.mob.tryDefence(self.player)
        self.player.DamageEnnemy(self.mob)
        self.mob.update(self.dt, self.surface, self.camera, self.map.colliders)
        self.mob.draw(self.surface, self.player)

        self.player.DrawArrow(self.surface, self.camera)

        

        self.player.UpdateArrow(self.dt)

        self.text.draw_text("fps :" + str(self.clock.get_fps()), (255, 255, 255), 100, 100, 10, 10)


        self.text.draw_text("Test de Text adaptatif !", (255, 255, 255), 100, 100, 10, 10)

        pygame.display.flip()

    def loop(self):
        
        running = True
        
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