#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from random import randrange, choice
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions      = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))


class Game(object):
    def __init__(self, height=4, width=4, winval=2048):
        self.height = height
        self.width  = width
        self.winval = winval
        # self.state  = 'Game'
        self.score  = 0
        self.hghscr = 0
        self.reset()

    def mainloop(self, stdscr):
        def init():
            self.reset()
            self.state = 'Game'

        def no_game(state):
            self.draw_matrix(stdscr)
            action = self.get_user_action(stdscr)
            resp   = defaultdict(lambda: state)
            resp['Restart'], resp['Exit'] = 'Init', 'Exit'
            self.state = resp[action]

        def game():
            self.draw_matrix(stdscr)
            action = self.get_user_action(stdscr)
            if action == 'Restart':
                self.state = 'Init'
            elif action == 'Exit':
                self.state = 'Exit'
            elif self.move(action):
                if self.is_win():
                    self.state = 'Win'
                elif self.is_gameover():
                    self.state = 'Gameover'
            else:
                self.state = 'Game'
        
        state_actions = {
            'Init': init,
            'Win': no_game('Win'),
            'Gameover': no_game('Gameover'),
            'Game': game,
        }
        # self.state = 'Init'
        self.state = 'Game'
        while self.state != 'Exit':
            state_actions[self.state]()
            # print(self.state)

    def reset(self):
        self.hghscr = max(self.hghscr, self.score)
        self.score  = 0
        self.matrix = [[0 for w in range(self.width)] for h in range(self.height)]
        self.spawn()
        self.spawn()

    def spawn(self):
        w, h = choice([(w, h) for w in range(self.width) for h in range(self.height) if self.matrix[w][h] == 0])
        self.matrix[w][h] = 4 if randrange(100) > 89 else 2

    def move(self, direction):
        def move_row_left(row):
            def tighten(row):
                new_row = [r for r in row if r != 0]
                new_row += [0 for _ in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                p       = False
                new_row = []
                for i, r in enumerate(row):
                    if p:
                        new_row    += [2 * r]
                        self.score += 2 * r
                        p          = False
                    else:
                        if i + 1 < len(row) and r == row[i + 1]:
                            p       = True
                            new_row += [0]
                        else:
                            new_row += [r]
                assert len(new_row) == len(row)
                return new_row

            return tighten(merge(tighten(row)))

        moves = {
            'Left': lambda matrix: [move_row_left(row) for row in matrix],
            'Right': lambda matrix: self.invert(moves.get('Left')(self.invert(matrix))),
            'Up': lambda matrix: self.T(moves.get('Left')(self.T(matrix))),
            'Down': lambda matrix: self.T(moves.get('Right')(self.T(matrix)))
        }
        if direction in moves:
            if self.can_move(direction):
                self.matrix = moves[direction](self.matrix)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(m >= self.winval for m in row) for row in self.matrix)

    def is_gameover(self):
        return not any(self.can_move(action) for action in actions)

    def can_move(self, direction):
        def can_move_row_left(row):
            def change(r):
                if (row[r] == 0 and row[r + 1] != 0) or \
                   (row[r] != 0 and row[r] == row[r + 1]):
                    return True
                return False

            return any(change(r) for r in range(len(row[:-1])))

        check = {
            'Left': lambda matrix: any(can_move_row_left(row) for row in matrix),
            'Right': lambda matrix: check.get('Left')(self.invert(matrix)),
            'Up': lambda matrix: check.get('Left')(self.T(matrix)),
            'Down': lambda matrix: check.get('Right')(self.T(matrix))
        }
        if direction in check:
            return check[direction](self.matrix)
        else:
            return False

    def draw_matrix(self, screen):
        help_str1 = '(W)Up/(S)Down/(A)Left/(D)Right'
        help_str2 = '(R)estart/(Q)Exit'
        gameover  = 'GAMEOVER'
        win       = 'YOUWIN!'

        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_sep():
            line = '+' + ('+-----' * self.width + '+')[1:]
            sep  = defaultdict(lambda: line)
            if not hasattr(draw_hor_sep, 'counter'):
                draw_hor_sep.counter = 0
            cast(sep[draw_hor_sep.counter])
            # cast(line)
            draw_hor_sep.counter += 1

        def draw_row(row):
            cast(''.join('|{:^5}'.format(num) if num > 0 else '|     ' for num in row) + '|')

        screen.clear()
        cast('SCORE: {}'.format(self.score))
        if self.hghscr != 0:
            cast('HIGHSCORE: {}'.format(self.hghscr))
        for row in self.matrix:
            draw_hor_sep()
            draw_row(row)
        draw_hor_sep()
        if self.is_win():
            cast(win)
        elif self.is_gameover():
            cast(gameover)
        else:
            cast(help_str1)
            cast(help_str2)

    def get_user_action(self, keyboard):
        char = None
        while char not in actions_dict:
            char = keyboard.getch()
        return actions_dict[char]

    def T(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def invert(self, matrix):
        return [row[::-1] for row in matrix]


if __name__ == '__main__':
    g = Game(8, 8, 1<<16)
    curses.wrapper(g.mainloop)
