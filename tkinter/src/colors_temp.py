__author__ = 'mabdul-aziz'
import Tkinter as tk

COLORS_DICT_TEMP = {
               1:'DarkSeaGreen1',
               2:'PaleGreen1',
               3:'PaleGreen2',
               4:'PaleGreen3',
               5:'PaleGreen4',
               6:'SpringGreen2',
               7:'SpringGreen3',
               8:'SpringGreen4',
               9:'green2',
               10:'green3',
               11:'green4',
               12:'green yellow',
               13:'pale green',
               14:'lawn green',
               15:'spring green',
               16:'medium spring green',
               17:'yellow green',
               18:'lime green',
               19:'forest green',
               20:'olive drab',
               21:'DarkSeaGreen2',
               22:'DarkSeaGreen3',
               23:'DarkSeaGreen4',
               24:'SeaGreen1',
               25:'SeaGreen2',
               26:'SeaGreen3',
               27:'chartreuse2',
               28:'chartreuse3',
               29:'chartreuse4',
               30:'OliveDrab1',
               31:'OliveDrab2',
               32:'OliveDrab4',
               33:'DarkOliveGreen1',
               34:'DarkOliveGreen2',
               35:'DarkOliveGreen3',
               36:'DarkOliveGreen4',
               37:'yellow',
               38:'gold',
               39:'yellow2',
               40:'yellow3',
               41:'yellow4',
               42:'gold2',
               43:'gold3',
               44:'gold4',
               45:'goldenrod1',
               46:'goldenrod2',
               47:'goldenrod3',
               48:'goldenrod4',
               49:'DarkGoldenrod1',
               50:'DarkGoldenrod2',
               51:'DarkGoldenrod3',
               52:'DarkGoldenrod4',
               53:'RosyBrown1',
               54:'RosyBrown2',
               55:'orange',
               56:'dark orange',
               57:'light salmon',
               58:'salmon',
               59:'coral',
               60:'tomato',
               61:'orange red',
               62:'red',
               63:'firebrick1',
               64:'firebrick2',
               65:'firebrick3',
               66:'firebrick4',
               67:'brown1',
               68:'brown2',
               69:'brown3',
               70:'brown4',
               71:'salmon1',
               72:'salmon2',
               73:'salmon3',
               74:'salmon4',
               75:'LightSalmon2',
               76:'LightSalmon3',
               77:'LightSalmon4',
               78:'orange2',
               79:'orange3',
               80:'orange4',
               81:'DarkOrange1',
               82:'DarkOrange2',
               83:'DarkOrange3',
               84:'DarkOrange4',
               85:'coral1',
               86:'coral2',
               87:'coral3',
               88:'coral4',
               89:'tomato2',
               90:'tomato3',
               91:'tomato4',
               92:'OrangeRed2',
               93:'OrangeRed3',
               94:'OrangeRed4',
               95:'red2',
               96:'red3',
               97:'red4',
               }


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
for i in range(1,98):
    btn = tk.Button(scframe.interior, height=1, width=20, relief=tk.FLAT,
        bg=COLORS_DICT_TEMP[i], fg='ghost white',
        font="Dosis", text=COLORS_DICT_TEMP[i])
    btn.pack(padx=10, pady=5, side=tk.TOP)

#def openlink(i):
#    print lis[i]

root.mainloop()