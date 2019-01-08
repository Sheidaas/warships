class ShootingPhase:

    def __init__(self):
        self.end_phase = False

    def on_click(self, board, mouse_position):
        localization = board.locate_mouse(mouse_position)
        if localization:
            if self.can_shoot(board, localization):
                self.shoot(board, localization)

    def can_shoot(self, board, localization):
        if localization not in board.render_objects['boards'][board.active_player]['shoots']:
            return True
        return False

    def shoot(self, board, localization, ai=None):
        board.render_objects['boards'][board.active_player]['shoots'].append(localization)
        if not self.if_hit(board, localization, ai):
            board.toggle_player()
            board.mixer.play_song('miss')
            if board.active_player == 1:
                board.active_board = 2
            else:
                board.active_board = 1

    def if_hit(self, board, localization, ai=None):
        player = 1
        if board.active_player == 1:
            player = 2
        for ship in board.render_objects['boards'][player]['own_ship']:
            for part in ship.parts:
                if localization == part['position']:
                    if self.is_destroyed(board, ship):
                        ship.destroyed = True
                        if not ai == None:
                            ai.attacking_ship['destroyed'] = True
                            ai.attacking_ship['hit'] = False
                        board.mixer.play_song('destroy')
                    else:
                        if not ai == None:
                            ai.attacking_ship['hit'] = True
                            ai.attacking_ship['destroyed'] = False
                        board.mixer.play_song('hit')
                    return True
        if not ai == None:
            ai.attacking_ship['hit'] = False
            ai.attacking_ship['destroyed'] = False
        return False

    def is_destroyed(self, board, ship):
        destroyed = False
        for part in ship.parts:
            for shoot in board.render_objects['boards'][board.active_player]['shoots']:
                if part['position'] == shoot:
                    destroyed = True
                    break
                else:
                    destroyed = False
        return destroyed

    def check_win(self, board):
        winner = False
        for ship in board.render_objects['boards'][2]['own_ship']:
            if ship.destroyed:
                winner = True
            else:
                winner = False
                break
        if winner:
            return 1

        for ship in board.render_objects['boards'][1]['own_ship']:
            if ship.destroyed:
                winner = True
            else:
                winner = False
                break
        if winner:
            return 2

        return 0