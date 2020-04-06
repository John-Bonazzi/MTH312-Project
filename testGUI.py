from tkinter import *
from tkinter.ttk import *
from password import Password
from tkinter import messagebox
import re

if __name__ == "__main__":
    window = Tk()


    window.title("MTH312 Project")
    window.geometry('350x250')

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
    # if message == "GAME OVER":
    #    enterBtn.configure(state="enabled")
    #    passBox.configure(state="enabled")
    #    window.passDispFlag = False
    #    messagebox.showinfo("YOU WIN!", "The test took too long and timed out,\n "
    #                                    "congratulations! Your Password is secure")
    #    knownLbl.configure(text="")
    # elif window.passDispFlag:
    knownLbl.configure(text=message)
    window.update()


def checkStrength():
    if len(passBox.get()) > 0:
        Password(passBox.get(), passwordUpdate)
        # enterBtn.configure(state="disabled")
        # passBox.configure(state="disabled")
        # window.passDispFlag = True
    else:
        knownLbl.configure(text="enter a password to test")


def about():
    messagebox.showinfo('MTH312 Project', "A MTH312 project by:\nJohn Bonazzi and Benjamin Brown")

if __name__ == "__main__":
    passLbl = Label(window, text="Enter \"Password\":")
    passBox = Entry(window, width=20, validate="key")
    passBox.configure(validatecommand=(passBox.register(testVal), '%P'))
    knownLbl = Label(window, text="")
    enterBtn = Button(window, text="Check Strength", command=checkStrength)
    timeLbl = Label(window, text="")
    fileMenu = Menu(window)
    fileItems = Menu(fileMenu)

    fileItems.add_command(label='Exit', command=window.destroy)
    fileItems.add_command(label='About', command=about)

    fileMenu.add_cascade(label='File', menu=fileItems)
    passLbl.grid(column=0, row=0)
    passBox.grid(column=0, row=1)
    enterBtn.grid(column=1, row=1)
    knownLbl.grid(column=0, row=2)
    timeLbl.grid(column=0, row=3)

    window.config(menu=fileMenu)
    passBox.focus()
    diff.set(1)
    window.update()

    window.mainloop()
