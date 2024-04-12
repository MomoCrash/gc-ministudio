import pygame

pygame.init()

class Songs:
    def __init__(self) -> None:
        self.active = True

    def toggle_music(self):
        if self.active:
            pygame.mixer.music.pause()
            self.active = False
        else:
            self.active = True
            pygame.mixer.music.unpause()


    def Play_Menu(self):
        pygame.mixer.music.load('Musics/Projet_Vikings_Menu.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1,0.0,3000)

    def Play_Tuto(self):
        pygame.mixer.music.load('Musics/Musique_Tuto.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1,0.0,3000)

    def Play_Level(self):
        pygame.mixer.music.load('Musics/Musique_Level.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1,0.0,3000)