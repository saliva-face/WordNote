#!usr/bin/env python
#calculator app

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import joshython as jt
from tkinter import messagebox as tkmb
import sys

class Calc():
#Main Class for the App, including error handling.
    def __init__(self):    
        self.number_buttons = []
        self.bttn_row = 1
        self.bttn_col = 2
        self.screen_text = "0"
        self.sum_string = []        
        self.initUI()
       

    def __repr__(self):
        """Creates a calculator app.
        
No required arguments, called using 'calc.Calc()'
        """
        return self.__repr__.__doc__

    def __str__(self):
        """Creates a calculator app.
        
No required arguments, called using 'calc.Calc()'
        """
        return self.__str__.__doc__ 

    def initUI(self):
     # Defines and initialises the UI
        self.root = tk.Tk()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.window_size = "265x281+" + (str(int(self.screen_x / 2) - 132)) \
        + "+" + (str(int(self.screen_y / 2) - 140))
        self.root.title("Calculator")
        self.root.geometry(self.window_size)
        self.root.focus_set()

        self.screen = tk.Entry(self.root)
        self.screen.insert("insert", "0")
        self.screen.config(state="disabled")
        for i in range(9, -1, -1):
            i = tk.Button(self.root, text=i, command=lambda x=i:self.enter(x))
            self.number_buttons.append(i)
        self.main_menu_button = tk.Button(self.root, text="Main Menu", \
        command=self.mainmenu)
        self.exit_button = tk.Button(self.root, text="Exit", \
        command=sys.exit)
        self.plus_button = tk.Button(self.root, text="+", \
        command=lambda:self.current_sum("+"))        
        self.subtract_button = tk.Button(self.root, text="-", \
        command=lambda:self.current_sum("-"))        
        self.multiply_button = tk.Button(self.root, text="*", \
        command=lambda:self.current_sum("*"))        
        self.divide_button = tk.Button(self.root, text="/", \
        command=lambda:self.current_sum("/"))

        self.root.bind("1", self.keypress)
        self.root.bind("2", self.keypress)
        self.root.bind("3", self.keypress)
        self.root.bind("4", self.keypress)
        self.root.bind("5", self.keypress)
        self.root.bind("6", self.keypress)
        self.root.bind("7", self.keypress)
        self.root.bind("8", self.keypress)
        self.root.bind("9", self.keypress)
        self.root.bind("0", self.keypress)
        self.root.bind("<Return>", self.calculation)

        self.screen.grid(row=0, column=2, columnspan=3)
        for bttn in self.number_buttons:
            if self.number_buttons.index(bttn) == 9:
                bttn.grid(row=4, column=1)
            else:
                bttn.grid(row=self.bttn_row, column=self.bttn_col)
            if self.bttn_col > 0:
                self.bttn_col -= 1
            else:
                self.bttn_row += 1
                self.bttn_col = 2
        self.plus_button.grid(row=1, column=3)
        self.subtract_button.grid(row=2, column=3)
        self.multiply_button.grid(row=3, column=3)
        self.divide_button.grid(row=4, column=3)
        self.main_menu_button.grid(row=5, columnspan=3)
        self.exit_button.grid(row=6, columnspan=2)

        self.root.mainloop()

#  current sum function - builds a text string that is then input to enter for eval()
#  currently eval() is not working - SyntaxError: invalid token, apparently 
 
    def enter(self, n):
        old_value = self.screen_text
        self.screen.config(state="normal")
        self.screen.delete("0", "end")
        self.screen.insert("insert", str(n))
        self.screen.config(state="disabled")
        self.current_sum(old_value)
        self.update_screen(self.screen)
    
    def keypress(self, event=None):
        self.screen_text = event.char
        self.current_sum(event.char)
        self.update_screen(self.screen)
    
    def current_sum(self, *args):
        for arg in args:
            self.sum_string.append(str(arg))
        self.sum_string.append(str(self.screen_text))
        self.update_screen(self.screen)
    
    def calculation(self, event=None):
        for char in self.sum_string:
            try:
                int(char)
                continue
            except ValueError:
                if char == "+":
                    v = int(self.sum_string[self.sum_string.index(char) - 1])\
                    + int(self.sum_string[self.sum_string.index(char) + 1])
                    self.sum_string[self.sum_string.index(char) + 1] = 900
                if char == "-":
                    v = int(self.sum_string[self.sum_string.index(char) - 1])\
                    - int(self.sum_string[self.sum_string.index(char) + 1])
                    self.sum_string[self.sum_string.index(char) + 1] = v
                if char == "/":
                    v = int(self.sum_string[self.sum_string.index(char) - 1])\
                    / int(self.sum_string[self.sum_string.index(char) + 1])
                    self.sum_string[self.sum_string.index(char) + 1] = v
                if char == "*":
                    v = int(self.sum_string[self.sum_string.index(char) - 1])\
                    * int(self.sum_string[self.sum_string.index(char) + 1])
                    self.sum_string[self.sum_string.index(char) + 1] = v
                self.screen.config(state="normal")
                self.screen_text = self.sum_string[len(self.sum_string) - 1]
                self.screen.config(state="disabled")
                
    def algebra(self, event=None, *args):
        self.screen_text=eval(sum_string)
        
    def update_screen(self, widget):
        widget.update()

    def mainmenu(self):
        self.root.destroy()

    def exit(self):
        self.root.destroy()
        try:
            platform.root.destroy()
        except:
            pass

if __name__ == "__main__":
    platform = jt.jtLauncher()