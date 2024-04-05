import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chapter's selection")
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

if __name__ == "__main__":
    main()