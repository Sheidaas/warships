import pygame

from data.modules.graphic.basic.button import Button
from data.modules.graphic.basic.background import Background


class Menu:

    def __init__(self):
        self.buttons = {}

    def create_buttons(self, screen):
        self.buttons = {}

        start = (480, 500)
        size = (250, 50)

        self.buttons['new_game'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['menu']['new_game'],
                                        screen.font, self.new_game, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen)

        start = (480, 575)

        self.buttons['score_board'] = Button(start[0], start[1], size[0], size[1],
                                      screen.engine.database.language.texts['gui']['menu']['score_board'], screen.font, self.go_to_scoreboard, screen.screen,
                                      screen.engine.settings.graphic['screen'], screen)

        start = (480, 650)

        self.buttons['settings'] = Button(start[0], start[1], size[0], size[1],
                                          screen.engine.database.language.texts['gui']['menu']['settings'], screen.font,
                                          self.go_to_settings, screen.screen, screen.engine.settings.graphic['screen'],
                                          screen)

        start = (480, 725)

        self.buttons['exit'] = Button(start[0], start[1], size[0], size[1],
                                      screen.engine.database.language.texts['gui']['menu']['exit'], screen.font, exit,
                                      screen.screen,
                                      screen.engine.settings.graphic['screen'], 0)

    def create_background(self, screen, path):
        self.background = self.resize_image(pygame.image.load(path + '/data/files/background.png'), screen)

    def create(self, screen, path):
        self.create_buttons(screen)
        self.create_background(screen, path)

    def render_buttons(self):
        for key in self.buttons.keys():
            self.buttons[key].render_button()

    def render_background(self, screen):
        screen.screen.blit(self.background, (0, 0))

    def render(self, screen):
        self.render_background(screen)
        self.render_buttons()

    @staticmethod
    def go_to_settings(screen):
        screen.gui['menu'] = False
        screen.gui['settings'] = True

    @staticmethod
    def go_to_scoreboard(screen):
        screen.gui['menu'] = False
        screen.gui['scoreboard'] = True

    @staticmethod
    def exit(screen):
        screen.gui['menu'] = False
        screen.drawer.gui['menu'] = None

    def new_game(self, screen):
        screen.gui['menu'] = False
        screen.gui['new_game'] = True
        screen.drawer.gui['menu'] = None

    def resize_image(self, img, screen):
        scale = (screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 screen.engine.settings.graphic['screen']['resolution_scale'][1])
        size = img.get_size()
        size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
        return pygame.transform.scale(img, size)
