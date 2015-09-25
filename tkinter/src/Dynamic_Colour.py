from Tkinter  import *
root = Tk()
colour = StringVar()
colour.set('blue')
odd_even=0
def colourUpdate():
    global odd_even
    if odd_even % 2 == 0:
        btn.config(bg='red',fg='white')
        l.config(fg='red')
        colour.set('red')
    else:
        btn.config(bg='blue',fg='white')
        l.config(fg='blue')
        colour.set('blue')
    root.update()

    odd_even += 1

btn = Button(root, text = "Click Me", command = colourUpdate)
l = Label(root, textvariable=colour, fg = colour.get())
l.pack()

btn.pack()
root.mainloop()