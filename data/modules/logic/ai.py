from . import composition_phase, shooting_phase
import random


class AI:

    def __init__(self):
        self.shooting_positions = []

    def locate_ship(self, composition_phase, board):
        turns = ['up', 'right', 'down', 'left']
        turn = turns[random.randrange(0, 4)]
        getattr(composition_phase.active_ship, 'rotate_to_' + turn)('right', board.screen.engine.settings.graphic['screen']['resolution_scale'])
        while composition_phase.players[2]['ships']:
            x = random.randrange(0, 9)
            y = random.randrange(0, 9)
            composition_phase.last_position = (x, y)
            composition_phase.on_click(board, None)
            print(len(composition_phase.players[2]['ships']))

    def shoot(self, shooting_phase, board):
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        shooting_phase.shoot(board, (x, y))

    def run(self, engine, board):
        if isinstance(engine.phase, composition_phase.CompositionPhase):
            self.locate_ship(engine.phase, board)
        else:
            self.shoot(engine.phase, board)