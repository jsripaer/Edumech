import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import Callable, Any

type Fn = Callable[[Any, ...], Any]

WIDTH = 900
HEIGHT = 700
SHELL_WIDTH = 300
SHELL_HEIGHT = 600
CANVAS_WIDTH = WIDTH - SHELL_WIDTH
CANVAS_HEIGHT = SHELL_HEIGHT
BOTTOM_HEIGHT = HEIGHT - SHELL_HEIGHT
BOTTOM_WIDTH = WIDTH
MENU_HEIGHT = 0

NUM_OF_FRAMES = 4

def event_operation(fn: Fn, *args: Any, **kwargs: Any) -> Callable:
    def event_fn(event: tk.Event):
        fn(*args, **kwargs)
    return event_fn

@dataclass
class Screen:
    root: tk.Tk
    style: ttk.Style
    canvas: tk.Canvas
    frame_list: list[tk.Frame]
    widget: dict[str, tk.Widget]

    def register(self, widget_name: str, widget: tk.Widget) -> None:
        """准备添加装饰器，并将所有widget构建函数全部以装饰器写，这样直接导入该类，不知道可不可行，或者直接在类里构建这些函数"""
        self.widget[widget_name] = widget

def main():
    screen = Screen

    _tk = tk.Tk()
    _tk.geometry(f'{WIDTH}x{HEIGHT}')
    _tk.title('My Test GUI')
    _tk.resizable(True, True)
    _tk.configure(background='white')

    paned_bottom = ttk.PanedWindow(_tk, width=WIDTH, height=HEIGHT, orient='vertical')
    paned_bottom.pack(fill='both', expand=True)
    paned_main = ttk.PanedWindow(paned_bottom, width=WIDTH, height=SHELL_HEIGHT, orient='horizontal')
    paned_main.pack(fill='x', expand=True)

    style = ttk.Style(_tk)
    style.theme_use('clam')

    n = NUM_OF_FRAMES
    frame_list: list[tk.Frame] = []
    for i in range(n):
        if i == 1 or i == 0:
            frame = tk.Frame(paned_main, relief='solid')
        elif i == 2:
            frame = tk.Frame(paned_bottom, relief='solid')
        else:
            frame = ttk.Frame(master=_tk, relief='solid')
        frame_list.append(frame)

    # frame_list 3: 顶栏， frame_list 2: 底栏, frame_list 1: 画布栏, frame_list 0: 左侧栏

    frame_list[3].configure(width=WIDTH, height=MENU_HEIGHT, borderwidth=1)
    frame_list[3].pack(side='top', fill='x')
    frame_list[2].configure(width=BOTTOM_WIDTH, height=BOTTOM_HEIGHT, borderwidth=1)
    # frame_list[2].pack(side='bottom', fill='both')
    frame_list[0].configure(width=SHELL_WIDTH, height=SHELL_HEIGHT, borderwidth=1)
    # frame_list[0].pack(side='left', fill='both')
    frame_list[1].configure(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=1)
    # frame_list[1].pack(side='left', fill='both', expand=True)
    paned_bottom.add(paned_main, weight=SHELL_HEIGHT//BOTTOM_HEIGHT)
    paned_main.add(frame_list[0], weight=1)
    paned_main.add(frame_list[1], weight=CANVAS_WIDTH // SHELL_WIDTH)
    paned_bottom.add(frame_list[2], weight=1)

    menubar = tk.Menu(frame_list[3])
    menubar.add_command(label='Quit', command=_tk.quit)
    _tk.config(menu=menubar)

    label = ttk.Label(master=frame_list[0], text='Hello World')
    label.pack()
    label = ttk.Label(master=frame_list[1], text='Hello World')
    label.pack()
    # 构建画布
    canvas = tk.Canvas(master=frame_list[1], relief='ridge', width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='gray', borderwidth=2)
    canvas.pack(fill='both', expand=True)
    canvas.create_line(0, 0, 100, 100, fill='black')
    var = tk.StringVar()
    var.set('Hello World')

    def label_change(label_: tk.Label, text: str):
        label_.configure(text=text)
    event_function = event_operation(label_change, label, f'{canvas.winfo_width()}x{canvas.winfo_height()}')
    canvas.bind('<Configure>', lambda event: print(canvas.winfo_width()),canvas.update_idletasks())
    label = ttk.Button(master=frame_list[2], textvariable=var)
    label.bind('<Button-1>', event_function)
    label.pack()

    tk.mainloop()

if __name__ == '__main__':
    main()






