from copy import deepcopy


class CompositionPhase:

    def __init__(self):
        self.players = {
            1: {
                'ships': []
            },
            2: {
                'ships': []
            }
        }
        self.active_ship = None
        self.active_player = 0
        self.last_position = ()
        self.disabled_positions = []
        self.end_phase = False

    def set_starting_ships(self, ships):
        for player in self.players:
            self.players[player]['ships'] = deepcopy(ships)

    def delete_ship(self, player, ship):
        self.players[player]['ships'].remove(ship)

    def start_composition(self, active_player):
        self.active_player = active_player
        self.active_ship = self.players[active_player]['ships'][0]

    def while_composition(self, active_player):
        self.active_ship = self.players[active_player]['ships'][0]

    def on_click(self, board, mouse_position):
        if self.check_can_locate_ship():
            real_position = self.active_ship.return_real_position(self.last_position)
            for part in range(len(self.active_ship.parts)):
                self.active_ship.parts[part]['position'] = real_position[part]
            board.render_objects['boards'][board.active_player]['own_ship'].append(self.active_ship)
            self.delete_ship(board.active_player, self.active_ship)
            self.update_disabled_positions()
            self.active_ship = None
            if len(self.players[board.active_player]['ships']):
                self.active_ship = self.players[board.active_player]['ships'][0]
            else:
                if board.active_player != self.active_player:
                    self.end_phase = True
                    board.toggle_player()
                    return None
                board.toggle_player()
                board.active_board = board.active_player
                self.disabled_positions = []
                self.active_ship = self.players[board.active_player]['ships'][0]
            return True
        else:
            return False

    def check_can_locate_ship(self):
        if self.last_position not in self.disabled_positions:
            if self.active_ship.turn == 'up':
                if self.last_position[1] + len(self.active_ship.parts) > 10:
                    return False
            elif self.active_ship.turn == 'down':
                if self.last_position[1] - len(self.active_ship.parts) < -1:
                    return False
            elif self.active_ship.turn == 'left':
                if self.last_position[0] - len(self.active_ship.parts) < -1:
                    return False
            elif self.active_ship.turn == 'right':
                if self.last_position[0] + len(self.active_ship.parts) > 10:
                    return False

            pos = self.active_ship.return_real_position(self.last_position)
            for position in pos:
                if position in self.disabled_positions:
                    return False
            return True

    def update_disabled_positions(self):
        for x in range(self.last_position[0]-1, self.last_position[0]+2):
            for y in range(self.last_position[1]-1, self.last_position[1]+2):
                self.disabled_positions.append((x, y))