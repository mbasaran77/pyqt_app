from tkinter import *

root = Tk()

def callback(event):
    # TODO: Open keyboard here and remove print statement
    print("focus in event raised, open keyboard")

frame = Frame(root, width=100, height=100)
frame.pack()

addressInput = Entry(frame, font = "Verdana 20 ", justify="center")
addressInput.bind("<FocusIn>", callback)
addressInput.pack()

root.mainloop()