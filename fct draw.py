import pygame

text_size = 20
text_font = pygame.font.SysFont("Arial",text_size)

def draw_text(text,font,text_color,x,y,vert_mrg,left_mrg):
    txt = font.render(text, True, text_color)
    text_surface = pygame.Surface( (2*left_mrg + txt.get_size()[0], 2*vert_mrg + txt.get_size()[1]), pygame.SRCALPHA)
    # Définir la couleur du rectangle avec une opacité de 20 (sur 255)
    pygame.draw.rect(text_surface, (0, 0, 0, 120), text_surface.get_rect(), 0)
    # Rendre le texte sur la surface transparente

    # Dessiner la surface avec le texte sur l'écran
    screen.blit(text_surface, (x - left_mrg, y - vert_mrg))
    screen.blit(txt, (x, y))

  draw_text("Hello World ! Le problème c. ", text_font, (255,255,255),200,500,15,30)
