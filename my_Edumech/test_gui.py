import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

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


    style = ttk.Style(_tk)
    style.theme_use('clam')

    n = NUM_OF_FRAMES
    frame_list: list[tk.Frame] = []
    for i in range(n):
        frame = ttk.Frame(master=_tk, relief='solid')
        frame_list.append(frame)

    # frame_list 3: 顶栏， frame_list 2: 底栏, frame_list 1: 画布栏, frame_list 0: 左侧栏

    frame_list[3].configure(width=WIDTH, height=MENU_HEIGHT, borderwidth=1)
    frame_list[3].pack(side='top', fill='x')
    frame_list[2].configure(width=BOTTOM_WIDTH, height=BOTTOM_HEIGHT, borderwidth=1)
    frame_list[2].pack(side='bottom', fill='both')
    frame_list[0].configure(width=SHELL_WIDTH, height=SHELL_HEIGHT, borderwidth=1)
    frame_list[0].pack(side='left', fill='both')
    frame_list[1].configure(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=1)
    frame_list[1].pack(side='left', fill='both', expand=True)

    menubar = tk.Menu(frame_list[3])
    menubar.add_command(label='Quit', command=_tk.quit)
    _tk.config(menu=menubar)

    label = ttk.Label(master=frame_list[0], text='Hello World')
    label.pack()
    label = ttk.Label(master=frame_list[1], text='Hello World')
    label.pack()
    # 构建画布
    canvas = tk.Canvas(master=frame_list[1], relief='solid', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack(fill='both', expand=True)

    tk.mainloop()

if __name__ == '__main__':
    main()






