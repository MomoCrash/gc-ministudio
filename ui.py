import pygame

#Pop up box
class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Hitbox:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = self.rect.inflate(50, 50)
        self.color = color
        self.show_popup = False
        self.big_popup = False

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.show_popup:
            if not self.big_popup:
                popup_rect = pygame.Rect(self.rect.x, self.rect.y - 80, self.rect.width + 100, 100)
                pygame.draw.rect(screen, BLACK, popup_rect)
                font = pygame.font.Font(None, 16) 
                description_text = "Appuyez sur E pour ouvrir la description"
                text_x = popup_rect.x + 10
                text_y = popup_rect.y + 10
                max_width = popup_rect.width - 20
                words = description_text.split()
                space_width = font.size(' ')[0]
                space_count = 0
                char_count = 0
                line = ''
                for word in words:
                    word_width = font.size(word)[0]
                    char_count += len(word)
                    if char_count * font.size('A')[0] + space_count * space_width >= max_width:
                        screen.blit(font.render(line, True, WHITE), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, WHITE), (text_x, text_y))
            else:
                popup_width = 600  
                popup_height = 300  
                popup_x = (SCREEN_WIDTH - popup_width) // 2  
                popup_y = (SCREEN_HEIGHT - popup_height) // 2 + 50  
                popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
                pygame.draw.rect(screen, BLACK, popup_rect)
                font = pygame.font.Font(None, 24)  
                description_text = "DESCRIPTION DE L'OBJET : description etc etc du rectangle"
                text_x = popup_rect.x + 20
                text_y = popup_rect.y + 20
                max_width = popup_rect.width - 40
                words = description_text.split()
                space_width = font.size(' ')[0]
                space_count = 0
                char_count = 0
                line = ''
                for word in words:
                    word_width = font.size(word)[0]
                    char_count += len(word)
                    if char_count * font.size('A')[0] + space_count * space_width >= max_width:
                        screen.blit(font.render(line, True, WHITE), (text_x, text_y))
                        text_y += font.get_linesize() + 5
                        line = ''
                        char_count = 0
                    line += word + ' '
                    space_count += 1
                screen.blit(font.render(line, True, WHITE), (text_x, text_y))


# Info box
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
    
# Starting menu
font = pygame.font.Font(None, 40)
menu_items = ["JOUER", "CHAPITRES"]
chapters = ["CHAPITRE 1", "CHAPITRE 2", "CHAPITRE 3", "CHAPITRE 4", "CHAPITRE 5",]
current_menu_item = None
image =  pygame.transform.scale(pygame.image.load("nordics.jfif") , (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = [image]

def draw_menu():
    SCREEN.fill(BLACK)
    for i, item in enumerate(menu_items):
        text = font.render(item, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
        SCREEN.blit(text, text_rect)

def draw_background():
    SCREEN.fill(BLACK)
    SCREEN.blit(image,(0, 0))

def draw_chapters():
    SCREEN.fill(BLACK)
    for i, chapter in enumerate(chapters):
        text = font.render(chapter, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
        SCREEN.blit(text, text_rect)
    back_button = font.render("RETOUR", True, WHITE)
    back_rect = back_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    SCREEN.blit(back_button, back_rect)
    return back_rect

def main_menu():
    global current_menu_item
    draw_background()
    draw_menu()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    text_rect = font.render(item, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        current_menu_item = item
                        if current_menu_item == "JOUER":
                            play_game()
                        elif current_menu_item == "CHAPITRES":
                            draw_chapters()
                            pygame.display.flip()
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        back_rect = draw_chapters()
                                        if back_rect.collidepoint(mouse_x, mouse_y):
                                            return
                                        for j, chapter in enumerate(chapters):
                                            text_rect = font.render(chapter, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + j * 50))
                                            if text_rect.collidepoint(mouse_x, mouse_y):
                                                print(f"chapitre {j+1} sélectionné ")  
                                                return
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    text_rect = font.render(item, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        menu_items[i] = item.upper()
                    else:
                        menu_items[i] = item
        draw_background()
        draw_menu()
        pygame.display.flip()

def play_game():
   
    print("jeu lancé")

        

def main():
    main_menu()