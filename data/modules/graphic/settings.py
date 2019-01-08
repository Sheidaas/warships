from data.modules.graphic.basic.button import Button
import pygame


class Settings:

    def __init__(self):
        self.background = None
        self.buttons = {}
        self.update = False

    def create(self, screen):
        self.buttons = {}
        start = (480, 420)

        size = (250, 50)

        self.buttons['resume'] = Button(start[0], start[1], size[0], size[1],
                                        screen.engine.database.language.texts['gui']['settings']['resume'], screen.font,
                                               self.exit, screen.screen, screen.engine.settings.graphic['screen'], screen)

        start = (480, 495)

        text = screen.engine.database.language.texts['gui']['settings']['antialias'] + str(screen.engine.settings.graphic['screen']['antialias'])
        self.buttons['change_antialias'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          self.change_antialias, screen.screen, screen.engine.settings.graphic['screen'],
                                                  screen)

        start = (480, 570)

        text = screen.engine.database.language.texts['gui']['settings']['fullscreen'] + str(screen.engine.settings.graphic['screen']['fullscreen'])
        self.buttons['change_fullscreen'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          self.change_fullscreen, screen.screen, screen.engine.settings.graphic['screen'], screen)

        start = (405, 645)
        size = (50, 50)
        self.buttons['font_size_minus'] = Button(start[0], start[1], size[0], size[1], '-', screen.font,
                                          self.change_font_size, screen.screen, screen.engine.settings.graphic['screen'], screen, '-')

        start = (480, 645)
        size = (250, 50)
        text = screen.engine.database.language.texts['gui']['settings']['font_size'] + str(screen.engine.settings.graphic['screen']['font_size'])
        self.buttons['font_size'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          None, screen.screen, screen.engine.settings.graphic['screen'], 0)

        start = (755, 645)
        size = (50, 50)
        self.buttons['font_size_plus'] = Button(start[0], start[1], size[0], size[1], '+', screen.font,
                                          self.change_font_size, screen.screen, screen.engine.settings.graphic['screen'], screen, '+')

        start = (405, 720)
        self.buttons['resolution_minus'] = Button(start[0], start[1], size[0], size[1], '-', screen.font,
                                          self.change_resolution, screen.screen, screen.engine.settings.graphic['screen'], screen, '-')

        start = (480, 720)
        size = (250, 50)
        text = str(screen.engine.settings.graphic['screen']['resolution_x']) + 'x' + str(screen.engine.settings.graphic['screen']['resolution_y'])
        self.buttons['resolution'] = Button(start[0], start[1], size[0], size[1], text, screen.font,
                                          None, screen.screen, screen.engine.settings.graphic['screen'], 0)

        start = (755, 720)
        size = (50, 50)
        self.buttons['resolution_plus'] = Button(start[0], start[1], size[0], size[1], '+', screen.font,
                                          self.change_resolution, screen.screen, screen.engine.settings.graphic['screen'], screen, '+')

        self.background = self.resize_image(pygame.image.load(screen.engine.path + '/data/files/background.png'), screen)

        self.update = False

    def go_to_player_settings(self, screen):
        screen.gui['settings'] = False
        screen.gui['settings_gui'] = True

    def change_resolution(self, screen, char):
        self.update = True
        if char == '-':
            key = 1
            for resolution in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                if screen.engine.settings.graphic['screen']['resolution_x'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][0] and \
                        screen.engine.settings.graphic['screen']['resolution_y'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][1]:
                    key = int(resolution)
                    break
            if key == 1:
                for index in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                    if key < int(index):
                        key = int(index)
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]
            else:
                key -= 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]

        else:
            key = 1
            for resolution in screen.engine.settings.graphic['screen']['avaible_resolutions']:
                if screen.engine.settings.graphic['screen']['resolution_x'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][0] and \
                    screen.engine.settings.graphic['screen']['resolution_y'] == screen.engine.settings.graphic['screen']['avaible_resolutions'][resolution][1]:
                    key = int(resolution)
                    break
            if key == len(screen.engine.settings.graphic['screen']['avaible_resolutions']):
                key = 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]
            else:
                key += 1
                screen.engine.settings.graphic['screen']['resolution_x'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][0]
                screen.engine.settings.graphic['screen']['resolution_y'] = screen.engine.settings.graphic['screen']['avaible_resolutions'][str(key)][1]

        screen.engine.save_settings()
        screen.change_resolution()

    def change_font_size(self, screen, char):
        self.update = True
        if char == '-':
            if screen.engine.settings.graphic['screen']['font_size'] > 24:
                screen.engine.settings.graphic['screen']['font_size'] -= 1
        else:
            if screen.engine.settings.graphic['screen']['font_size'] < 30:
                screen.engine.settings.graphic['screen']['font_size'] += 1
        screen.change_font_size()
        screen.engine.save_settings()

    def change_fullscreen(self, screen):
        self.update = True
        if screen.engine.settings.graphic['screen']['fullscreen']:
            screen.engine.settings.graphic['screen']['fullscreen'] = False
            screen.change_fullscreen()
        else:
            screen.engine.settings.graphic['screen']['fullscreen'] = True
            screen.change_fullscreen()
        screen.engine.save_settings()

    def change_antialias(self, screen):
        self.update = True
        if screen.engine.settings.graphic['screen']['antialias'] == 0:
            screen.engine.settings.graphic['screen']['antialias'] = 1
        else:
            screen.engine.settings.graphic['screen']['antialias'] = 0
        screen.engine.save_settings()

    def render_buttons(self):
        for key in self.buttons.keys():
            self.buttons[key].render_button()

    def render_background(self, screen):
        screen.screen.blit(self.background, (0, 0))

    def render(self, screen):
        if self.update:
            self.create(screen)
        self.render_background(screen)
        self.render_buttons()

    @staticmethod
    def exit(screen):
        screen.gui['settings'] = False
        screen.gui['menu'] = True

    def resize_image(self, img, screen):
        scale = (screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 screen.engine.settings.graphic['screen']['resolution_scale'][1])
        size = img.get_size()
        size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
        return pygame.transform.scale(img, size)