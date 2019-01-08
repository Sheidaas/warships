from data.modules.logic.composition_phase import CompositionPhase
from data.modules.logic.shooting_phase import ShootingPhase
from data.modules.graphic.end_game import Menu
from data.modules.logic.ai import AI
from data.modules.logic.music import Mixer
from data.files.ships.ships import ships
import pygame


class Board:

    def __init__(self, screen, ai=False):
        self.screen = screen
        self.active_player = 1
        self.active_board = 1
        self.start = ()
        self.render_objects = {
            'boards': {
                1: {
                    'shoots': [],
                    'own_ship': []

                },
                2: {
                    'shoots': [],
                    'own_ship': []

                }
            },
            'squares': [],
            'square': {
                'square': {
                    'render': '/data/files/board/square.png',
                    'size': (90, 90)
                },
                'miss_square': {
                    'render': '/data/files/board/miss_square.png',
                    'size': (90, 90)
                },
                'hit_square': {
                    'render': '/data/files/board/hit_square.png',
                    'size': (90, 90)
                },
            },
            'background': {
                'render': '/data/files/board/background.png',
                'position': (0, 0)
            }
        }
        self.ai = None
        if ai:
            self.ai = AI()
        self.mixer = Mixer(screen.engine.path)

    def create(self, path):
        self.active_player = self.screen.engine.phase.active_player

        resolution = (self.screen.engine.settings.graphic['screen']['resolution_x'],
                      self.screen.engine.settings.graphic['screen']['resolution_y'])
        scale = (self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        self.render_objects['square']['square']['size'] = (90 * scale[0], 90 * scale[1])
        self.render_objects['square']['miss_square']['size'] = (90 * scale[0], 90 * scale[1])
        self.render_objects['square']['hit_square']['size'] = (90 * scale[0], 90 * scale[1])
        self.start = (resolution[0] / 2 - self.render_objects['square']['square']['size'][0] * 10 / 2,
                      resolution[1] / 2 - self.render_objects['square']['square']['size'][1] * 10 / 2)

        self.load_resources(path)

    def render(self, mouse_position):
        self.screen.screen.blit(self.render_objects['background']['render'],
                           self.render_objects['background']['position'])
        position = (self.start[0] + (800 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]),
                    self.start[1],
                    525 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1],
                    225 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        pygame.draw.rect(self.screen.screen, (100, 100, 100), position)

        position = (position[0] + (50 * self.screen.engine.settings.graphic['screen']['resolution_scale'][0]), position[1])
        for key in self.screen.engine.database.language.texts['gui']['board'].keys():
            position = (position[0], position[1] + (50 * self.screen.engine.settings.graphic['screen']['resolution_scale'][1]))
            text_to_render = self.screen.font.render(self.screen.engine.database.language.texts['gui']['board'][key],
                                                     int(self.screen.engine.settings.graphic['screen']['antialias']), (255, 255, 255))
            self.screen.screen.blit(text_to_render, position)


        for x in range(10):
            position = [self.start[0] + x * self.render_objects['square']['square']['size'][0] - 200, self.start[1]]
            for y in range(10):
                position = [position[0], self.start[1] + y * self.render_objects['square']['square']['size'][1]]

                if not isinstance(self.screen.engine.phase, CompositionPhase):
                    if self.active_player != self.active_board:
                        if (x, y) in self.render_objects['boards'][self.active_player]['shoots']:
                            self.screen.screen.blit(self.render_objects['square']['miss_square']['render'], position)
                            player = 0
                            if self.active_player == 1:
                                player = 2
                            else:
                                player = 1
                            for ship in self.render_objects['boards'][player]['own_ship']:
                                for part in ship.parts:
                                    if (x, y) == part['position']:
                                        self.screen.screen.blit(self.render_objects['square']['hit_square']['render'], position)
                        else:
                            self.screen.screen.blit(self.render_objects['square']['square']['render'], position)
                    else:
                        player = 0
                        if self.active_player == 1:
                            player = 2
                        else:
                            player = 1
                        if (x, y) in self.render_objects['boards'][player]['shoots']:
                            self.screen.screen.blit(self.render_objects['square']['miss_square']['render'], position)
                            for ship in self.render_objects['boards'][self.active_player]['own_ship']:
                                for part in ship.parts:
                                    if (x, y) == part['position']:
                                        self.screen.screen.blit(self.render_objects['square']['hit_square']['render'], position)
                        else:
                            self.screen.screen.blit(self.render_objects['square']['square']['render'], position)
                else:
                    self.screen.screen.blit(self.render_objects['square']['square']['render'], position)

        self.render_ships()

        if self.screen.engine.phase.end_phase:
            self.screen.engine.next_phase()
        if isinstance(self.screen.engine.phase,  CompositionPhase):
            if not self.ai == None:
                if self.active_player == 1:
                    self.screen.engine.phase.while_composition(self.active_player)
                    self.render_ship_in_composition_phase(mouse_position)
                else:
                    self.ai.run(self.screen.engine, self)
            else:
                self.screen.engine.phase.while_composition(self.active_player)
                self.render_ship_in_composition_phase(mouse_position)

        elif isinstance(self.screen.engine.phase, ShootingPhase):
            if self.active_player == 2 and not self.ai == None:
                self.ai.run(self.screen.engine, self)

            player = self.screen.engine.phase.check_win(self)
            if player != 0:
                self.mixer.play_song('end_game')
                self.screen.engine.end_game(player, self.check_score(player))
                self.screen.gui['board'] = False
                self.screen.gui['end_game'] = True
                self.screen.drawer.gui['end_game'] = Menu(player, self.check_score(player))
                self.screen.drawer.gui['end_game'].create(self.screen, self.screen.engine.path)
                self.screen.drawer.gui['board'] = None

    def render_ships(self):
        if self.active_player == self.active_board:
            for ship in self.render_objects['boards'][self.active_player]['own_ship']:
                for part in range(len(ship.parts)):
                    position = (ship.parts[part]['position'][0] * self.render_objects['square']['square']['size'][0] + self.start[0]-200+5,
                                ship.parts[part]['position'][1] * self.render_objects['square']['square']['size'][1] + self.start[1]+5)
                    self.screen.screen.blit(ship.parts[part]['render'], position)

    def render_shoots(self):
        pass

    def load_resources(self, path):
        self.render_objects['background']['render'] = \
            pygame.image.load(path + self.render_objects['background']['render'])
        self.render_objects['background']['render'] = self.resize_image(self.render_objects['background']['render'])

        for image in ('square', 'miss_square', 'hit_square'):
            self.render_objects['square'][image]['render'] = \
                pygame.image.load(path + self.render_objects['square'][image]['render'])
            self.render_objects['square'][image]['render'] = self.resize_image(self.render_objects['square'][image]['render'])

        for player in self.render_objects['boards']:
            for ship in self.screen.engine.phase.players[player]['ships']:
                for part in ship.parts:
                    part['render'] = self.resize_image(pygame.image.load(path + ships[len(ship.parts)][part['render']]))

    def resize_image(self, img):
        scale = (self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        size = img.get_size()
        size = (int(size[0] * scale[0]), int(size[1] * scale[1]))
        return pygame.transform.scale(img, size)

    def toggle_player(self):
        if self.active_player == 1:
            self.active_player = 2
        else:
            self.active_player = 1

    def toggle_board(self):
        if self.active_board == 1:
            self.active_board = 2
        else:
            self.active_board = 1

    def locate_mouse(self, mouse_position):
        for x in range(10):
            position = [self.start[0] + x * self.render_objects['square']['square']['size'][0] - 200, self.start[1]]
            for y in range(10):
                position = [position[0], self.start[1] + y * self.render_objects['square']['square']['size'][1]]
                size = self.render_objects['square']['square']['size']
                area = (
                position[0], position[1], position[0] + size[0], position[1] + size[1])
                if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
                        and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
                    return (x, y)

        return False

    def render_ship_in_composition_phase(self, mouse_position):
        scale = (self.screen.engine.settings.graphic['screen']['resolution_scale'][0],
                 self.screen.engine.settings.graphic['screen']['resolution_scale'][1])
        _break = False
        for x in range(10):
            if _break:
                break
            position = [self.start[0] + x * self.render_objects['square']['square']['size'][0] - 200, self.start[1]]
            for y in range(10):
                position = [position[0], self.start[1] + y * self.render_objects['square']['square']['size'][1]]
                size = self.render_objects['square']['square']['size']
                area = (
                position[0], position[1], position[0] + size[0], position[1] + size[1])
                if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
                        and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
                    ship = self.screen.engine.phase.active_ship
                    self.screen.engine.phase.last_position = (x, y)
                    for part in ship.parts:
                        pos = (position[0] + part['position'][0]+5, position[1] + part['position'][1]+5)
                        self.screen.screen.blit(part['render'], pos)
                    _break = True
                    break

    def check_score(self, player):
        score = 0
        second_player = 2
        if player == 2:
            second_player = 1

        for ship in self.render_objects['boards'][second_player]['own_ship']:
            score += 50 * len(ship.parts)

        for ship in self.render_objects['boards'][player]['own_ship']:
            for part in ship.parts:
                if part['position'] in self.render_objects['boards'][second_player]['shoots']:
                    score -= len(ship.parts) * 50

        return score