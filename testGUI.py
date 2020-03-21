from tkinter import *
from tkinter.ttk import *
from password import Password
from tkinter import messagebox

window = Tk()

window.title("MTH312 Project")
window.geometry('350x250')

diff = IntVar()
window.passDispFlag = True
window.passLimit = 16


def testVal(P):
    if not (P.isalpha() and P.islower()):
        return False
    if len(passBox.get()) == window.passLimit:
        return False
    return True


def passwordUpdate(message):
    if message == "GAME OVER":
        enterBtn.configure(state="enabled")
        passBox.configure(state="enabled")
        window.passDispFlag = False
        messagebox.showinfo("YOU WIN!", "The test took too long and timed out,\n "
                                        "congratulations! Your Password is secure")
        knownLbl.configure(text="")
    elif window.passDispFlag:
        knownLbl.configure(text=message)
    window.update()


def checkStrength():
    Password(passBox.get(), passwordUpdate)
    enterBtn.configure(state="disabled")
    passBox.configure(state="disabled")
    window.passDispFlag = True



def about():
    messagebox.showinfo('MTH312 Project', "A MTH312 project by:\nJohn Bonazzi and Benjamin Brown")


easyRad = Radiobutton(window, text='Easy', value=1, variable=diff)
medRad = Radiobutton(window, text='Medium', value=2, variable=diff)
hardRad = Radiobutton(window, text='Hard', value=3, variable=diff)
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
easyRad.grid(column=0, row=4)
medRad.grid(column=1, row=4)
hardRad.grid(column=2, row=4)

window.config(menu=fileMenu)
passBox.focus()
diff.set(1)
window.update()


window.mainloop()
