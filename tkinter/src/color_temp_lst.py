__author__ = 'Mohammed'
__author__ = 'mabdul-aziz'
import Tkinter as tk

COLORS_DICT_TEMP = [
                 'DarkOliveGreen1',
                 'DarkOliveGreen2',
                 'DarkOliveGreen3',
                 'DarkSeaGreen1',
                 'PaleGreen1',
                 'PaleGreen2',
                 'PaleGreen3',
                 'PaleGreen4',
                 'SpringGreen2',
                 'SpringGreen3',
                 'SpringGreen4',
                 'green2',
                 'green3',
                 'green4',
                 'green yellow',
                 'pale green',
                 'lawn green',
                 'spring green',
                 'medium spring green',
                 'yellow green',
                 'lime green',
                 'forest green',
                 'olive drab',
                 'DarkSeaGreen2',
                 'DarkSeaGreen3',
                 'DarkSeaGreen4',
                 'SeaGreen1',
                 'SeaGreen2',
                 'SeaGreen3',
                 'chartreuse2',
                 'chartreuse3',
                 'chartreuse4',
                 'OliveDrab1',
                 'OliveDrab2',
                 'OliveDrab4',
                 'DarkOliveGreen4',
                 'yellow',
                 'gold',
                 'yellow2',
                 'yellow3',
                 'yellow4',
                 'gold2',
                 'gold3',
                 'gold4',
                 'goldenrod1',
                 'goldenrod2',
                 'goldenrod3',
                 'goldenrod4',
                 'DarkGoldenrod1',
                 'DarkGoldenrod2',
                 'DarkGoldenrod3',
                 'DarkGoldenrod4',
                 'orange',
                 'dark orange',
                 'light salmon',
                 'salmon',
                 'coral',
                 'tomato',
                 'orange red',
                 'red',
                 'firebrick1',
                 'firebrick2',
                 'firebrick3',
                 'firebrick4',
                 'brown1',
                 'brown2',
                 'brown3',
                 'brown4',
                 'salmon1',
                 'salmon2',
                 'salmon3',
                 'salmon4',
                 'LightSalmon2',
                 'LightSalmon3',
                 'LightSalmon4',
                 'orange2',
                 'orange3',
                 'orange4',
                 'DarkOrange1',
                 'DarkOrange2',
                 'DarkOrange3',
                 'DarkOrange4',
                 'coral1',
                 'coral2',
                 'tomato2',
                 'coral3',
                 'tomato3',
                 'OrangeRed2',
                 'red2',
                 'red3',
                 'OrangeRed3',
                 'OrangeRed4',
                 'coral4',
                 'tomato4',
                 'red4',

               ]


class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


root = tk.Tk()
root.title("Scrollable Frame Demo")
root.configure(background="gray99")

scframe = VerticalScrolledFrame(root)
scframe.pack()

lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
for i in range(1,len(COLORS_DICT_TEMP)):
    btn = tk.Button(scframe.interior, height=1, width=20, relief=tk.FLAT,
        bg=COLORS_DICT_TEMP[i], fg='ghost white',
        font="Dosis", text=COLORS_DICT_TEMP[i])
    btn.pack(padx=10, pady=5, side=tk.TOP)

#def openlink(i):
#    print lis[i]

root.mainloop()