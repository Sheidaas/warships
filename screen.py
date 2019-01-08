import os
import pygame
from data.modules.logic import drawer
from data.modules.logic import engine
from data.modules.logic.composition_phase import CompositionPhase


class Screen:

    def __init__(self,):
        self.engine = engine.GameEngine(os.path.dirname(os.path.abspath(__file__)))
        self.screen = None
        self.drawer = drawer.Drawer()
        self.font = None
        self.gui = {
            'menu': True,
            'settings': False,
            'board': False,
            'scoreboard': False,
            'end_game': True,
            'new_game': False
        }
        self.mouse = (None, (0, 0, 0))
        self.is_need_to_restart = False

    def init(self):
        pygame.display.init()
        if self.engine.settings.graphic['screen']['fullscreen']:
            self.screen = pygame.display.set_mode((self.engine.settings.graphic['screen']['resolution_x'],
                                                   self.engine.settings.graphic['screen']['resolution_y']),
                                                  pygame.FULLSCREEN | pygame.HWSURFACE, 32)
        else:
            self.screen = pygame.display.set_mode((self.engine.settings.graphic['screen']['resolution_x'],
                                                   self.engine.settings.graphic['screen']['resolution_y']))

        self.engine.settings.graphic['screen']['resolution_scale'] = (self.engine.settings.graphic['screen']['resolution_x']/1920,
                                                                      self.engine.settings.graphic['screen']['resolution_y']/1080)
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.font = pygame.font.Font(None, self.engine.settings.graphic['screen']['font_size'])
        pygame.display.set_caption(self.engine.settings.graphic['screen']['caption'])

    def change_resolution(self):
        self.is_need_to_restart = True

    def change_font_size(self):
        self.font = pygame.font.Font(None, screen.engine.settings.graphic['screen']['font_size'])

    def change_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def run(self):
        while True:
            if self.is_need_to_restart:
                return True
            self.get_event()
            self.draw()

    def get_event(self):
        self.mouse = (pygame.mouse.get_pos(), (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    self.mouse = (self.mouse[0], (pygame.mouse.get_pressed()))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)
                if self.gui['board']:
                    if isinstance(self.engine.phase, CompositionPhase):
                        if event.key == pygame.K_q:
                            self.engine.phase.active_ship.change_turn('left', self.engine.settings.graphic['screen']['resolution_scale'])
                        elif event.key == pygame.K_e:
                            self.engine.phase.active_ship.change_turn('right', self.engine.settings.graphic['screen']['resolution_scale'])
                    if event.key == pygame.K_x:
                        self.drawer.gui['board'].toggle_board()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.drawer.render_gui(self)
        pygame.display.flip()

if __name__ == '__main__':
    while True:
        screen = Screen()
        screen.init()
        screen.run()
