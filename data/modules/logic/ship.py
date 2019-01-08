import pygame


class Ship:

    def __init__(self):
        self.turns = ['up', 'right', 'down', 'left']
        self.turn = 'up'
        self.destroyed = False
        self.parts = []

    def change_turn(self, turn, scale):
        if turn == 'left':
            for _turn in range(len(self.turns)):
                if self.turns[_turn] == self.turn:
                    self.turn = self.turns[_turn-1]
                    break
        else:
            for _turn in range(len(self.turns)):
                if self.turns[_turn] == self.turn:
                    if _turn == len(self.turns)-1:
                        self.turn = self.turns[0]
                    else:
                        self.turn = self.turns[_turn+1]

        getattr(self, 'rotate_to_' + self.turn)(turn, scale)

    def rotate_to_up(self, turn, scale):
        for part in range(len(self.parts)):
            self.parts[part]['position'] = (0, 80 * part * scale[1])
        self.rotate_image(turn)

    def rotate_to_right(self, turn, scale):
        for part in range(len(self.parts)):
            self.parts[part]['position'] = (80 * part * scale[0], 0)
        self.rotate_image(turn)

    def rotate_to_down(self, turn, scale):
        for part in range(len(self.parts)):
            self.parts[part]['position'] = (0, -80 * part * scale[1])
        self.rotate_image(turn)

    def rotate_to_left(self, turn, scale):
        for part in range(len(self.parts)):
            self.parts[part]['position'] = (-80 * part * scale[0], 0)
        self.rotate_image(turn)

    def rotate_image(self, turn):
        if turn == 'left':
            for part in self.parts:
                part['render'] = pygame.transform.rotate(part['render'], -90)
        elif turn == 'right':
            for part in self.parts:
                part['render'] = pygame.transform.rotate(part['render'], 90)

    def return_real_position(self, position):
        positions = []
        if self.turn == 'up':
            for parts in range(len(self.parts)):
                positions.append((position[0], position[1]+parts))
        elif self.turn == 'right':
            for parts in range(len(self.parts)):
                positions.append((position[0]+parts, position[1]))
        elif self.turn == 'left':
            for parts in range(len(self.parts)):
                positions.append((position[0]-parts, position[1]))
        else:
            for parts in range(len(self.parts)):
                positions.append((position[0], position[1] - parts))
        return positions


    def create(self, parts, scale):
        for part in range(parts):
            x = {
                'render': part,
                'position': (),
            }
            self.parts.append(x)
        self.rotate_to_up('None', scale)