import curses
import block_data
from block import Block
import threading
import time
import copy
import random

BLOCK_STATES = [block_data.BLOCK_I_STATE, block_data.BLOCK_L1_STATE, block_data.BLOCK_L2_STATE, block_data.BLOCK_O_STATE, block_data.BLOCK_T_STATE, block_data.BLOCK_Z1_STATE, block_data.BLOCK_Z2_STATE]
BLOCK_INFOS  = [block_data.BLOCK_I_INFO, block_data.BLOCK_L1_INFO, block_data.BLOCK_L2_INFO, block_data.BLOCK_O_INFO, block_data.BLOCK_T_INFO, block_data.BLOCK_Z1_INFO, block_data.BLOCK_Z2_INFO]
BLOCK_TYPES  = [block_data.TYPE_I, block_data.TYPE_L1, block_data.TYPE_L2, block_data.TYPE_O, block_data.TYPE_T, block_data.TYPE_Z1, block_data.TYPE_Z2]

class Game(object):
    def __init__(self, stdscr):
        self.game_area = copy.deepcopy(block_data.GAME_AREA)
        self.game_area_nlines = 22
        self.game_area_ncols  = 12
        self.win = curses.newwin(self.game_area_nlines, self.game_area_ncols * 2, 0, 0)
        self.current_block_type = random.randint(0, 6) 
        self.current_block = Block(self.win, 3, 3, 1, 5, BLOCK_STATES[self.current_block_type], BLOCK_INFOS[self.current_block_type], BLOCK_TYPES[self.current_block_type])
        self.timer = None
        self.game_over = False
        self.stdscr = stdscr

    def content(self):
        self.win.clear()
        for line in range(self.game_area_nlines):
            for col in range(self.game_area_ncols):
                try:
                    if self.game_area[line][col] == 1 or self.game_area[line][col] == 2:
                        self.win.chgat(line, col * 2, 2, curses.A_REVERSE)
                except curses.error:
                    pass

    def map_block(self):
        b1, b2, b3, b4 = self.current_block.square_pos()
        self.game_area[b1[0]][b1[1]] = 2
        self.game_area[b2[0]][b2[1]] = 2
        self.game_area[b3[0]][b3[1]] = 2
        self.game_area[b4[0]][b4[1]] = 2
    
    def move_left(self):
        b1, b2, b3, b4 = self.current_block.square_pos()
        if self.game_area[b1[0]][b1[1] - 1] != 1 and self.game_area[b2[0]][b2[1] - 1] != 1 and self.game_area[b3[0]][b3[1] - 1] != 1 and self.game_area[b4[0]][b4[1] - 1] != 1:
            self.game_area[b1[0]][b1[1]] = 0
            self.game_area[b2[0]][b2[1]] = 0
            self.game_area[b3[0]][b3[1]] = 0
            self.game_area[b4[0]][b4[1]] = 0
            self.current_block.move_left()

    def move_right(self):
        b1, b2, b3, b4 = self.current_block.square_pos()
        if self.game_area[b1[0]][b1[1] + 1] != 1 and self.game_area[b2[0]][b2[1] + 1] != 1 and self.game_area[b3[0]][b3[1] + 1] != 1 and self.game_area[b4[0]][b4[1] + 1] != 1:
            self.game_area[b1[0]][b1[1]] = 0
            self.game_area[b2[0]][b2[1]] = 0
            self.game_area[b3[0]][b3[1]] = 0
            self.game_area[b4[0]][b4[1]] = 0
            self.current_block.move_right()

    def move_down(self):
        b1, b2, b3, b4 = self.current_block.square_pos()
        if self.game_area[b1[0] + 1][b1[1]] != 1 and self.game_area[b2[0] + 1][b2[1]] != 1 and self.game_area[b3[0] + 1][b3[1]] != 1 and self.game_area[b4[0] + 1][b4[1]] != 1:
            self.game_area[b1[0]][b1[1]] = 0
            self.game_area[b2[0]][b2[1]] = 0
            self.game_area[b3[0]][b3[1]] = 0
            self.game_area[b4[0]][b4[1]] = 0
            self.current_block.move_down()
        else:
            self.game_area[b1[0]][b1[1]] = 1
            self.game_area[b2[0]][b2[1]] = 1
            self.game_area[b3[0]][b3[1]] = 1
            self.game_area[b4[0]][b4[1]] = 1
            line = 20
            while line != 0:
                if self.game_area[line] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                    for index in range(line, 1, -1):
                        self.game_area[index] = self.game_area[index - 1]
                    self.game_area[1] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                else:
                    line = line - 1
                        
            self.current_block_type = random.randint(0, 6)
            self.current_block = Block(self.win, 3, 3, 1, 5, BLOCK_STATES[self.current_block_type], BLOCK_INFOS[self.current_block_type], BLOCK_TYPES[self.current_block_type])
            c1, c2, c3, c4 = self.current_block.square_pos()
            if self.game_area[c1[0]][c1[1]] == 1 or self.game_area[c2[0]][c2[1]] == 1 or self.game_area[c3[0]][c3[1]] == 1 or self.game_area[c4[0]][b4[1]] == 1:
                self.game_over = True
                    


    def change_shape(self):
        self.current_block.change_state()
        b1, b2, b3, b4 = self.current_block.square_pos()
        if self.game_area[b1[0] ][b1[1]] != 1 and self.game_area[b2[0]][b2[1]] != 1 and self.game_area[b3[0]][b3[1]] != 1 and self.game_area[b4[0]][b4[1]] != 1:
            self.current_block.change_state(-1)
            c1, c2, c3, c4 = self.current_block.square_pos()
            self.game_area[c1[0]][c1[1]] = 0
            self.game_area[c2[0]][c2[1]] = 0
            self.game_area[c3[0]][c3[1]] = 0
            self.game_area[c4[0]][c4[1]] = 0
            self.current_block.change_state()
        else:
            self.current_block.change_state(-1)

    def down(self):
        self.move_down()
        if not self.game_over:
            self.map_block()
            self.content()
            self.refresh()
            self.timer = threading.Timer(0.5, self.down)
            self.timer.start()
        else:
            self.game_area = block_data.GAME_AREA.copy()
            self.content()
            self.win.addstr(10, 8, "GAME OVER")
            self.refresh()
            self.current_block = None

    def run(self):
        self.timer = threading.Timer(0.1, self.down)
        self.timer.start()
        while True:
            ch = self.win.getch()
            if self.current_block:
                if ch == ord('a'):
                    self.move_left()
                    self.map_block()
                    self.content()
                    self.refresh()
                elif ch == ord('d'):
                    self.move_right()
                    self.map_block()
                    self.content()
                    self.refresh()
                elif ch == ord('s'):
                    self.move_down()
                    self.map_block()
                    self.content()
                    self.refresh()
                elif ch == ord('w'):
                    self.change_shape()
                    self.map_block()
                    self.content()
                    self.refresh()

    def refresh(self):
        self.win.refresh()
    
    def clear(self):
        self.win.clear()


def main(stdscr):
    curses.curs_set(0)
    stdscr.refresh()
    game = Game(stdscr)
    game.map_block()
    game.content()
    game.refresh()
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)