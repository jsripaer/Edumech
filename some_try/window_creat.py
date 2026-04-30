import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

type Fn = Callable[[...], Any]

WIDTH = 900
HEIGHT = 700
SHELL_WIDTH = 300
SHELL_HEIGHT = 600
CANVAS_WIDTH = WIDTH - SHELL_WIDTH
CANVAS_HEIGHT = SHELL_HEIGHT
BOTTOM_HEIGHT = HEIGHT - SHELL_HEIGHT
BOTTOM_WIDTH = WIDTH
MENU_HEIGHT = 15


FRAME_REGISTER: dict[str, tk.Frame] = {}
MENU_REGISTER: dict[str, tk.Frame] = {}

def create_window(window_name: str, ) -> tk.Tk:
    # create root
    _tk = tk.Tk()
    _tk.geometry(f'{WIDTH}x{HEIGHT}')
    _tk.title(window_name)
    _tk.resizable(True, True)
    _tk.configure(background='white')

    # create two layer which is used to split window
    paned_top = tk.PanedWindow(_tk, width=WIDTH, height=MENU_HEIGHT, orient='horizontal')
    paned_top.pack(fill='both', expand=False)
    paned_bottom = ttk.PanedWindow(_tk, width=WIDTH, height=HEIGHT, orient='vertical')
    paned_bottom.pack(fill='both', expand=True)
    paned_main = ttk.PanedWindow(paned_bottom, width=WIDTH, height=SHELL_HEIGHT+MENU_HEIGHT, orient='horizontal')
    paned_main.pack(fill='x', expand=True)

    style = ttk.Style()
    style.theme_use('clam')

    # creat frame
    frame_top = tk.Frame(paned_top, width=WIDTH, height=MENU_HEIGHT, borderwidth=1, relief='solid')
    frame_left = tk.Frame(paned_main, width=SHELL_WIDTH, height=SHELL_HEIGHT, borderwidth=1, relief='solid')
    frame_canvas = tk.Frame(paned_main, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=1, relief='solid')
    frame_bottom = tk.Frame(paned_bottom, width=BOTTOM_WIDTH, height=BOTTOM_HEIGHT, borderwidth=1, relief='solid')

    FRAME_REGISTER['frame_top'] = frame_top
    FRAME_REGISTER['frame_left'] = frame_left
    FRAME_REGISTER['frame_canvas'] = frame_canvas
    FRAME_REGISTER['frame_bottom'] = frame_bottom

    paned_top.add(frame_top)
    paned_bottom.add(paned_main, weight=SHELL_HEIGHT//BOTTOM_HEIGHT)
    paned_main.add(frame_left, weight=1)
    paned_main.add(frame_canvas, weight=CANVAS_WIDTH // SHELL_WIDTH)
    paned_bottom.add(frame_bottom, weight=1)

    return _tk

if "__main__" == __name__:
    window_name = ''
    window = create_window(window_name)
    menu = tk.Menu(FRAME_REGISTER['frame_top'], tearoff=1)
    menu.add_command(label='Exit', command=window.destroy)
    window.config(menu=menu)
    window.mainloop()