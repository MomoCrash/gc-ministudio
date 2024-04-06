import pygame

class Text :
  def __init__(self,surface: pygame.Surface,font_name) -> None:
    self.screen = surface
    self.text_size = 20
    self.text_font = pygame.font.SysFont(font_name,self.text_size)

  def draw_text(self,text,text_color,x,y,vert_mrg,left_mrg):
      txt = self.text_font.render(text, True, text_color)
      text_surface = pygame.Surface( (2*left_mrg + txt.get_size()[0], 2*vert_mrg + txt.get_size()[1]), pygame.SRCALPHA)
      pygame.draw.rect(text_surface, (0, 0, 0, 120), text_surface.get_rect(), 0)
      self.screen.blit(text_surface, (x - left_mrg, y - vert_mrg))
      self.screen.blit(txt, (x, y))

