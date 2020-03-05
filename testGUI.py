from tkinter import *
from tkinter.ttk import *
from password import Password
from tkinter import messagebox

window = Tk()

window.title("MTH312 Project")
window.geometry('350x250')

diff = IntVar()

def passwordUpdate(message):
  #window.after(1000,password.give_hint())
  #display = password.get_password()
  knownLbl.configure(text=message)
  window.update()

def checkStrength():
    password = Password(passBox.get(),passwordUpdate)
    #passBox.configure(state='disabled')
    #passBox.configure(state='enabled')


def about():
    messagebox.showinfo('MTH312 Project',"A MTH312 project by:\nJohn Bonazzi and Benjamin Brown")

easyRad = Radiobutton(window, text='Easy', value=1, variable=diff)
medRad = Radiobutton(window, text='Medium', value=2, variable=diff)
hardRad = Radiobutton(window, text='Hard', value=3, variable=diff)
passLbl = Label(window, text="Enter \"Password\":")
passBox = Entry(window,width=20)
knownLbl = Label(window, text="")
enterBtn = Button(window, text="Check Strength", command=checkStrength)
timeLbl = Label(window, text="")
fileMenu = Menu(window)
fileItems = Menu(fileMenu)

fileItems.add_command(label='Exit',command=window.destroy)
fileItems.add_command(label='About',command=about)

fileMenu.add_cascade(label='File',menu=fileItems)
passLbl.grid(column=0,row=0)
passBox.grid(column=0,row=1)
enterBtn.grid(column=1,row=1)
knownLbl.grid(column=0,row=2)
timeLbl.grid(column=0,row=3)
easyRad.grid(column=0,row=4)
medRad.grid(column=1,row=4)
hardRad.grid(column=2,row=4)

window.config(menu=fileMenu)
passBox.focus()
diff.set(1)
window.update()

window.mainloop()