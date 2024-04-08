import pygame
import sys


pygame.init()
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plateformer 2D")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
           
class InfoBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.font = pygame.font.Font(None, 24)
        self.text = "Appuyez sur E pour les infos"
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.text = "Appuyez sur E pour les infos"
        else:
            self.text = ""
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

class DescriptionBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300, 200))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.font = pygame.font.Font(None, 24)
        self.text = "Description : C'est un rectangle blanc"
        self.text_render = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

def main():
    player = Player()
    info_box = InfoBox(400, 300, 200, 100)
    description_box = DescriptionBox()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, info_box, description_box)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if info_box.text:
                        description_box.text = "Description : C'est un rectangle blanc."
                    else:
                        description_box.text = ""

        
        all_sprites.update(player)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()