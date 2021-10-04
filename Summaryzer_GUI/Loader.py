import time
from tkinter import *

root = Tk()
root.withdraw()
Label(root,text="I am main window").pack()

class SplashScreen:
    def __init__(self):
        self.a = Toplevel()
        self.percentage = 0
        Label(self.a,text="I am loading screen").pack()
        self.load = Label(self.a,text=f"Loading...{self.percentage}%")
        self.load.pack()
        self.load_bar()

    def load_bar(self):
        self.percentage +=5
        self.load.config(text=f"Loading...{self.percentage}%")
        if self.percentage == 100:
            self.a.destroy()
            root.deiconify()
            return
        else:
            root.after(100,self.load_bar)

SplashScreen()
#root.deiconify()
root.mainloop()