import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

class Basic:
    def __init__(self, title = "Basic GUI"):
        """Basic GUI with a menu bar and a canvas"""
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        # Set the title and icon of the window
        self.root.title(title)
        self.frame.pack()
        self.root.iconbitmap(default="./edumech.ico")
        self.menu_bar = tk.Menu(self.frame)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

    def mainloop(self):
        self.root.mainloop()

class Canvas(tk.Canvas):
    """TODO: Should insert pyplot in the canvas."""
    def __init__(self, master, width=400, height=400):
        super().__init__(master, width=width, height=height)
        self.pack()

if __name__ == "__main__":
    gui = Basic()
    gui.mainloop()

    