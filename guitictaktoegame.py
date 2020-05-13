# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:13:09 2020

@author: himan
"""

import random

import tkinter as tk
import tkinter.ttk as ttk


class AppMain:

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master, width=250, height=150, relief='groove')
        self.frame.pack_propagate(False)
        self.play = ttk.Button(self.frame, text='Play',
                               command=lambda: PlayMenu(do=0))
        self.settings = ttk.Button(self.frame, text='Settings',
                                   command=SettingsWindow)
        self.qb = ttk.Button(self.frame, text="Quit", command=root.destroy)

        self.main_window()

    def main_window(self):
        self.remove_widgets()
        self.frame.pack(padx=25, pady=75)
        self.play.pack(side='top', pady=(33, 0))
        self.settings.pack(side='top', pady=5)
        self.qb.pack(side='top', pady=(0, 32))

    def remove_widgets(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()


class SettingsWindow(AppMain):

    def __init__(self):
        self.frame = ttk.Frame(root, width=250, height=150, relief='groove')
        self.frame.pack_propagate(False)
        self.rb1 = ttk.Radiobutton(self.frame, text='Easy', variable=mode,
                                   value=0)
        self.rb2 = ttk.Radiobutton(self.frame, text='Impossible',
                                   variable=mode, value=1)
        self.rb3 = ttk.Radiobutton(self.frame, text='2 players',
                                   variable=mode, value=2)
        self.back = ttk.Button(self.frame, text='Back',
                               command=lambda: AppMain(master=root))

        self.settings_window()

    def settings_window(self):
        r = AppMain(master=root)
        r.remove_widgets()
        self.frame.pack(padx=25, pady=75)
        self.rb1.pack(side='top', pady=(10, 0))
        self.rb2.pack(side='top', pady=(10, 0))
        self.rb3.pack(side='top', padx=(0, 22), pady=(10, 0))
        self.back.pack(side='top', pady=(16, 16))


class PlayMenu(AppMain):

    def __init__(self, do):
        self.do = do
        self.label = ttk.Label(root, text='Choose your side',
                               font=('French Script MT', 20))
        self.frame = ttk.Frame(root, width=250, height=150, relief='groove')
        self.frame.pack_propagate(False)
        self.player_x = ttk.Button(self.frame, text='X',
                                   command=lambda: GameWindow(pl='X', pc='O'))
        self.player_o = ttk.Button(self.frame, text='O',
                                   command=lambda: GameWindow(pl='O', pc='X'))
        self.back = ttk.Button(self.frame, text='Back',
                               command=lambda: AppMain(master=root))

        if do == 'redeclare':
            global statusLib
            statusLib = [None for v in range(9)]

        self.play_menu()

    def play_menu(self):
        r = AppMain(master=root)
        r.remove_widgets()
        self.label.pack(side='top', pady=(25, 0))
        self.frame.pack(padx=25, pady=25)
        self.player_x.grid(column=0, row=0, padx=(5, 0), pady=(5, 0))
        self.player_o.grid(column=1, row=0, padx=(0, 5), pady=(5, 0))
        self.back.grid(column=0, row=1, sticky='w, e', padx=(5, 5), pady=(0, 5),
                       columnspan=2)


class GameWindow(AppMain):

    def __init__(self, pl, pc):
        self.pl, self.pc, self.stop_game = pl, pc, False
        self.frame = ttk.Frame(root, width=650, height=700)
        self.frame.pack_propagate(False)
        self.canvas = tk.Canvas(self.frame, width=600, height=600)
        self.restart = ttk.Button(self.frame, text='Restart',
                                  command=lambda: PlayMenu(do='redeclare'))
        self.game_window()

    def game_window(self):
        r = AppMain(master=root)
        r.remove_widgets()
        self.frame.pack()
        self.canvas.pack(side='top', pady=(25, 0))
        self.restart.pack(side='bottom', pady=20)
        self.draw_board()
        self.canvas.bind('<Button-1>', self.square_selector)
        if self.pl == 'O':
            self.computer_move()

    def draw_board(self):
        self.canvas.create_line(0, 200, 600, 200)
        self.canvas.create_line(0, 400, 600, 400)
        self.canvas.create_line(200, 0, 200, 600)
        self.canvas.create_line(400, 0, 400, 600)

    def square_selector(self, event):
        self.player_move(square=(event.x // 200 * 3 + event.y // 200))

    def player_move(self, square):
        if statusLib[square] is None:
            self.make_move(sq=square, symbol=self.pl, turn='player')
            if not self.stop_game:
                self.computer_move()

    def computer_move(self):
        status, square = 0, None
        while status is not None:
            square = random.randint(0, 8)
            status = statusLib[square]
        self.make_move(sq=square, symbol=self.pc, turn='computer')

    def make_move(self, sq, symbol, turn):
        self.draw_move(symbol=symbol, sq=sq)
        statusLib[sq] = symbol
        self.end_game(this_move=turn, symbol=symbol)

    def draw_move(self, symbol, sq):
        pos = [100 + sq // 3 * 200, 100 + sq % 3 * 200]
        self.canvas.create_text(pos, text=symbol, font=('French Script MT', 50),
                                anchor='center')

    def end_game(self, this_move, symbol):
        condition = self.check_end_game(symbol=symbol)
        self.stop_game = condition[0]
        text = ''
        if condition[0]:
            self.canvas.unbind('<Button-1>')
            if this_move == 'player' and not condition[1]:
                text = 'You win'
            elif this_move == 'computer' and not condition[1]:
                text = 'You lose'
            elif condition[1]:
                text = 'It\'s a tie'
            self.finisher(fin=condition[2])
            self.canvas.create_text(300, 300, text=text,
                                    font=('French Script MT', 50),
                                    fill='#EE2C2C')

    @staticmethod
    def check_end_game(symbol):
        if statusLib[0] == statusLib[1] == statusLib[2] == symbol:
            return [True, False, 1]
        elif statusLib[3] == statusLib[4] == statusLib[5] == symbol:
            return [True, False, 2]
        elif statusLib[6] == statusLib[7] == statusLib[8] == symbol:
            return [True, False, 3]
        elif statusLib[0] == statusLib[3] == statusLib[6] == symbol:
            return [True, False, 4]
        elif statusLib[1] == statusLib[4] == statusLib[7] == symbol:
            return [True, False, 5]
        elif statusLib[2] == statusLib[5] == statusLib[8] == symbol:
            return [True, False, 6]
        elif statusLib[2] == statusLib[4] == statusLib[6] == symbol:
            return [True, False, 7]
        elif statusLib[0] == statusLib[4] == statusLib[8] == symbol:
            return [True, False, 8]
        elif all(k is not None for k in statusLib):
            return [True, True, 0]
        else:
            return [False, False, 0]

    def finisher(self, fin):
        lib = [[100, 100, 100, 500], [300, 100, 300, 500], [500, 100, 500, 500],
               [100, 100, 500, 100], [100, 300, 500, 300], [100, 500, 500, 500],
               [500, 100, 100, 500], [100, 100, 500, 500]]
        if fin != 0:
            self.canvas.create_line(lib[fin - 1][0], lib[fin - 1][1],
                                    lib[fin - 1][2], lib[fin - 1][3],
                                    fill='#1874CD', width=5)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tic Tac Toe')
    root.minsize(width=300, height=300)

    statusLib = [None for i in range(9)]
    mode = tk.IntVar()

    AppMain(master=root)
    root.mainloop()