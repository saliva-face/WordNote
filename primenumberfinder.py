#!usr/bin/env python
#prime number finding app
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import joshython as jt
from tkinter import messagebox as tkmb
import sys

class PNF():
#Main Class for the App, including error handling.    
    def __init__(self):
        self.e_text = ""
        self.pos_result = " is prime."
        self.neg_result = " is not prime."
        self.r_s_text = ""
        self.r_e_text = ""
        self.f_list = []
        self.r_list = []
        self.initUI()

    def __repr__(self):
        """Creates a prime number finding app.
        
No required arguments, called using 'primenumberfinder.PNF()'
        """
        return self.__repr__.__doc__

    def __str__(self):
        """Creates a prime number finding app.
        
No required arguments, called using 'primenumberfinder.PNF()'
        """
        return self.__str__.__doc__ 
    
    def initUI(self):
#Defines and initialises the UI
        self.root = tk.Tk()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.window_size = "265x281+" + (str(int(self.screen_x / 2) - 132)) \
+ "+" + (str(int(self.screen_y / 2) - 140))
        self.root.title("Prime Number Finder")
        self.root.geometry(self.window_size)
        self.root.focus_set()

        self.single_entry_label = tk.Label(self.root, text="Enter a number:")
        self.single_entry = tk.Entry(self.root, width=5, \
textvariable=self.e_text)
        self.single_entry_button = tk.Button(self.root, text="Check", \
command=self.prime_number_finder)
        self.range_label = tk.Label(self.root, text="Or enter a range:")
        self.range_start = tk.Entry(self.root, width=5, \
textvariable=self.r_s_text)
        self.range_label_2 = tk.Label(self.root, text="to")
        self.range_end = tk.Entry(self.root, width=5, \
textvariable=self.r_e_text)
        self.range_button = tk.Button(self.root, text="Calculate", \
command=self.prime_number_range)
        self.exit_button = tk.Button(self.root, text="Exit", \
command=sys.exit)
        self.spacer_1 = tk.Label(self.root, height=1)
        self.spacer_2 = tk.Label(self.root, height=2)
        self.main_menu_button = tk.Button(self.root, text="Main Menu", \
command=self.mainmenu)

        self.single_entry_label.pack()
        self.single_entry.pack()
        self.single_entry_button.pack()
        self.spacer_1.pack()
        self.range_label.pack()
        self.range_start.pack()
        self.range_label_2.pack()
        self.range_end.pack()
        self.range_button.pack()
        self.spacer_2.pack()
        self.main_menu_button.pack()
        self.exit_button.pack()

        self.root.mainloop()

    def prime_number_finder(self):
#Checks a single number for prime-ness, attached to the 'Enter' button
        try:
            num = int(self.single_entry.get())
            n = int((int(self.single_entry.get())) / 2) + 1
            for x in range(2, n):
                if num % x == 0:
                    self.e_text = str(num)
                    self.result(self.e_text, self.neg_result)
                    self.clear()
                    print(x)
                    break
                else:
                    continue
            self.e_text = str(num)
            self.result(self.e_text, self.pos_result)
        except ValueError:
            self.error(0)
        except TypeError:
            self.error(1)

    def prime_number_range(self):
#Checks a range of numbers for primes, attached to the 'Calculate' button
        try:
            num_1 = int(self.range_start.get())
            num_2 = int(self.range_end.get())
            for a in range(num_1, num_2 + 1):
                x = int((a / 2) + 1)
                for b in range(2, x):
                    if a % b == 0:
                        self.f_list.append(a)
                        break
                if a not in self.f_list:    
                    self.r_list.append(a)
                    continue
            self.range_result(str(num_1), str(num_2), self.r_list)
        except ValueError:
            self.error(0)
        except TypeError:
            self.error(1)
            
    def result(self, result, result_text):
#Presents the results of a single number check in a pop-up info box
        tkmb.showinfo("Result", result + result_text)
        self.clear()
        pass
    
    def range_result (self, start, end, results):
#Presents the results of a range check in a pop-up info box
        result = "\n"
        for x in results:
            result += str(x) + ", "
        result = result[:len(result)-2:]
        result += "."
        tkmb.showinfo("Result", "The prime numbers between %s and %s are" \
% (start, end) + result)
        self.clear()
        self.r_list = []
        return None

    def clear(self):
#Resets the App back to the default, clearing all entries and variables
        self.root.destroy()
        App = PNF()
        pass

    def mainmenu(self):
        self.root.destroy()
    
    def error(self, error_type):
#Provides basic error handling in a user-friendly pop-up info box
        if error_type == 0:
            tkmb.showinfo("Error", "Please enter a number BEFORE pressing \
check or calculate - to otherwise would defeat the purpose.", icon="warning")
            self.clear()
        elif error_type == 1:
            tkmb.showinfo("Error", "Please enter numbers only.  I'm not even \
sure what a prime letter would look like.")
            self.clear()

    def exit(self):
        self.root.destroy()
        try:
            platform.root.destroy()
        except:
            pass

#If the App is opened directly, rather than from the platform, it will  
#initialise the platform, with an option to launch the App from it
if __name__ == "__main__":
    platform = jt.jtLauncher()