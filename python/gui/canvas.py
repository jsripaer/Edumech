import tkinter as tk

# The maintainer of the image, recieve the coordinates of items and draw them.
# Adaptive window planned.

class PosAdapter:
    """
    The role that transform coordinates, decide whether to move axis.
    Keeping track on the point zero, it will kown how to choose right step, 
    phy_scale and the position of axis and grids.
    """
    pass

class TextBox:
    """
    Implemetion of text boxes that float on the canvas and show some data.
    This object should be adaptive to its content, and can be move from here to
    there.
    """
    def __init__(self, x1, y1, x2, y2, text, color='black'):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.text = text
        self.items = {'l1':0, 'l2':0, 'l3':0, 'l4':0,
                      'text':0}

    def draw_self(self, canvas):
        pass

class Canvas(tk.Canvas):
    def __init__(self, 
                 master, width=750, height=500, phy_scale=20, background='white'):
        super().__init__(
            master=master, width=width, height=height, background=background)
        self.pack(expand=True)
        self.width = width
        self.height = height
        self.half_width = width // 2
        self.half_height = height // 2
        self.zero = (self.half_width, self.half_height)
        # relative to the corner
        self.phy_scale = phy_scale
        # interface coord = (physics coord - central) * phy_scale
        self.axis = {'axis':True, 'grid':False, 'width':2, 'numx':20, 'numy':20,
                     'step':5, 'ax':0, 'ay':0, 'gridx':[], 'gridy':[], 'scalex':[],
                     'scaley':[], 'textx':[], 'texty':[]}
        self.axis['step'] = (width + height) / 40
        # x, y is the serial number of axis.

    def to_corner(self, x, y):
        """
        Given coordinates relative to the upper left corner. Return the coord 
        relative to the central.
        NOTE: this function is likely to be called very frequently, take care
         of performance.
        NOTE: NEVER try to modify the physics data in this class.
        """
        # TODO: involve numpy to process in batch instead 
        x = x * self.phy_scale + self.zero[0]
        y = y * self.phy_scale + self.zero[1]
        return x, y
    
    def to_central(self, x, y):
        # Is this necessary?
        x = (x - self.zero[0]) / self.phy_scale
        y = (y - self.zero[1]) / self.phy_scale
        return x, y

    def dot(self, x, y, r=5, color='black', corner=False):
        if not corner:
            x, y = self.to_corner(x, y)
        return self.create_oval(x-r//2, y-r//2, x+r//2, y+r//2, outline=color, fill=color)
    
    def rectangle(self, x1, y1, x2, y2, color='black', corner=False):
        if not corner:
            x1, y1 = self.to_corner(x1, y1)
            x2, y2 = self.to_corner(x2, y2)
        return self.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)
    
    def square(self, x, y, size, color='black', direction=(1, 1), corner=False):
        """Shortcut of squares. Direction represents how the figure expands."""
        if not corner:
            x, y = self.to_corner(x, y)
        xend = x + size * direction[0]
        yend = y + size * direction[1]
        return self.rectangle(x, y, xend, yend, color=color, corner=corner)
    
    def line(self, x1, y1, x2, y2, width=2, color='black', corner=False):
        if not corner:
            x1, y1 = self.to_corner(x1, y1)
            x2, y2 = self.to_corner(x2, y2)
        return self.create_line(x1, y1, x2, y2, width=width, fill=color)
    
    def arrow(self, x1, y1, x2, y2, width=2, color='black', corner=False):
        """As vectors."""
        if not corner:
            x1, y1 = self.to_corner(x1, y1)
            x2, y2 = self.to_corner(x2, y2)
        return self.create_line(x1, y1, x2, y2, width=width, fill=color, arrow='last')
    
    def text(self, text:str, x, y, color='black', corner=False):
        if not corner:
            x, y = self.to_corner(x, y)
        return self.create_text(x, y, text=text, fill=color)
    
    def darw_axis(self):
        """Interal method to draw the axis. Lazy method that should 
        only be called when the window is moved with some particles."""
        self.delete(self.axis['ax'])
        self.delete(self.axis['ay'])
        x0, y0 = self.zero
        if x0 > self.width - 2:
            x0 = self.width - 2
        elif x0 < 0:
            x0 = 0
        if y0 > self.height - 2:
            y0 = 2
        elif y0 < 0:
            y0 = self.height
        self.axis['ax'] = self.line(x0, 0, x0, self.height, 1, corner=True)
        self.axis['ay'] = self.line(0, y0, self.width, y0, 1, corner=True)

        # Draw scales 
        for i in self.axis['scalex']:
            self.delete(i)
        for j in self.axis['scaley']:
            self.delete(j)
        for i in self.axis['textx']:
            self.delete(i)
        for  j in  self.axis['texty']:
            self.delete(j)
        x, y = 0, 0
        signx, signy = 1, 1
        length = 4
        step = self.axis['step']
        if x0 + step >= self.width:
            signx = - signx
        if y0 + step >= self.height:
            signy = - signy
        while 0 <= y <= self.height:
            i = self.line(x0, y, x0+length*signy, y, width=1, color='grey', corner=True) \
            if not self.axis['grid'] \
            else self.line(0, y, self.width, y, width=1, color='grey', corner=True)
            self.axis['scalex'].append(i)
            _, _y = self.to_central(0, y)
            if _y == 0:
                y += step * signy
                continue
            j = self.text(str(round(_y)), x0-length*signx*2, y, 'grey', corner=True)
            self.axis['textx'].append(j)
            y += step * signy
        while 0 <= x <= self.width:
            i = self.line(x, y0, x, y0+length*signx, width=1, color='grey', corner=True) \
            if not self.axis['grid'] \
            else self.line(x, 0, x, self.height, width=1, color='grey', corner=True)
            self.axis['scaley'].append(i)
            _x, _ = self.to_central(x, 0)
            if _x == 0:
                x += step * signx
                continue
            j = self.text(str(round(_x)), x, y0-length*signx*2, color='grey', corner=True)
            self.axis['texty'].append(j)
            x += step * signx


    def darw_grid(self):
        """See axis.""" 
        x0, y0 = self.zero
        step = self.axis['step'] * self.phy_scale
        xoffset = x0 % step
        yoffset = y0 % step
        while xoffset < self.width:
            i = self.line(xoffset, 0, xoffset, self.height, color='#090909', corner=True)
            self.axis['gridx'].append(i)
            xoffset += step
        while yoffset < self.height:
            i = self.line(0, yoffset, self.width, yoffset, color='#090909', corner=True)
            self.axis['gridy'].append(i)
            yoffset += step

        
    def axisSettings(self, **kwargs):
        """Interface that enables reset parameters of axis."""
        for key in kwargs:
            if key not in self.axis:
                raise KeyError("Unkown parameter name: " + str(key))
            self.axis[key] = kwargs[key]

if __name__ == "__main__":
    # TODO: test for appropriate step and phy_scale.
    master = tk.Tk()
    master.title("Unit test of Canvas")
    canvas = Canvas(master)
    canvas.create_text(60, 20, text='Init zero: ' + (str(canvas.zero)), fill='green')
    canvas.create_rectangle(canvas.width-35, canvas.height-35,
                            canvas.width-25, canvas.height-20, fill='black')
    canvas.line(50, 50, 150, 150, color="blue", corner=True)
    canvas.axisSettings(grid=True)
    canvas.darw_axis()
    a = canvas.rectangle(300, 200, 330, 440, corner=True)
    b = canvas.square(200, 200, 30, color='green', corner=True)
    c = canvas.dot(120, 150, 10, corner=True)
    master.mainloop()