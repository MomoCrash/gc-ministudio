import pygame
import time
import settings

pygame.init()

"""
class Entity():
    def __init__(self, spawn_x, spawn_y):
        self.x = spawn_x
        self.y = spawn_y
        self.vel = 5
        self.Maxvel = 10
        self.left = False
        self.right = False
        self.last = 0
        self.walkCount = 0
        self.CanJump = False
        self.JumpCount = 10

    
    def movement(self):
        pass

    def flip(self):
        pass

    def RectCollision(self, other_rect: pygame.rect):
        collide = pygame.Rect.colliderect(player.rect,other_rect)
        if collide:
            self.rect.bottom = other_rect.top

"""

class Player():
    def __init__(self) :
        #super().__init__(100, 100)
        self.x = 100
        self.y = 100
        self.vel = 5
        self.Maxvel = 10
        self.left = False
        self.right = False
        self.last = 0
        self.walkCount = 0
        self.walkRight = [pygame.image.load("./Assets/SpriteSheets/Player/MoveRight/image_0-0.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveRight/image_0-1.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveRight/image_0-2.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveRight/image_0-3.png")]
        for i in range(len(self.walkRight)):
            self.walkRight[i] = pygame.transform.scale(self.walkRight[i], (40, 80))
        self.walkLeft = [pygame.image.load("./Assets/SpriteSheets/Player/MoveLeft/image_1-0.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveLeft/image_1-1.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveLeft/image_1-2.png"),pygame.image.load("./Assets/SpriteSheets/Player/MoveLeft/image_1-3.png")]
        for i in range(len(self.walkLeft)):
            self.walkLeft[i] = pygame.transform.scale(self.walkLeft[i], (40, 80))
        self.StandLeft = pygame.image.load("./Assets/SpriteSheets/Player/MoveLeft/image_1-0.png")
        self.StandLeft = pygame.transform.scale(self.StandLeft, (40, 80))
        self.StandRight = pygame.image.load("./Assets/SpriteSheets/Player/MoveRight/image_0-0.png")
        self.StandRight = pygame.transform.scale(self.StandRight, (40, 80))
        self.CanJump = False
        self.JumpCount = 10

        self.rect = self.StandRight.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.StandRight.get_width()
        self.height = self.StandRight.get_height()
        self.IsFacingRight = True

    def movement(self):
        keys = pygame.key.get_pressed()
        win.fill((0,0,0))
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.vel

        if keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] < 0:
            self.left = True
            self.right = False
            self.last = 1
        elif keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] > 0:
            self.left = False
            self.right = True
            self.last = 0
        else:
            self.left = False
            self.right = False
        
        

        if keys[pygame.K_SPACE]:
            self.CanJump = True
        
        if self.CanJump:
            if self.JumpCount >= -10:
                self.rect.y -= (self.JumpCount * abs(self.JumpCount)) * 0.1
                self.JumpCount -= 1
            else: # This will execute if our jump is finished
                self.JumpCount = 10
                self.CanJump = False

        if self.CanJump == False:
            self.rect.y += 14
        

    def flip(self):
        if keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] < 0 and self.IsFacingRight:
            self.sprite = pygame.transform.flip(self.StandRight,True, False)
            self.IsFacingRight = False
        elif keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] > 0 and self.IsFacingRight == False:
            self.sprite = pygame.transform.flip(self.StandLeft,True, False)
            self.IsFacingRight = True


    def update(self):
        #On affiche notre sprite en fonction du walCount
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if self.left:  
            win.blit(self.walkLeft[self.walkCount//6],self.rect)
            self.walkCount += 1                          
        elif self.right:
            win.blit(self.walkRight[self.walkCount//6], self.rect)
            self.walkCount += 1
        else:
            if self.last == 0:
                win.blit(self.StandRight, self.rect)
            else:
                win.blit(self.StandLeft, self.rect)
            self.walkCount = 0

    def RectCollision(self, other_rect: pygame.rect):
        collide = pygame.Rect.colliderect(player.rect,other_rect)
        if collide:
            self.rect.bottom = other_rect.top

class Platform:
    def __init__(self,leftx,topy,width,height):
        self.height = height
        self.widht = width
        self.x = leftx
        self.y = topy
        self.rect = pygame.Rect(self.x,self.y,self.widht,self.height)

    def draw(self):
        pygame.draw.rect(win,settings.WHITE, self.rect)

        

run = True
fpsClock = pygame.time.Clock()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")
player = Player()
platform = Platform(0,470,500,30)
  # Fills the screen with black

while run:
    pygame.display.flip()
    fpsClock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
   
    player.movement()
    player.flip()
    player.RectCollision(platform.rect)
    player.update()
    platform.draw()
    pygame.display.update() 
    
pygame.quit()