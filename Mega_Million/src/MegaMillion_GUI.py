# -*- coding: utf-8 -*-
'''
Created on Dec 10, 2014

@author: Duhi
'''

# from Tkinter import Tk, Frame, BOTH
 
from tkinter import Frame, BOTH, Tk
from tkinter.ttk import Button, Style, Label


class MM_Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        self.parent.title("Centered window")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.initUI()
        
    def initUI(self):
        self.parent.title("Quit button")
        self.style = Style()
        self.style.theme_use("default")

        # self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit",
            command=self.quit)
        quitButton.place(x=200, y=50)
        buttons_list = []
        g=0
        c=0
        for i in range(1,52):
            crnt_button = Label(self, text=str(i),background=FF0000)
            crnt_button.grid(row=g, column=c)
            buttons_list.append(crnt_button)
            c += 1
            if i%10 ==0:
                g +=1
                c=0
    def centerWindow(self):
      
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
  
    root = Tk()
    ex = MM_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()  
