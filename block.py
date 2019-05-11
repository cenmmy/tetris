import curses

class Block(object):
    def __init__(self, win, nlines, ncols, begin_y, begin_x, states, info, type):
        """ 初始化函数 """
        self.win = win
        self.nlines = nlines
        self.ncols = ncols
        self.begin_y = begin_y
        self.begin_x = begin_x
        self.states = states
        self.info = info
        self.type = type
        self.current_state = 0

    def change_state(self, plus=1):
        """ 改变当前的状态 """
        if plus == 1:
            self.current_state = (self.current_state + 1) % (len(self.states) - 1)
        else:
            self.current_state = (self.current_state - 1) % (len(self.states) - 1)
    
    def square_pos(self):
        """ 返回有方块的位置 """
        res = []
        for y, x in self.info[self.current_state]:
            res.append((self.begin_y + y, self.begin_x + x))
        return res

    def content(self):
        """ 在win中画出方块 """
        for line in range(self.nlines):
            for col in range(self.ncols):
                if self.states[self.current_state][line][col] == 1:
                    self.win.chgat(self.begin_y + line, self.begin_x + col * 2, 2, curses.A_REVERSE)

    def clear(self):
        """ 清除win中方块 """
        for line in range(self.nlines):
            for col in range(self.ncols):
                self.win.chgat(self.begin_y + line, self.begin_x + col * 2, 2, curses.A_NORMAL)

    def refresh(self):
        """ 刷新 """
        self.win.refresh()
    
    def move_down(self):
        """ 方块向下移动 """
        self.begin_y = self.begin_y + 1
    
    def move_right(self):
        """  方块向右移动 """
        self.begin_x = self.begin_x + 1
    
    def move_left(self):
        """  方块向左移动 """
        self.begin_x = self.begin_x - 1