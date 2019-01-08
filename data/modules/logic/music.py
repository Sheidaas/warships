import pygame


class Mixer:
    def __init__(self, path):
        pygame.mixer.init()
        self.path = path

    def play_song(self, name):
        pygame.mixer.music.load(self.path + '/data/files/music/' + name + '.ogg')
        pygame.mixer.music.play(0)

