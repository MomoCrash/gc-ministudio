import pygame
from pygame import mixer

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

class Songs:
    def __init__(self) -> None:
        pass