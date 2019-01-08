import pygame

from data.modules.graphic.basic.button import Button
from data.modules.graphic.basic.background import Background


class Menu:

    def __init__(self):
        self.background = None
        self.buttons = {}

    def create_buttons(self, screen):
        self.buttons = {}

        for score in screen.engine.database.scoreboard.score:
            size = (480, 100 + (int(score) * 75), 250, 50)
            pygame.draw.rect(screen.screen, (100, 100, 100), size)
            text_to_render = screen.font.render(screen.engine.database.scoreboard.score[score]['winner'],
                                               int(screen.engine.settings.graphic['screen']['antialias']), (0, 0, 255))
            screen.screen.blit(text_to_render, (size[0] + 50, size[1]+15))
            text_to_render = screen.font.render(str(screen.engine.database.scoreboard.score[score]['score']),
                                               int(screen.engine.settings.graphic['screen']['antialias']), (255, 255, 255))
            screen.screen.blit(text_to_render, (size[0] + 150, size[1]+15))


        start = (480, 850)
        size = (250, 50)
        self.buttons['return'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['new_game']['return'],
                                        screen.font, self.back, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen)

        self.update = False

    def create_background(self, screen, path):
        self.background = self.resize_image(pygame.image.load(path + '/data/files/background.png'), screen)

    def create(self, screen, path):
        self.create_background(screen, path)
        self.create_buttons(screen)

    def render_buttons(self):
        for key in self.buttons.keys():
            self.buttons[key].render_button()

    def render_background(self, screen):
        screen.screen.blit(self.background, (0, 0))

    def render(self, screen, path):
        if self.update:
            self.create(screen, path)
        self.render_background(screen)
        self.create(screen, path)
        self.render_buttons()

    def back(self, screen):
        screen.gui['scoreboard'] = False
        screen.drawer.gui['scoreboard'] = None
        screen.gui['menu'] = True

    def resize_image(self, img, screen):
        scale = (screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 screen.engine.settings.graphic['screen']['resolution_scale'][1])
        size = img.get_size()
        size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
        return pygame.transform.scale(img, size)

