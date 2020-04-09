from tkinter import *
from tkinter.ttk import *
from password import Password
from tkinter import messagebox
import re

if __name__ == "__main__":
    window = Tk()

    window.title("MTH312 Project")
    window.geometry('575x300')

    diff = IntVar()
    # window.passDispFlag = True
    window.passLimit = 16


def testVal(P):
    if not (re.fullmatch(r'(\S|\b)*', P)):
        return False
    if len(P) > window.passLimit:
        return False
    return True


def passwordUpdate(message):
    knownLbl.configure(text=message)
    window.update()


def checkStrength():
    enterBtn.configure(state="disabled")
    passBox.configure(state="disabled")
    window.update()
    if len(passBox.get()) > 0:
        Password(passBox.get(), passwordUpdate)
    else:
        knownLbl.configure(text="enter a password to test")
    enterBtn.configure(state="enabled")
    passBox.configure(state="enabled")


def about():
    messagebox.showinfo('MTH312 Project', "A MTH312 project by:\nJohn Bonazzi and Benjamin Brown")

if __name__ == "__main__":
    passLbl = Label(window, text="Enter \"Password\":")
    passBox = Entry(window, width=20, validate="key")
    passBox.configure(validatecommand=(passBox.register(testVal), '%P'))
    knownLbl = Label(window, wraplength=550, text="")
    enterBtn = Button(window, text="Check Strength", command=checkStrength)
    fileMenu = Menu(window)
    fileItems = Menu(fileMenu)

    fileItems.add_command(label='Exit', command=window.destroy)
    fileItems.add_command(label='About', command=about)

    fileMenu.add_cascade(label='File', menu=fileItems)
#    passLbl.grid(column=0, row=0)
#    passBox.grid(column=0, row=1)
#    enterBtn.grid(column=0, row=2)
#    knownLbl.grid(column=0, row=3)

    passLbl.pack()
    passBox.pack()
    enterBtn.pack()
    knownLbl.pack(fill=BOTH)


    window.config(menu=fileMenu)
    passBox.focus()
    diff.set(1)
    window.update()

    window.mainloop()
