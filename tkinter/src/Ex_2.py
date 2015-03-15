'''
Created on Feb 8, 2015

@author: Duhi
'''
from Tkinter import *

class Application(Frame):
     
    
    def say_hi(self):
        print "hi there, everyone!"
        #self.txt_box["text"] = "hi there, everyone!" + str(self.cnt)
        self.cnt += 1
        self.hi_there["text"] = "Hello", str(self.cnt) 
        
        

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello", str(self.cnt)
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})
        
        self.mm_numbers = Frame(self)
        self.pack({"side": "left"})
        #self.txt_box = Text(self)
        #self.txt_box.pack({"side": "left"} )
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.cnt = 0
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()