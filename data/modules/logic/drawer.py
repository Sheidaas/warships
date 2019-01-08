from data.modules.graphic import menu, settings, board, new_game, scoreboard, end_game


class Drawer:

    def __init__(self):
        self.gui = {
            'menu': None,
            'settings': None,
            'board': None,
            'new_game': None,
            'scoreboard': None,
            'end_game': None,
        }

    def render_gui(self, screen):
        if screen.gui['menu']:
            if self.gui['menu'] == None:
                self.gui['menu'] = menu.Menu()
                self.gui['menu'].create(screen, screen.engine.path)
                self.gui['menu'].render(screen)
            else:
                self.gui['menu'].render(screen)
                if screen.mouse[1][0]:
                    self.is_mouse_clicked('menu', screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

        if screen.gui['new_game']:
            if self.gui['new_game'] == None:
                self.gui['new_game'] = new_game.Menu()
                self.gui['new_game'].create(screen, screen.engine.path)
                self.gui['new_game'].render(screen, screen.engine.path)
            else:
                self.gui['new_game'].render(screen, screen.engine.path)
                if screen.mouse[1][0]:
                    self.is_mouse_clicked('new_game', screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

        elif screen.gui['settings']:
            if self.gui['settings'] == None:
                self.gui['settings'] = settings.Settings()
                self.gui['settings'].create(screen)
                self.gui['settings'].render(screen)
            else:
                self.gui['settings'].render(screen)
                if screen.mouse[1][0]:
                    self.is_mouse_clicked('settings', screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

        if screen.gui['board']:
            if self.gui['board'] == None:
                self.gui['board'] = board.Board(screen, screen.engine.ai)
                self.gui['board'].create(screen.engine.path)
                self.gui['board'].render(screen.mouse[0])
                self.gui['board'].mixer.play_song('end_game')
            else:
                self.gui['board'].render(screen.mouse[0])
                if screen.mouse[1][0]:
                    screen.engine.phase.on_click(self.gui['board'], screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

        if screen.gui['scoreboard']:
            if self.gui['scoreboard'] == None:
                self.gui['scoreboard'] = scoreboard.Menu()
                self.gui['scoreboard'].create(screen, screen.engine.path)
                self.gui['scoreboard'].render(screen, screen.engine.path)
            else:
                self.gui['scoreboard'].render(screen, screen.engine.path)
                if screen.mouse[1][0]:
                    self.is_mouse_clicked('scoreboard', screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

        if screen.gui['end_game']:
            if self.gui['end_game'] != None:
                self.gui['end_game'].render(screen, screen.engine.path)
                if screen.mouse[1][0]:
                    self.is_mouse_clicked('end_game', screen.mouse[0])
                    screen.mouse = (screen.mouse[0], (0, 0, 0))

    @staticmethod
    def mouse_clicked_in_button(button):
        button.on_click()

    @staticmethod
    def is_mouse_clicked_in_button(button, mouse_position):
        area = (button.start[0], button.start[1], button.start[0] + button.size[0], button.start[1] + button.size[1])
        if mouse_position[0] >= area[0] and mouse_position[0] <= area[2] \
            and mouse_position[1] >= area[1] and mouse_position[1] <= area[3]:
            return True
        return False

    def is_mouse_clicked(self, screen_key, mouse_pos):
        for key in self.gui[screen_key].buttons.keys():
            if self.is_mouse_clicked_in_button(self.gui[screen_key].buttons[key], mouse_pos):
                self.mouse_clicked_in_button(self.gui[screen_key].buttons[key])
                break