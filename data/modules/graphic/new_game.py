import pygame

from data.modules.graphic.basic.button import Button
from data.modules.graphic.basic.background import Background


class Menu:

    def __init__(self):
        self.background = None
        self.buttons = {}

    def create_buttons(self, screen):
        self.buttons = {}

        start = (480, 300)
        size = (400, 50)

        self.buttons['new_game'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['new_game']['new_game_human'],
                                        screen.font, self.new_game, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen, False)
        start = (480, 375)
        self.buttons['new_game_ai'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['new_game']['new_game_ai'],
                                        screen.font, self.new_game, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen, True)

        for ship in screen.engine.database.language.texts['gui']['new_game']['ships']:
            start = (380, 375 + (75 * int(ship)))
            size = (50, 50)
            self.buttons[ship + 'minus'] = Button(start[0], start[1], size[0], size[1], '-', screen.font,
                                                      self.change_ship, screen.screen,
                                                      screen.engine.settings.graphic['screen'], screen, '-', ship)

            start = (480, 375 + (75 * int(ship)))
            size = (400, 50)
            text = screen.engine.database.language.texts['gui']['new_game']['ships'][ship] + ': ' + str(screen.engine.settings.primary_settings['ships'][ship])
            self.buttons[ship] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                                None, screen.screen, screen.engine.settings.graphic['screen'], 0)

            start = (960, 375 + (75 * int(ship)))
            size = (50, 50)
            self.buttons[ship + 'plus'] = Button(start[0], start[1], size[0], size[1], '+', screen.font,
                                                     self.change_ship, screen.screen,
                                                     screen.engine.settings.graphic['screen'], screen, '+', ship)

        start = (480, 800)
        self.buttons['return'] = Button(start[0], start[1],
                                        size[0], size[1], screen.engine.database.language.texts['gui']['new_game']['return'],
                                        screen.font, self.back, screen.screen,
                                        screen.engine.settings.graphic['screen'], screen)

        self.update = False

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

    def render(self, screen, path):
        if self.update:
            self.create(screen, path)
        self.render_background(screen)
        self.render_buttons()

    def change_ship(self, screen, char, ship):
        self.update = True
        if char == '-':
            if screen.engine.settings.primary_settings['ships'][ship] > 1:
                screen.engine.settings.primary_settings['ships'][ship] -= 1
        else:
            if screen.engine.settings.primary_settings['ships'][ship] < 2:
                screen.engine.settings.primary_settings['ships'][ship] += 1
        screen.engine.save_settings()

    def new_game(self, screen, ai):
        screen.gui['new_game'] = False
        screen.drawer.gui['new_game'] = None
        screen.engine.new_game(screen.gui, ai)

    def back(self, screen):
        screen.gui['new_game'] = False
        screen.drawer.gui['new_game'] = None
        screen.gui['menu'] = True

    def resize_image(self, img, screen):
        scale = (screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 screen.engine.settings.graphic['screen']['resolution_scale'][1])
        size = img.get_size()
        size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
        return pygame.transform.scale(img, size)

