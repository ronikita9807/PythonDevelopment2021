import tkinter
from dataclasses import dataclass
from tkinter import *
from tkinter import messagebox
import random

window = Tk()
window.title("15 game")
window.geometry("500x500")

btn_size = 2


@dataclass
class State:
    column: int
    row: int


game_state = State(column=3, row=3)


def start_game():
    global game_state
    new_order = list(range(15))
    random.shuffle(new_order)
    for i, btn_idx in enumerate(new_order):
        btns[btn_idx].grid(
            column=i % 4 * btn_size,
            row=i // 4 * btn_size + 1,
            columnspan=btn_size,
            rowspan=btn_size,
            sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W,
        )
    game_state = State(column=3, row=3)


def exit_game():
    window.destroy()


def check_winning():
    for i, btn in enumerate(btns):
        info = btn.grid_info()
        col = info["column"] // btn_size
        row = info["row"] // btn_size
        if col == i % 4 and row == i // 4:
            continue
        else:
            return
    messagebox.showinfo("Result game", "YOU WIN!")
    start_game()
    return


def check_boundaries(col, row):
    return abs(game_state.column - col) + abs(game_state.row - row) > 1


def moving_btn(btn_idx):
    idx = btn_idx

    def move_btn():
        global game_state
        grid_info = btns[idx].grid_info()
        col = grid_info["column"] // grid_info["columnspan"]
        row = grid_info["row"] // grid_info["rowspan"]
        if check_boundaries(col, row):
            return
        btns[idx].grid_configure(
            column=game_state.column * btn_size, row=game_state.row * btn_size + 1
        )
        game_state = State(column=col, row=row)
        check_winning()

    return move_btn


for i in range(8):
    window.grid_columnconfigure(i, weight=10)
    window.grid_rowconfigure(i + 1, weight=10)

btns = [
    Button(window, text=str(i + 1), bg="#54FA9B", command=moving_btn(i))
    for i in range(15)
]

new_btn = Button(window, text="New", bg="green", command=start_game)
new_btn.grid(
    column=1,
    row=0,
    columnspan=btn_size,
    sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W,
)

exit_btn = Button(window, text="Exit", bg="red", command=exit_game)
exit_btn.grid(
    column=5,
    row=0,
    columnspan=btn_size,
    sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W,
)

start_game()

window.mainloop()
