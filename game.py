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


        self.map = Map(self, win_width, win_height)
        self.map.createObject( Vector2( 0, 850 ), Vector2( 5000, 20 ) )
        self.map.createObject( Vector2( 1000, 900 ), Vector2( 200, 80 ) )
        self.map.createObject( Vector2( 1500, 650 ), Vector2( 250, 80 ) )
        self.map.createObject( Vector2( 2500, 650 ), Vector2( 250, 80 ) )
        
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(
                                position = Vector2( 1000, 500 ),
                                walkingLeftSpriteSheetRef = SpriteSheetsRef.PLAYER_WALK_LEFT,
                                walkingRightSpriteSheetRef = SpriteSheetsRef.PLAYER_WALK_RIGHT,
                                spriteDimensions = Vector2( 40, 80 )
                            )
        self.mob = Mob( position=Vector2( 500, 500 ), scale=Vector2( 40, 80 ) )
        self.camera = pygame.Vector2(0, 0)

        self.text = Text(self.screen, "Arial")
        
        self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]

        self.loop()

    def inputs(self) -> bool:

        self.camera.x = self.player.transform.position.x - self.width // 4
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))
        
        # for mapObject in self.map.elements:
        #     mapObject.transform.position.x = mapObject.transform.position.x - self.camera.x

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.player.Attack()
        return True
    
    
    def update(self):
        pass

    def update_graphics(self):

        self.map.draw(self.surface)

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))
        
        self.player.update( self.surface, self.map.elements )

        self.mob.movement(self.player)

        self.mob.tryThrow(self.player)
        self.mob.update(self.dt)
        self.mob.draw(self.surface, self.player)

        self.text.draw_text("Salut la team", (0, 0, 0), 100, 100, 10, 10)


        #for mapObject in self.map.elements:
        #    mapObject.draw(self.surface)

        #Assets.GetSprite(SpritesRef.LIGHT).draw(self.surface, (self.camera.x ,self.camera.y))

        

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