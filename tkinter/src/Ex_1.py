'''
Created on Dec 20, 2014

@author: Duhi
'''
#Testing 
def test_func():
    return

from tkinter import *

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")
    
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "green"
        self.QUIT["command"] = self.quit
        
        self.QUIT.pack({"side":"left"})
        
    def __init__ (self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()