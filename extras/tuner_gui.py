from tkinter import *

class Window(Frame):
    def __init__(self, master):
        frame = Frame(master)
        self.master = master
        self.master.title("Guitar Tuner")

        # Add button
        self.button_left = Button(master, text="Click Me", command=self.greet)
        self.button_left.pack(side="left")
        # Add label
        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        # Add greet button
        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        # Add close button
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        # Add menu
        self.dropdown_menu = Menu(master)#, text="Tunings")
        #self.dropdown_menu.pack()


    def greet(self):
        print("Greetings!")
    '''
    def init_window(self) :
        

        self.pack(fill=BOTH, expand=1)

        # Add menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # Create Tunings object
        tunings = Menu(menu)
    '''

 


root = Tk()
root.geometry("400x300")
my_gui = Window(root)
root.mainloop()