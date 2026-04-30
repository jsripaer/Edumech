import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

type Fn = Callable[[...], Any]

class Window(tk.Tk):
    def __init__(self, window_name:str, window_width: int = 900, widow_height: int = 700, shell_width: int = 300,
                 shell_height: int = 600, top_height: int=15, style_theme: str = 'clam') -> None:
        super().__init__()
        self.window_name = window_name
        self.window_size = (window_width, widow_height)
        self.shell_size = (shell_width, shell_height)
        self.canvas_size = (window_width - shell_width, shell_height)
        self.bottom_size = (window_width, widow_height - shell_height)
        self.top_size = (window_width, top_height)

        self.geometry(f'{self.window_size[0]}x{self.window_size[1]}')
        self.title(window_name)
        self.resizable(True, True)
        self.configure(background='white')

        # self.window = self._create_window()
        self.frame_register: dict[str, tk.Frame] = {}
        self.menu_register: dict[str, tk.Frame] = {}
        self._frame_creat()

        style = ttk.Style()
        style.theme_use(style_theme)

    def _frame_creat(self) -> None:
        # create two layer which is used to split window
        paned_top = tk.PanedWindow(self, width=self.window_size[0], height=self.top_size[1], orient='horizontal')
        paned_top.pack(fill='both', expand=False)
        paned_bottom = ttk.PanedWindow(self, width=self.window_size[0], height=self.window_size[1], orient='vertical')
        paned_bottom.pack(fill='both', expand=True)
        paned_main = ttk.PanedWindow(paned_bottom, width=self.window_size[0], height=self.shell_size[1]+self.top_size[1], orient='horizontal')
        paned_main.pack(fill='x', expand=True)

        # creat frame
        frame_top = tk.Frame(paned_top, width=self.window_size[0], height=self.top_size[1], borderwidth=1, relief='solid')
        frame_left = tk.Frame(paned_main, width=self.shell_size[0], height=self.shell_size[1], borderwidth=1, relief='solid')
        frame_canvas = tk.Frame(paned_main, width=self.canvas_size[0], height=self.canvas_size[1], borderwidth=1, relief='solid')
        frame_bottom = tk.Frame(paned_bottom, width=self.bottom_size[0], height=self.bottom_size[1], borderwidth=1, relief='solid')

        self.frame_register['frame_top'] = frame_top
        self.frame_register['frame_left'] = frame_left
        self.frame_register['frame_canvas'] = frame_canvas
        self.frame_register['frame_bottom'] = frame_bottom

        paned_top.add(frame_top)
        paned_bottom.add(paned_main, weight=self.shell_size[1]//self.bottom_size[1])
        paned_main.add(frame_left, weight=1)
        paned_main.add(frame_canvas, weight=self.canvas_size[0] //self.shell_size[0])
        paned_bottom.add(frame_bottom, weight=1)


if "__main__" == __name__:
    window_name = ''
    w = Window(window_name)
    w.mainloop()
    print(w.frame_register)
