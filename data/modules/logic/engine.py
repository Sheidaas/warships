from data.modules.logic import database, settings_loader, ship as sh, composition_phase, shooting_phase, scoreboard_loader


class GameEngine:

    def __init__(self, path):
        self.path = path
        self.settings = settings_loader.SettingsLoader(self.path, '/settings.ini').return_settings()
        self.database = database.Database(self.path, self.settings.primary_settings['language'])
        self.phase = None
        self.ai = False

    def save_settings(self):
        settings = {
            '1': self.settings.primary_settings,
            '2': self.settings.graphic
        }
        saver = settings_loader.SettingsLoader(self.path, '/settings.ini')
        saver.settings = settings
        saver.save_settings()

    def save_score(self):
        saver = scoreboard_loader.ScoreLoader(self.path)
        saver.score = self.bubble_sort(self.database.scoreboard.score)
        self.database.scoreboard.score = saver.score
        saver.save_score()

    def new_game(self, screen_gui, ai):
        self.ai = ai
        screen_gui['board'] = True
        _ships = []
        for ships in self.settings.primary_settings['ships']:
            for ship in range(self.settings.primary_settings['ships'][ships]):
                _ship = sh.Ship()
                _ship.create(int(ships), self.settings.graphic['screen']['resolution_scale'])
                _ships.append(_ship)

        self.phase = composition_phase.CompositionPhase()
        self.phase.set_starting_ships(_ships)

        import random
        active_player = random.randrange(1, 2)
        self.phase.start_composition(active_player)

    def next_phase(self):
        if isinstance(self.phase, composition_phase.CompositionPhase):
            self.phase = shooting_phase.ShootingPhase()

    def end_game(self, player, points):
        score = {
            'winner': 'Player ' + str(player),
            'score': points,
        }
        self.database.scoreboard.score[len(self.database.scoreboard.score)+1] = score
        self.save_score()

    def bubble_sort(self, scoreboard):
        new_scoreboard = [scoreboard[x] for x in scoreboard]

        for x in range(len(new_scoreboard)-1):
            for y in range(len(new_scoreboard)-1):
                if new_scoreboard[y]['score'] < new_scoreboard[y+1]['score']:
                    new_scoreboard[y]['score'], new_scoreboard[y + 1]['score'] = new_scoreboard[y+1]['score'], new_scoreboard[y]['score']

        score = {}
        for x in range(10):
            try:
                score[x] = new_scoreboard[x]
            except IndexError:
                break
        return score






