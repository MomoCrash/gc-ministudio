import pygame
import sys

pygame.init()

WHITE =(255, 255, 255)
BLACK =(0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Tests")
font = pygame.font.Font(None, 40)
menu_items = ("Jouer", "Options", "Quitter")





