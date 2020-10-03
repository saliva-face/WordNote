#!usr/bin/env python3
## WordNote App                                                             ##
## Author: Joshua Andrews                                                   ##
## Distributed under GPL                                                    ##
## If re-distributing, please do so under GPL, retaining original author    ##
## and version history documentation, as well as this request to do so.     ##

## VERSION HISTORY                                                          ##
## 18/12/15 -:- Version 0.5.1 Finished -:- Version incremented in line with ##
## WordNote, implemented 'lock' and 'unlock' methods and interface.         ##
## 07/12/15 -:- Version 0.1.0 Finished -:- no known bugs and all features   ##
## working as intended.                                                     ##


# Currently in many places here and in JT Users\Josh\Documents\ is 
# being used instead of current directory for logging.  Fix it.
# This one also requires a major read-through and some 
# consistency/style checking - look at this, here and below.  
# Disgraceful.  Add a 'kill all'/'reset' button, could replace current 
# main menu buttons with 'previous' buttons and have sub-menus in this,
# by category.  Might need to change the root windows of the other 
# files to toplevel widgets so that forgotten passwords can be handled 
# by a button that will open a pop-out window that will return True if 
# a secret question is answered correctly, False if not.  True will 
# route to a password reset window, False will return you to the 
# original login screen and will record a failed password reset for 
# that user's attention on next successful login.  Alternatively could 
# do an e-mail based reset, system will need to count used attempts in 
# self.remaining_password_attempts, and reset this on successful login.
# Create Exceptions - having read-through and corrected as far as this.
# Line continuations need to be cleaned up throughout still - see PEP 8
# Tidy up opening section after a thorough read of docstring and 
# version history sections of PEP 8.
# Maybe allow an _enternal_unlock() method in WordNote in case that 
# window gets closed?


import sys
import os

try:
    import tkinter as tk
    from tkinter import messagebox as tkmb
    from tkinter import font as tkf
except ImportError:
    import Tkinter as tk, tkMessagebox as tkmb, tkFont as tkf

import primenumberfinder as pnf
#import stopwatch as sw
import calculator as calc
import wordnote as wn
import hashlib
import jtlcd
import configsettings
import pwg

LOCKED = False


class IncorrectUsernameException(Exception):
    """Exception raised when username is incorrect."""
    def __init__(self, jtInstance):
        tkmb.showinfo("Login failed", 
                      "The username or password has not been recognised")
        jtInstance.root.destroy()
        jtInstance = JTLauncher()
        return None



def _hashcheck(text, hashtype, jtInstance=None, username=""):
    # Performs various types of hash-based confirmations.
    if hashtype == 1:
        try:
            return pwg.pwc(text, jtlcd.lcd[username][1])
        except KeyError as e:
            raise IncorrectUsernameException(jtInstance)
            return None
    elif hashtype == 2:
        return pwg.pwg(text)
    elif hashtype == 3:
        text = str(text).encode("utf-8")
        result = hashlib.md5(text)
        return result.hexdigest()


class JTLauncher():
    """Creates an instance of the login prompt for the App.  Logins 
    allow for personalisation and customisation.
    """

    def __init__(self):
     # Separate from UI building to prevent TclErrors stopping the 
     # geometry manager from .pack()-ing the widgets
        self.users = jtlcd.lcd
        self.initUI()

    def __repr__(self):
        """Creates an instance of login prompt for Joshython.
        
        No required arguments, called using 'joshython.Joshython()'
        """
        return self.__repr__.__doc__

    def __str__(self):
        """Creates an instance of login prompt for Joshython.
        
        No required arguments, called using 'joshython.Joshython()'
        """
        return self.__str__.__doc__
        
    def initUI(self):
     # Builds the launcher UI
        # Main window and config
        self.root = tk.Tk()
        self.root.title("Joshython")
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 150)
        self.y_pos = str(int(self.screen_y / 2) - 70)
        self.window_size = "+".join(["300x140", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        self.root.bind("<Return>", self.sign_in)

        # Create and configure widgets
        self.message_label = tk.Label(self.root, 
                                      text="Enter your name:")
        self.username_entry = tk.Entry(self.root, 
                                       width=15, 
                                       justify="center")
        self.username_entry.focus_set()
        self.password_entry = tk.Entry(self.root, 
                                       width = 15, 
                                       show="*", 
                                       justify="center", 
                                       exportselection="False")
        self.sign_in_button = tk.Button(self.root, 
                                        text="Sign in", 
                                        command=self.sign_in)
        self.new_user_button = tk.Button(self.root, 
                                         text="New User", 
                                         command=self.create_new_user)
        self.exit = tk.Button(self.root, text="Exit", command=sys.exit)
        self.password_entry.bind("<Control-KeyPress-c>", self.password_copy)

        # Pack widgets and start event loop
        self.message_label.pack()
        self.username_entry.pack()
        self.password_entry.pack()
        self.sign_in_button.pack()
        self.new_user_button.pack()
        self.exit.pack()
        self.root.mainloop()

    def sign_in(self, event=None):
     # Attempts to sign in with entered details - on successful login 
     # creates the menu and passes the entered name to it.
     # All logins (and attempts) are logged to master log file here.
        username = str(self.username_entry.get())
        self.username = username
        self.hashresult = _hashcheck(self.password_entry.get(), 
                                     1, 
                                     self, 
                                     username)
        self.password = self.password_entry.get()
        accepted = True
        if username == "":
            self.error(1)
        elif username.isnumeric():
            self.error(2)
        elif username.isalpha() == False:
            for char in username:
                if char.isalpha() or char in [" ", "\t", "\n"]:
                    continue
                else:
                    accepted = False
                    break
            if accepted:
                if self.password_check(self.hashresult):
                    self.root.destroy()
                    App = Joshython(username)
                else:
                    self.error(4)
            else:
                self.error(3)
        else:
            if self.password_check(self.hashresult):
                self.root.destroy()
                App = Joshython(username)
            else:
                self.error(4)

    def error(self, error):
     # Provides error handling for name entry.
     # These are user errors, not code-based nor system errors, they need 
     # moved to an Exception heirarchy at some point.
        if error == 1:
            tkmb.showinfo("Error", "Please enter a name", icon="warning")
            self.reset()
        elif error == 2:
            tkmb.showinfo("Error", 
                          "That was a number.  Numbers are not names", 
                          icon="warning")
            self.reset()
        elif error == 3:
            tkmb.showinfo("Error", 
                          "I doubt that your name contains characters other "
                          "than letters.  Try again, this time entering your "
                          "name.", 
                          icon="warning")
            self.reset()
        elif error == 4:
            tkmb.showinfo("Authentication Failure", 
                          "An incorrect username or password was entered.  "
                          "Please check your credentials and try again.  "
                          "Alternatively, you can contact your local IT "
                          "support, register as a new user, reset your "
                          "password, or contact the person who's details you "
                          "were tying to use and ask them nicely what their "
                          "username and password are.")
            print(os.path.dirname(os.path.realpath(__file__)))    
            with open(r"C:\Users\Josh\Documents\loglogginglogins.txt", 
                      "a+") as file:
                file.write(self.username + " : ")
                file.write(self.password + " : ")
                file.write(str(self.hashresult[0]) + "\n")
            self.reset()

    def reset(self):
        self.password_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.username_entry.focus_set()
        return None
        
    def hashcheck(self, text):
        text = str(text).encode("utf-8")
        result = hashlib.sha256(text)
        for i in range(200000):
            result = hashlib.sha256(result.hexdigest().encode("utf-8"))
        self.hashresult = result.hexdigest()
        return result.hexdigest()


    def password_check(self, password):
        try:
            username = self.username_entry.get()
            if password == self.users[username][0]:
                with open(r"C:\Users\user\Documents\bin\loglogginglogins.txt",
                          "a+") as file:
                    file.write("correct details, successful login for user: "
                               + username + "\n")
                return True
            else:
                with open(r"C:\Users\user\Documents\bin\loglogginglogins.txt",
                          "a+") as file:
                    file.write("incorrect password for user: " + username 
                               + "\n")
                return False
        except KeyError:
            with open(r"C:\Users\Josh\Documents\loglogginglogins.txt", \
            "a+") as file:
                file.write("incorrect username: ")
                for key in self.users:
                    file.write(key + ", ")
            return False

    def password_copy(self, event=None):
        self.password_entry.delete(0, "end")
        self.root.clipboard_clear()
        tkmb.showinfo("Password?", 
                      "Go ahead, paste that somewhere.", 
                      icon="question")
        self.root.clipboard_append("Strange... this isn't a password.")
        return 'break'
    
    def create_new_user(self):
        self.root.destroy()
        new_user = UserCreator()

class UserCreator():

    def __init__(self):
        self.users = jtlcd.lcd
        self.initUI()
        
    def initUI(self):
        self.root = tk.Tk()
        self.root.title("Joshython User Creator")
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 150)
        self.y_pos = str(int(self.screen_y / 2) - 62)
        self.window_size = "+".join(["300x125", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        
        self.username_entry = tk.Entry(self.root, 
                                       text="Enter your desired username", 
                                       justify="center")
        self.password_entry = tk.Entry(self.root, 
                                       width=15, 
                                       show="*", \
                                       exportselection="False", 
                                       justify="center")
        self.password_confirmation = tk.Entry(self.root, 
                                              width=15, 
                                              show="*", 
                                              exportselection="False", 
                                              justify="center")
        self.username_label = tk.Label(self.root, text="Enter your desired "
                                       "username: ")
        self.password_label = tk.Label(self.root, text="Enter your new "
                                       "password: ")
        self.password_confirmation_label = tk.Label(self.root, 
                                                    text="Re-enter your new "
                                                    "password: ")
        self.create_button = tk.Button(self.root, text="Create Profile", 
                                       command=self.create_user)
        self.cancel_button = tk.Button(self.root, text="Cancel", 
                                       command=self.cancel)
        self.spacer_label = tk.Label(self.root, text="")
        
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        self.password_confirmation_label.grid(row=2, column=0)
        self.password_confirmation.grid(row=2, column=1)
        self.spacer_label.grid(row=3, columnspan=2)
        self.create_button.grid(row=4, column=0)
        self.cancel_button.grid(row=4, column=1)
        
        self.username_entry.focus_set()
        self.root.bind("<Return>", self.create_user)
        self.root.mainloop()
        
 # Need to add checking for numbers in username - borrow from the login 
 # screen, it currently allows setting up a username with numbers but will 
 # reject it at login every time.
    def create_user(self, event=None):
        self.username = self.username_entry.get()
        if self.username == "":
            self.password_entry.delete(0, "end")
            self.password_confirmation.delete(0, "end")
            return self.error(1)
        elif self.username.isnumeric():
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.password_confirmation.delete(0, "end")
            return self.error(2)
        elif self.username.isalpha() == False:
            for char in self.username:
                if char.isalpha() or char in (" ", "\n", "\t"):
                    continue
                else:
                    self.username_entry.delete(0, "end")
                    self.password_entry.delete(0, "end")
                    self.password_confirmation.delete(0, "end")
                    return self.error(3)
                    break
            if _hashcheck(self.password_entry.get(), 
                          3) == _hashcheck(self.password_confirmation.get(), 
                                           3):
                self.password = self.password_entry.get()
                if self.password == "":
                    self.error(4)
                else:
                    if self.username not in self.users:
                        self.users[self.username] = _hashcheck(self.password, 
                                                               2)
                        with open("jtlcd.py", "w+") as file:
                            file.write("lcd = " + str(self.users))
                            tkmb.showinfo("Success", "User created, you will "
                                          "now be re-directed to the login "
                                          "screen.")
                        self.root.destroy()
                        app = JTLauncher()
                    else:
                        self.username_entry.delete(0, "end")
                        self.password_entry.delete(0, "end")
                        self.password_confirmation.delete(0, "end")
                        return self.error(5)
            else:
                self.password_entry.delete(0, "end")
                self.password_confirmation.delete(0, "end")
                return self.error(6)
        else:
            if _hashcheck(self.password_entry.get(), 
                          3) == _hashcheck(self.password_confirmation.get(), 
                                           3):
                self.password = self.password_entry.get()
                if self.password == "":
                    self.error(4)
                else:
                    if self.username not in self.users:
                        self.users[self.username] = _hashcheck(self.password, 
                                                               2)
                        with open("jtlcd.py", "w+") as file:
                            file.write("lcd = " + str(self.users))
                            tkmb.showinfo("Success", "User created, you will "
                                          "now be re-directed to the login "
                                          "screen.")
                        self.root.destroy()
                        app = JTLauncher()
                    else:
                        self.username_entry.delete(0, "end")
                        self.password_entry.delete(0, "end")
                        self.password_confirmation.delete(0, "end")
                        return self.error(5)
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.password_confirmation.delete(0, "end")
            return self.error(7)


    def cancel(self):
        self.root.destroy()
        app = JTLauncher()


    def error(self, errorcode):
        if errorcode == 1:
            return tkmb.showinfo("No Username Entered", "You must enter a "
                                 "username.  To otherwise would defeat the "
                                 "purpose.")
        elif errorcode == 2:
            return tkmb.showinfo("Error", "Usernames cannot contain numbers, "
                                 "because names cannot contain numbers.  "
                                 "Please enter a different username - one "
                                 "that could also be a name.")
        elif errorcode == 3:
            return tkmb.showinfo("Error", "At least one of the characters in "
                                 "that username cannot be used.  Please try "
                                 "again with a different username, containing"
                                 " no letters or special characters.")
        elif errorcode == 4:
            return tkmb.showinfo("No Passwords Entered", "It would be a bit "
                                 "silly if you could login without a "
                                 "password, really, wouldn't it?")
        elif errorcode == 5:
            return tkmb.showinfo("Username Already Exists", "Sorry, that "
                                 "username already exists in the user "
                                 "database.  Please choose another.  "
                                 "Alternatively, don't.")
        elif errorcode == 6:
            return tkmb.showinfo("Password Mismatch", "Those passwords "
                                 "weren't the same.  Please try again, "
                                 "entering two identical passwords. Just to "
                                 "be clear, that's one in each box.")
        elif errorcode == 7:
            return tkmb.showinfo("Error", "Unknown error.  Please try again."
                                 "  If the problem persists, please contact a"
                                 " system administrator with the exact "
                                 "username and password you were trying to "
                                 "input, and this code:\n1000507")



class PWC():

    def __init__(self, username):
        self.username = username
        self.users = jtlcd.lcd
        self.initUI()
    
    def initUI(self):
        self.root = tk.Tk()
        self.root.title("Joshython Password Change")
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 150)
        self.y_pos = str(int(self.screen_y / 2) - 62)
        self.window_size = "+".join(["300x125", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        
        self.old_password_entry = tk.Entry(self.root, 
                                           width=15, 
                                           show="*", 
                                           exportselection="False", 
                                           justify="center")
        self.new_password_entry = tk.Entry(self.root, 
                                           width=15, 
                                           show="*", 
                                           exportselection="False", 
                                           justify="center")
        self.new_password_confirm = tk.Entry(self.root, 
                                             width=15, 
                                             show="*", 
                                             exportselection="False", 
                                             justify="center")
        self.old_password_label = tk.Label(self.root, text="Old Password: ")
        self.new_password_label = tk.Label(self.root, text="New Password: ")
        self.new_password_confirm_label = tk.Label(self.root, 
                                                   text="Confirm New Password")
        self.password_change = tk.Button(self.root, 
                                         text="Change", 
                                         command=self.change)
        self.cancel_button = tk.Button(self.root, 
                                       text="Cancel", 
                                       command=self.cancel)
        self.spacer_label = tk.Label(self.root, text="")
        
        self.old_password_label.grid(column=0, row=0)
        self.old_password_entry.grid(column=1, row=0)
        self.new_password_label.grid(column=0, row=1)
        self.new_password_entry.grid(column=1, row=1)
        self.new_password_confirm_label.grid(column=0, row=2)
        self.new_password_confirm.grid(column=1, row=2)
        self.spacer_label.grid(columnspan=2, row=3)
        self.password_change.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def hashcheck(self, text, hashtype):
        if hashtype == 1:
            return pwg.pwg(text)
        elif hashtype == 2:
            text = str(text).encode("utf-8")
            result = hashlib.md5(text)
            return result.hexdigest()

    def change(self):
        current_hash = self.users[self.username][0]
        current_password = self.old_password_entry.get()
        if _hashcheck(current_password, 1, self.username) == current_hash:
            new_password = self.new_password_entry.get()
            new_password_confirmation = self.new_password_confirm.get()
            if _hashcheck(new_password, 3) == _hashcheck\
            (new_password_confirmation, 3):
                self.users[self.username] = _hashcheck(new_password, 2)
                with open("jtlcd.py", "w") as file:
                    file.write("lcd = " + str(self.users))
                tkmb.showinfo("Success", "Password successfully changed.  "
                              "You will now be redirected to the login "
                              "screen.", icon="warning")
                with open("loglogginglogins.txt", "a+") as file:
                    file.write("Password changed for user: " + self.username 
                               + "\n")
                self.root.destroy()
                App = JTLauncher()
            else:
                tkmb.showinfo("Error", "New passwords did not match.  Please"
                              " re-enter them.", icon="warning")
                self.old_password_entry.delete(0, "end")
                self.new_password_entry.delete(0, "end")
                self.new_password_confirm.delete(0, "end")
        else:
            tkmb.showinfo("Error", "Incorrect current password entered.  "
                          "Please check and try again.", icon="warning")
            self.old_password_entry.delete(0, "end")
            self.new_password_entry.delete(0, "end")
            self.new_password_confirm.delete(0, "end")
        
    def cancel(self):
        if tkmb.askokcancel("Warning", "Password wlll not be changed if you "
                            "continue.", icon="warning"):
            self.root.destroy()
            App = Joshython(self.username)
        else:
            return None
        

class Joshython():
    
    def __init__(self, username):
     # Separate from UI building to prevent TclErrors stopping the geometry 
     # manager from .pack()-ing the widgets
        self.username = username
        self.initUI(self.username)

    def __repr__(self):
        """Creates a menu from which to load the included apps.
        
        No required arguments, called using 'joshython.Joshython()'
        """
        return self.__repr__.__doc__

    def __str__(self):
        """Creates a menu from which to load the included apps.
        
        No required arguments, called using 'joshython.Joshython()'
        """
        return self.__str__.__doc__  
  
    def initUI(self, username):
     # Builds the UI, including personalisation
        username_text = "Welcome, " + username + ", to your dashboard."
        self.root = tk.Tk()
        self.root.title("Joshython")
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 150)
        self.y_pos = str(int(self.screen_y / 2) - 98)
        self.window_size = "+".join(["300x196", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        self._config = configsettings.config
        if self.username not in self._config:
            self._config[self.username] = self._config['default']
            with open("configsettings.py", "w+") as file:
                 file.write("import os\n\nconfig  =  " + str(self._config))
            tkmb.showinfo("User Profile Created", "User profile created with"
                          + " default options.")
        self.root.iconbitmap(self._config[self.username]['images']['icon'])
        
        self.locked_frame = tk.Frame(self.root)
        self.unlocked_frame = tk.Frame(self.root)
        def _unlock_helper(event=None):
            wn._external_unlock(self, self.WN_instance)
        self.lock_message = tk.Label(self.root, 
                                     text="This program has been locked by "
                                     "WordNote.  Please enter your password "
                                     "below to unlock: ",
                                     wraplength="200")
        self.unlock_password_entry = tk.Entry(self.root, 
                                              width=15, 
                                              show="*",
                                              exportselection="False", 
                                              justify="center")
        self.unlock_button = tk.Button(self.root,
                                       text="Unlock",
                                       command=_unlock_helper)
        self.username_label = tk.Label(self.root, text=username_text)
        self.pnf_button = tk.Button(self.root, 
                                    text="Prime Number Finder", 
                                    command=self.launchpnf)
     #  self.sw_button = tk.Button(self.root, text="Stopwatch", 
     #                             command=self.launchsw)
        self.calc_button = tk.Button(self.root, 
                                     text="Calculator", 
                                     command=self.launchcalc)
        self.wordnote_button = tk.Button(self.root, 
                                         text="Wordnote", 
                                         command=self.launchwordnote)
        self.change_password_button = tk.Button(self.root, 
                                                text="Change Password", 
                                                command=self.change_password)
        self.sign_out_button = tk.Button(self.root, 
                                         text="Log out", 
                                         command=self.sign_out)
        self.exit_button = tk.Button(self.root, 
                                     text="Exit", 
                                     command=sys.exit)
        
        self.lock_message.pack(in_=self.locked_frame, pady="30")
        self.unlock_password_entry.pack(in_=self.locked_frame)
        self.unlock_button.pack(in_=self.locked_frame)
        self.unlocked_frame.pack(fill="both", expand="1")
        self.username_label.pack(in_=self.unlocked_frame)
        self.pnf_button.pack(in_=self.unlocked_frame)
     #  stopwatch app - DEPRECATED
     #  self.sw_button.pack(in_=self.unlocked_frame)
        self.calc_button.pack(in_=self.unlocked_frame)
        self.wordnote_button.pack(in_=self.unlocked_frame)
        self.change_password_button.pack(in_=self.unlocked_frame)
        self.sign_out_button.pack(in_=self.unlocked_frame)
        self.exit_button.pack(in_=self.unlocked_frame)
        
        self.unlock_password_entry.bind("<KeyPress-Return>", _unlock_helper)

        self.root.mainloop()

    def change_password(self):
        self.root.destroy()
        App = PWC(self.username)
        return None

    def launchpnf(self):
     # Launches the Prime Number Finder app
        app = pnf.PNF()
        return None

     #  stopwatch app - DEPRECATED
  # def launchsw(self):
     # Launches the Stopwatch app
     #  app = sw.SW()
     #  return None

    def launchcalc(self):
     # Launches the calculator app
        app = calc.Calc()
        return None
    
    def launchwordnote(self):
     # Launches the text editor app
        self.root.iconify()
        app = wn.WN(username = self.username, master = self)
        return None

    def lock(self, WN_instance):
        self.WN_instance = WN_instance
        self.unlocked_frame.pack_forget()
        self.locked_frame.pack(fill="both", expand="1")
        return None

    def unlock(self):
        self.locked_frame.pack_forget()
        self.unlocked_frame.pack(fill="both", expand="1")
        return None
    
    def sign_out(self):
        self.root.destroy()
        App = JTLauncher
        try:
            App.username_entry.focus_set()
        except:
            pass
        finally:
            App()
        
if __name__ == "__main__":
 # Automatically generates an instance of the launcher class object
    import __init__ as init
    App = JTLauncher()