'''
Created on Feb 23, 2015

@author: Duhi
'''
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
        #TODO: Create a factory method to dynamically create buttons
        #import Tkinter as tk

        #for i in range(boardWidth):
        #    newButton = tk.Button(root, text=str(i+1),
        #        command=lambda j=i+1: Board.playColumn(j, Board.getCurrentPlayer()))
        #Board.boardButtons.append(newButton)
        
        #TODO: pack() or grid() to display the button
        #TODO: convert the background (bg) to accept values
        #TODO: 
        self.button1=Button(self)
        self.button1['text']=1
        self.button1['bg']='green'
        self.button1.pack({"side": "left"})
        
        self.button2=Button(self)
        self.button2['text']=2
        self.button2['bg']='green'
        self.button2.pack({"side": "left"})
        
        self.button3=Button(self)
        self.button3['text']=3
        self.button3['bg']='green'
        self.button3.pack({"side": "left"})
        
        self.button4=Button(self)
        self.button4['text']=4
        self.button4['bg']='green'
        self.button4.pack({"side": "left"})
        
        self.button5=Button(self)
        self.button5['text']=5
        self.button5['bg']='green'
        self.button5.pack({"side": "left"})
        
        self.button6=Button(self)
        self.button6['text']=6
        self.button6['bg']='orange'
        self.button6.pack({"side": "left"})
        
        self.button7=Button(self)
        self.button7['text']=7
        self.button7['bg']='yellow'
        self.button7.pack({"side": "left"})
        
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