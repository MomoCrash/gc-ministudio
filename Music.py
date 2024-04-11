import pygame
from pygame import mixer

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

class Songs:
    def __init__(self) -> None:
        pass

    def Play_Menu():
        pygame.mixer.music.load('Musics/Projet_Vikings_Menu.mp3')
        pygame.mixer.music.play(-1,0.0,3000)

    def Play_Tuto():
        pygame.mixer.music.load('Musics/Musique_Tuto.mp3')
        pygame.mixer.music.play(-1,0.0,3000)

    def Play_Level():
        pygame.mixer.music.load('Musics/Musique_Level.mp3')
        pygame.mixer.music.play(-1,0.0,3000)