"""
Created on Dec 20, 2014

@author: Duhi
"""
import tkinter
#Testing 
def test_func():
    return



class Application(tkinter.Frame):
    def say_hi(self):
        print("hi there, everyone!")
    
    def createWidgets(self):
        self.QUIT = tkinter.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "green"
        self.QUIT["command"] = self.quit
        
        self.QUIT.pack({"side":"left"})
        
    def __init__ (self,master=None):
        tkinter.Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()