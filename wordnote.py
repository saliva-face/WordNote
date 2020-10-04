#usr/bin/env python3.4

## WordNote App                                                             ##
## Author: Joshua Andrews                                                   ##
## Distributed under GPL                                                    ##






##############################################################################
##                             VERSION  HISTORY                             ##
##############################################################################
## 03/10/20 -:- Version 0.9.2 Finished -:- Adjusted tabbed mode menus, and  ##
## corrected bugs.  Updated placeholder methods.                            ##
## 17/09/17 -:- Version 0.9.1 Finished -:- Tabbed mode menus completed.     ##
## 23/08/17 -:- Version 0.9.0 Finished -:- Can now switch between tabbed    ##
## and windowed modes.  Some menu items still need re-assigned to support   ##
## this functionality.                                                      ##
## 12/01/16 -:- Version 0.8.0 Finished -:- New file format created, saving  ##
## tag and font information as a file header in XML.  Opening and saving    ##
## methods adjusted to allow file type detection for this new format.       ##
## 10/01/16 -:- Version 0.7.0 Finished -:- Major re-work of 'duplicate'     ##
## method, correcting bug relating to loss of text formatting.              ##
## 09/01/16 -:- Version 0.6.1 Finished -:- Style improvements, added a new  ##
## 'close others' method.                                                   ##
## 07/01/16 -:- Version 0.6.0 Finished -:- Text colour selection option     ##
## added (finally) - added to style banner for good measure.                ##
## 06/01/16 -:- Version 0.5.7 Finished -:- Style banner options re-worked,  ##
## simplifications and optimisations.  Inconsistent 'font_change' behaviour ##
## corrected.  Banner expansion and event recognition consistency improved. ##
## 05/01/16 -:- Version 0.5.6 Finished -:- Banners complete and working as  ##
## intended.  Improvements to menu display choices and banner display.      ##
## 02/01/16 -:- Version 0.5.5 Finished -:- Finished Exceptions, killed some ##
## banner bugs specific to view changes.                                    ##
## 24/12/15 -:- Version 0.5.4 Finished -:- Some Exceptions, more to do      ##
## prior to Version increment.                                              ##
## 23/12/15 -:- Version 0.5.3 Finished -:- Improvements to font changes.    ##
## 19/12/15 -:- Version 0.5.2 Finished -:- Improvements to banners.         ##
## 18/12/15 -:- Version 0.5.1 Finished -:- 'Lock' and 'unlock' methods      ##
## improved and simplified, other minor fixes and improvements.             ##
## 17/12/15 -:- Version 0.5.0 Finished -:- Added 'Entertainment' feature,   ##
## added iteration methods, updated internal functions.                     ##
## 16/12/15 -:- Version 0.4.1 Finished -:- Added another banner, improved   ##
## layout.                                                                  ##
## 16/12/15 -:- Version 0.4.0 Finished -:- Major re-work of banner, some    ##
## minor improvements elsewhere.                                            ##
## 15/12/15 -:- Version 0.3.1 Finished -:- Minor improvements, added three  ##
## new highlight colours, allowed multiple different colour highights, new  ##
## images added to resources.                                               ##
## 14/12/15 -:- Version 0.3.0 Finished -:- Text alignment options added,    ##
## major code improvements, eight new fonts added.                          ##
## 14/12/15 -:- Version 0.2.1 Finished -:- Cosmetic improvements and menu   ##
## customisations now working, minor code optimisations.                    ##
## 13/12/15 -:- Version 0.2.0 Finished -:- Font Style dialogue reworked,    ##
## previously undiscovered bug flattened, minor improvements made.          ##
## 12/12/15 -:- Version 0.1.2 Finished -:- 'undo'/'redo' methods added.     ##
## 05/12/15 -:- Version 0.1.1 Finished -:- additional menus completed and   ##
## some 'Find & Replace' bugs squashed.                                     ##
## 04/12/15 -:- Version 0.1.0 Finished -:- no known bugs and all features   ##
## working as intended.                                                     ##
##                            END VERSION HISTORY                           ##
##############################################################################






##############################################################################
##                                  TO DO:                                  ##
##############################################################################
## Consider providing options for paragraph layout for further styling.     ##
## Will need to attempt distinction between colour and black/white          ##
## printing if text colour choice is provided.  Might be as easy as         ##
## pre-processing the data sent to print and making it black/white, but     ##
## otherwise printing as normal.  i.e. printing it in full colour, the      ##
## colour being black.                                                      ##
## Update/revise/complete function documentation.                           ##
## While you're at it, read through the whole damn thing and ensure         ##
## there's nothing stupid in there, and do some more testing.               ##
## Investigate 'unlock' try/except, write Exception for it.                 ##
## Write an 'About' section, maybe a help menu.                             ##
##############################################################################








import hashlib
import sys
import os
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from tkinter import font as tkf
except ImportError:
    import tkFont as tkf
try:
    from tkinter import messagebox as tkmb
except ImportError:
    from Tkinter import messagebox as tkmb
try:
    from tkinter import filedialog
except ImportError:
    from Tkinter import filedialog
try:
    from tkinter import colorchooser as tkcc
except ImportError:
    import tkColorChooser as tkcc
from PIL import Image, ImageTk
import win32print
import winsound
import xml.etree.ElementTree as ET
import string
import joshython as jt
import jtlcd
import configsettings



global count 
count = 0
global _config
_config = configsettings.config
global _running
_running = False
global _window_set
_window_set = {}

class TextNotFoundError(Exception):
    """Exception raised by 'Find' and 'Replace' methods of 'WN' class"""
    def __init__(self):
        tkmb.showinfo("Search Failed", "Text not found in document")


class TextNotSelectedError(Exception):
    """Exception raised by with custom message"""
    def __init__(self, message):
        tkmb.showinfo("Error", message)


class InvalidInputError(Exception):
    """Exception raised when non-fatal ValueErrors occur."""
    def __init__(self, message):
        tkmb.showinfo("Error", message)


class LaunchFailureError(Exception):
    """Raised when instance fails to launch, prompts for re-try."""
    def __init__(self, WN_instance):
        try:
            username = WN_instance.username
            file_contents = WN_instance.file_contents
            master = WN_instance.master
            WN_instance.close()
        except AttributeError:
            tkmb.showinfo("Error", "Failed to start WordNote, and details "
                          "could not be recovered.")
            WN_instance.root.mainloop()
            WN_instance.close()
        else:
            if tkmb.askyesno("Error", "Failed to start WordNote, but details "
                             "were recovered.  Re-try launch?"):
                App = WN(username=username,
                         file_contents=file_contents,
                         master=master)
        finally:
            return None



class FontDialogue():
    def _establish_baselines(self):
        self.new_font = {"size" : 0,
                         "weight" : "",
                         "slant" : "",
                         "family" : "",
                         "overstrike" : 0,
                         "underline" : 0,
                         "strikethrough_change" : False,
                         "underline_change" : False}
        if self.WN_instance.text_entry.tag_ranges("sel"):
            self.sample_font = tkf.Font(size=10, family="Arial")
        else:
            self.sample_font = tkf.Font(size=self.WN_instance.custom_font[
                            'size'],
                        weight=self.WN_instance.custom_font['weight'],
                        slant=self.WN_instance.custom_font['slant'],
                        family=self.WN_instance.custom_font['family'],
                        overstrike=self.WN_instance.custom_font['overstrike'],
                        underline=self.WN_instance.custom_font['underline'])
        self.strikethrough = tk.IntVar()
        self.strikethrough.set(self.new_font["overstrike"])
        self.underline = tk.IntVar()
        self.underline.set(self.new_font["underline"])
        self.text_offset = tk.IntVar()
        self.text_offset.set(0)
        self.offset = None
        return self.new_font
        
 # 'Font Style Options' dialogue for App, providing customisation 
 # options for the font style used for selected ranges of text, or for 
 # the document as a whole.

    def __init__(self, WN_instance):
        self.WN_instance = WN_instance
        self._establish_baselines()
        self.initUI()
        
        
    def initUI(self):
        self.root = tk.Toplevel()        
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 226)
        self.y_pos = str(int(self.screen_y / 2) - 145)
        self.window_size = "+".join(["452x290", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        self.root.title("Wordnote - Font Style Options")
        self.root.focus_set()
        
        self.font_size_frame = tk.Frame(self.root, relief="sunken")
        self.font_style_frame = tk.Frame(self.root,
                                         width="60",
                                         relief="raised")
        self.font_effect_frame = tk.Frame(self.root,
                                          relief="raised",
                                          width="60")
        self.font_family_frame = tk.Frame(self.root, relief="sunken")
        self.sample_frame = tk.Frame(self.root, relief="sunken")
        self.button_frame = tk.Frame(self.root, relief="raised")
        self.sample_text_label = tk.Label(self.root,
                                          text="Sample Text!",
                                          font=self.sample_font)
        self.sample_text_label.lift(aboveThis=None)
        
        # Font size selection widgets
        self.vertscroll_size = tk.Scrollbar(self.root)
        self.font_size_list = tk.Listbox(self.root, 
                                         selectmode="MULTIPLE", 
                                         height="6", 
                                         bg="white", 
                                         yscrollcommand=\
                                             self.vertscroll_size.set, 
                                         exportselection=0)
        self.vertscroll_size.config(command=self.font_size_list.yview)
        for n in range(2, 73, 2):
            self.font_size_list.insert("end", str(n))
        self.font_size_entry = tk.Entry(self.root, text="", width="2")
        self.font_size_label = tk.Label(self.root, 
                                        text="Select a font size: ")

        # Font style and effect selection widgets
        self.font_style_list = tk.Listbox(self.root, 
                                          selectmode="MULTIPLE", 
                                          height="4", 
                                          bg="white", 
                                          exportselection=0)
        self.font_style_list.insert("end", "None")
        self.font_style_list.insert("end", "Bold")
        self.font_style_list.insert("end", "Italic")
        self.font_style_list.insert("end", "Bold Italic")
        self.strikethrough_cb = tk.Checkbutton(self.root,
                                               variable=self.strikethrough,
                                               text="Strikethrough",
                                               command=self.strikethrough_set)
        self.underline_cb = tk.Checkbutton(self.root,
                                           variable=self.underline,
                                           text="Underline",
                                           command=self.underline_set)
        self.superscript_rb = tk.Radiobutton(self.root,
                                             text="Superscript",
                                             value=20,
                                             variable=self.text_offset)
        self.regular_text_rb = tk.Radiobutton(self.root,
                                              text="Regular",
                                              value=1,
                                              variable=self.text_offset)
        self.subscript_rb = tk.Radiobutton(self.root,
                                           text="Subscript",
                                           value=-20,
                                           variable=self.text_offset)
                                          
        if self.strikethrough.get() == 1:
            self.strikethrough_cb.select()
        else:
            self.strikethrough_cb.deselect()
        if self.underline.get() == 1:
            self.underline_cb.select()
        else:
            self.underline_cb.deselect()

        # Font family selection widgets
        self.vertscroll_family = tk.Scrollbar(self.root)
        self.font_family_list = tk.Listbox(self.root, 
                                           selectmode="MULTIPLE",
                                           height="6",
                                           bg="white",
                                           yscrollcommand=\
                                               self.vertscroll_family.set,
                                           exportselection=0)
        self.vertscroll_family.config(command=self.font_family_list.yview)
        self.font_family_list.insert("end", "Arial")
        self.font_family_list.insert("end", "Comic Sans MS")
        self.font_family_list.insert("end", "Courier")
        self.font_family_list.insert("end", "Georgia")
        self.font_family_list.insert("end", "Helvetica")
        self.font_family_list.insert("end", "MS Sans Serif")
        self.font_family_list.insert("end", "MS Serif")
        self.font_family_list.insert("end", "Symbol")
        self.font_family_list.insert("end", "System")
        self.font_family_list.insert("end", "Times")
        self.font_family_list.insert("end", "Verdana")
        self.font_family_list.insert("end", "Wingdings")

        # Buttons
        self.ok_button = tk.Button(self.root, text="OK", width="6", \
        command=self.confirm)
        self.cancel_button = tk.Button(self.root, text="Cancel", \
        command=self.cancel)

        # Keybinds
        self.font_size_list.bind("<<ListboxSelect>>", self.font_size)
        self.font_style_list.bind("<<ListboxSelect>>", self.font_style)
        self.font_size_entry.bind("<KeyPress-Return>", self.font_size)
        self.font_family_list.bind("<<ListboxSelect>>", self.font_family)

        # Pack frames
        self.button_frame.pack(fill="x", side="bottom", expand="1")
        self.sample_frame.pack(fill="x", side="top", expand="1")
        self.font_size_frame.pack(fill="both", side="left", expand="1")
        self.font_family_frame.pack(fill="both", side="right", expand="1")
        self.font_style_frame.pack(anchor="n", side="top", expand="1")
        self.font_effect_frame.pack(side="left", expand="1")
        
        # Pack font size widgets
        self.vertscroll_size.pack(side="right", 
                                  fill="y", 
                                  in_=self.font_size_frame,
                                  expand="1")
        self.font_size_list.pack(fill="both",
                                 side="right",
                                 in_=self.font_size_frame,
                                 expand="1")
        self.font_size_label.pack(side="left", 
                                  anchor="n", 
                                  in_=self.button_frame)
        self.font_size_entry.pack(side="left", 
                                  anchor="n", 
                                  in_=self.button_frame)
        
        # Pack font style and effect widgets
        self.font_style_list.pack(anchor="n", 
                                  padx="15", 
                                  fill="x", 
                                  in_=self.font_style_frame)
        self.strikethrough_cb.pack(anchor="w",
                                   side="top",
                                   in_=self.font_effect_frame)
        self.underline_cb.pack(anchor="w",
                               side="top",
                               in_=self.font_effect_frame)
        self.superscript_rb.pack(anchor="w",
                                 side="top",
                                 in_=self.font_effect_frame)
        self.regular_text_rb.pack(anchor="w",
                                  side="top",
                                  in_=self.font_effect_frame)
        self.subscript_rb.pack(anchor="w",
                                 side="top",
                                 in_=self.font_effect_frame)
        
        
        # Pack font family widgets
        self.vertscroll_family.pack(side="right",
                                    fill="y",
                                    in_=self.font_family_frame,
                                    expand="1")
        self.font_family_list.pack(side="right",
                                   fill="both",
                                   in_=self.font_family_frame,
                                   expand="1")
        
        # Pack buttons
        self.cancel_button.pack(side="right", 
                                padx="30", 
                                in_=self.button_frame)
        self.ok_button.pack(side="right", 
                            pady="30", 
                            padx="30", 
                            in_=self.button_frame)
        self.root.bind("<FocusOut>", self.focus_lost)
        self.sample_text_label.pack(side="left", padx="20", in_=self.sample_frame)
        
        self.root.mainloop()
        
      
    def font_size(self, event=None):
        try:
         # Attempts to resolve selection to a suitable string.
            widget = event.widget
            selection = widget.curselection()
        except AttributeError:
         # AttributeError is raised if the current widget has no method
         # 'widget.curselection()' - i.e. it is the Entry widget.
            size = self.font_size_entry.get()
            self.font_size_list.selection_clear(0, "end")
            self.font_size_list.selection_set(int((int(size) / 2) - 1))
            self.font_size_list.selection_anchor(int((int(size) / 2) - 1))
            self.font_size_list.see("anchor")
        except ValueError:
         # ValueError is raised if the value in the Entry widget cannot
         # be resolved to an int, i.e. it is an empty string or it 
         # contains non-numeric characters.
            raise InvalidInputError("Please ensure you enter only numbers "
                                      "for the font size.")
        else:
         # Clears Entry widget to avoid clashes later between selected
         # and entered values - thus propagating only the most recent.
            size = str((int(selection[0]) + 1) * 2)
            self.font_size_entry.delete(0, "end")
            self.new_font["size"] = size
            self._update_sample("size")
        finally:
            return None
        
    
    def font_style(self, event):
        widget = event.widget
        selection = widget.curselection()
        style = str(widget.get(int(selection[0]))).lower()
        self.new_font["weight"] = "bold" if "bold" in style else "normal"
        self.new_font["slant"] = "italic" if "italic" in style else "roman"
        self._update_sample("weight", "slant")
        return None
        
        
    def font_family(self, event):
        widget = event.widget
        selection = widget.curselection()
        family = str(widget.get(int(selection[0]))).lower()
        self.new_font["family"] = family
        self._update_sample("family")
        return None


    def strikethrough_set(self, event=None):
        self.new_font["overstrike"] = self.strikethrough.get()
        self.new_font["strikethrough_change"] = True
        self._update_sample("overstrike")
        return None


    def underline_set(self, event=None):
        self.new_font["underline"] = self.underline.get()
        self.new_font["underline_change"] = True
        self._update_sample("underline")
        return None


    def focus_lost(self, event=None):
        self.root.focus_force()
        return None


    def _update_sample(self, *args):
        for arg in args:
            self.sample_font[arg]=self.new_font[arg]
        self.root.update()
        return None        


    def confirm(self):
        if self.font_size_entry.get() is not "":
            try:
                int(self.font_size_entry.get())
            except ValueError:
             # Raised for non-numeric values only.
                raise InvalidInputError("Please ensure you enter only "
                                          "numbers for the font size.")
            else:
                self.new_font["size"] = self.font_size_entry.get()
                self._update_sample() # forces offset to update
                if self.text_offset.get():
                    if self.text_offset.get() is 1:
                        self.text_offset.set(0)
                    self.offset = self.text_offset.get()
                self.WN_instance.font_change(self.new_font, self.offset)
                self.root.destroy()
            finally:
                return None
        else:
            self._update_sample() # forces offset to update
            if self.text_offset.get():
                if self.text_offset.get() is 1:
                    self.text_offset.set(0)
                self.offset = self.text_offset.get()
            self.WN_instance.font_change(self.new_font, self.offset)
            self.root.destroy()
            return None
    
    
    def cancel(self):
        self.root.destroy()
        return None
        
        
class LayoutDialogue():
 # 'Layout Options' dialogue for main App, providing some limited 
 # control of layout of text.
 
    def __init__(self, WN_instance):
        self.WN_instance = WN_instance
        self.initUI()


    def initUI(self):
        self.root = tk.Toplevel()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 126)
        self.y_pos = str(int(self.screen_y / 2) - 80)
        self.window_size = "+".join(["252x160", self.x_pos, self.y_pos])
        self.root.geometry(self.window_size)
        self.root.title("Layout Options")
        self.justification_var = tk.StringVar()
        if self.WN_instance.text_entry.tag_ranges("sel"):
            _tags = self.WN_instance.text_entry.tag_names("sel.first")
            if "left" in _tags:
                self.justification_var.set("left")
            elif "center" in _tags:
                self.justification_var.set("center")
            elif "right" in _tags:
                self.justification_var.set("right")
            else:
                self.justification_var.set("left")
        else:
            _first_char_tags = self.WN_instance.text_entry.tag_names("1.0")
            if "left" in _first_char_tags:
                self.justification_var.set("left")
            elif "center" in _first_char_tags:
                self.justification_var.set("center")
            elif "right" in _first_char_tags:
                self.justification_var.set("right")
            else:
                self.justification_var.set("left")
        
        self.justification_frame = tk.Frame(self.root,
                                            width=90,
                                            relief="raised")
        self.button_frame = tk.Frame(self.root, 
                                     width=252, 
                                     relief="sunken")
        self.justification_label = tk.Label(self.root, text="Text Alignment:")
        self.justify_left = tk.Radiobutton(self.root,
                                           text="Left",
                                           value="left",
                                           variable=self.justification_var)
        self.justify_centre = tk.Radiobutton(self.root,
                                             text="Centre",
                                             value="center",
                                             variable=self.justification_var)
        self.justify_right = tk.Radiobutton(self.root,
                                            text="Right",
                                            value="right",
                                            variable=self.justification_var)
        self.confirm_button = tk.Button(self.root,
                                        text="Confirm",
                                        command=self.confirm)
        self.cancel_button = tk.Button(self.root,
                                       text="Cancel",
                                       command=self.cancel)
                                       
        self.justification_frame.pack(fill="y", 
                                      side="left", 
                                      anchor="w", 
                                      expand=1)
        self.button_frame.pack(side="top", fill="x", anchor="s", expand=1)
        self.justification_label.pack(anchor="w", 
                                      in_=self.justification_frame)
        self.justify_left.pack(anchor="w",in_=self.justification_frame)
        self.justify_centre.pack(anchor="w", in_=self.justification_frame)
        self.justify_right.pack(anchor="w", in_=self.justification_frame)
        self.confirm_button.pack(side="left", anchor="e", in_=self.button_frame)
        self.cancel_button.pack(side="left", anchor="e", in_=self.button_frame)

        self.root.mainloop()


    def set_just(self, justification):
        self.justification_var.set(justification)
        return None


    def confirm(self):
        WN.layout_changes(self.WN_instance, self.justification_var.get())
        self.root.destroy()
        return None


    def cancel(self):
        self.root.destroy()
        return None



class TextSearch():
 # 'Find' dialogue for App, providing text-search functionality based 
 # on Tkinter 'search' function, with custom UI.
 # Allow for iterative search, unidirectional (top-down) at present.

    def __init__(self, WN_instance):
        self.WN_instance = WN_instance
        self.initUI()


    def initUI(self):
        self.root = tk.Toplevel()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.root.title("Find")

        # Attempts to position the dialogue away from main body of the 
        # text for ease of identifying matches.
        if self.WN_instance.view_mode == "standard":
            self.x_pos = str(int(self.screen_x / 2) + 198)
            self.y_pos = str(int(self.screen_y / 2) - 225)
            self.window_size = "+".join(["245x112", self.x_pos, self.y_pos])
        else: 
            if self.WN_instance.view_mode == "left panel":
                self.x_pos = str(int(self.screen_x / 2) + 2)
            elif self.WN_instance.view_mode == "right panel":
                self.x_pos = str(int(self.screen_x / 2) - 249)
            elif self.WN_instance.view_mode == "fullscreen":
                self.x_pos = str(int(self.screen_x - 256))
            self.window_size = "+".join(["245x112", self.x_pos, "0"])
        self.root.geometry(self.window_size)

        # Create, configure and pack widgets
        self.search_field = tk.Entry(self.root)
        self.find_button = tk.Button(self.root, 
                                     width=6, 
                                     text="Find", 
                                     command=self.find)
        self.cancel_button = tk.Button(self.root, 
                                       width=6, 
                                       text="Cancel", 
                                       command=self.close)
        self.helptext = tk.Label(self.root, 
                                 text="Enter text below then click 'Find' to "
                                 "search for the text within the document.\n"
                                 "Results are highlighted sequentially")
        self.search_field.focus_force()
        self.search_field.bind("<Return>", self.find)
        self.helptext.pack()
        self.search_field.pack()
        self.find_button.pack()
        self.cancel_button.pack()


    def find(self, event=None):
        self.search_text = self.search_field.get()
        if self.search_text == "":
            self.message_box = tkmb.showinfo("Error", 
                                             "No search text entered.", 
                                             icon="warning")
            self.search_field.focus_force()
            return None
        else:
            try:
                # Checks to see if this is the most recent search text.
                # This provides iterative functionality - if the search
                # text has not changed, it resumes searching from where
                # the last result was found.
                if self.search_text == self.previous_search_text:
                    if self.WN_instance.window_mode == "windowed":
                        previous_result = \
                            self.WN_instance.text_entry.tag_ranges("sel")
                    elif self.WN_instance.window_mode == "tabbed":
                        previous_result = \
                                self.WN_instance.get_active_tab()[1]\
                                .tag_ranges("sel")
                    if previous_result == self.WN_instance.last_search_result:
                        if self.WN_instance.window_mode == "windowed":
                            WN.search_text(self.WN_instance, 
                                           self.search_text, 
                                           previous_result[-1])
                        elif self.WN_instance.window_mode == "tabbed":
                            WN.search_text_tab(self.WN_instance,
                                               self.search_text,
                                               previous_result[-1])
                        return None
                    else:
                        self.previous_search_text = self.search_text
                        if self.WN_instance.window_mode == "windowed":
                            WN.search_text(self.WN_instance, self.search_text)
                        elif self.WN_instance.window_mode == "tabbed":
                            WN.search_text_tab(self.WN_instance, 
                                               self.search_text)
                        return None
            except AttributeError:
             # Raised if no previous search text has been saved.
                self.previous_search_text = self.search_text
                if self.WN_instance.window_mode == "windowed":
                    WN.search_text(self.WN_instance, self.search_text)
                elif self.WN_instance.window_mode == "tabbed":
                    WN.search_text_tab(self.WN_instance, self.search_text)
                return None


    def close(self):
        self.root.destroy()
        return None



class TextReplace():
 # 'Find' dialogue for App, providing text-based 'find and replace' 
 # functionality based on Tkinter 'search' function, with custom UI.
 # Currently provides iterative, unidirectional (top-down) searching.

    def __init__(self, WN_instance):
        self.WN_instance = WN_instance
        self.initUI()


    def initUI(self):
        self.root = tk.Toplevel()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.root.title("Find and Replace")
        
        # Attempts to place the dialogue away from the main body of the
        # text, for ease of identifying matches.
        if self.WN_instance.view_mode == "standard":
            self.x_pos = str(int(self.screen_x / 2) + 198)
            self.y_pos = str(int(self.screen_y / 2) - 225)
            self.window_size = "+".join(["245x75", self.x_pos, self.y_pos])
        else: 
            if self.WN_instance.view_mode == "left panel":
                self.x_pos = str(int(self.screen_x / 2) + 2)
            elif self.WN_instance.view_mode == "right panel":
                self.x_pos = str(int(self.screen_x / 2) - 249)
            elif self.WN_instance.view_mode == "fullscreen":
                self.x_pos = str(int(self.screen_x - 256))
            self.window_size = "+".join(["245x75", self.x_pos, "0"])
        self.root.geometry(self.window_size)
        
        # Create, configure and pack widgets.
        self.search_frame = tk.Frame(self.root)
        self.replace_frame = tk.Frame(self.root)
        self.button_frame = tk.Frame(self.root)
        self.search_text_label = tk.Label(self.root, text="Replace: ")
        self.search_field = tk.Entry(self.root)
        self.replacement_text_label = tk.Label(self.root, text="with: ")
        self.replace_field = tk.Entry(self.root)
        self.replace_button = tk.Button(self.root, 
                                        width=7, 
                                        text="Replace", 
                                        command=self.replace)
        self.cancel_button = tk.Button(self.root, 
                                       width=7, 
                                       text="Cancel", 
                                       command=self.close)
        self.search_field.focus_force()
        self.replace_field.bind("<Return>", self.replace)
        self.search_frame.pack(fill="x")
        self.replace_frame.pack(fill="x")
        self.button_frame.pack(side="right")
        self.search_text_label.pack(side="left", 
                                    anchor="e", 
                                    in_=self.search_frame)
        self.search_field.pack(side="right", 
                               fill="x", 
                               anchor="w", 
                               in_=self.search_frame)
        self.replacement_text_label.pack(side="left", 
                                         anchor="e", 
                                         in_=self.replace_frame)
        self.replace_field.pack(side="right", 
                                fill="x", 
                                anchor="w", 
                                in_=self.replace_frame)
        self.cancel_button.pack(side="right", in_=self.button_frame)
        self.replace_button.pack(side="right", in_=self.button_frame)


    def replace(self, event=None):
        self.search_text = self.search_field.get()
        self.replacement_text = self.replace_field.get()
        if self.search_text == "":
            self.message_box = tkmb.showinfo("Error", 
                                             "No search text entered.", 
                                             icon="warning")
            self.search_field.focus_force()
            return None
        elif self.replacement_text == "":
            self.message_box = tkmb.showinfo("Error", 
                                             "No replacement text entered.", 
                                             icon="warning")
            self.replace_field.focus_force()
            return None
        else:
            try:
                # Checks to see if this is the most recent search text.
                # This provides iterative functionality - if the search
                # text has not changed, it resumes searching from where
                # the last result was found, and replaced.
                if self.search_text == self.previous_search_text:
                    if self.WN_instance.window_mode == "windowed":
                        previous_result = \
                            self.WN_instance.text_entry.tag_ranges("sel")
                    elif self.WN_instance.window_mode == "tabbed":
                        previous_result = \
                            self.WN_instance.get_active_tab()[1].tag_ranges\
                                ("sel")
                    if previous_result == \
                            self.WN_instance.last_replacement_text:
                        WN.replace_text(self.WN_instance, 
                                        self.search_text, 
                                        self.replacement_text, 
                                        previous_result[-1])
                    else:
                        if self.WN_instance.window_mode == "windowed":
                            WN.replace_text(self.WN_instance, 
                                            self.search_text, 
                                            self.replacement_text)
                        elif self.WN_instance.window_mode == "tabbed":
                            WN.replace_text_tab(self.WN_instance, 
                                                self.search_text, 
                                                self.replacement_text)
                else:
                    if self.WN_instance.window_mode == "windowed":
                        WN.replace_text(self.WN_instance,
                                        self.search_text,
                                        self.replacement_text)
                    elif self.WN_instance.window_mode == "tabbed":
                        WN.replace_text_tab(self.WN_instance,
                                            self.search_text,
                                            self.replacement_text)
            except AttributeError:
             # Raised if no previous search text was saved.
                self.previous_search_text = self.search_text
                self.previous_replacement_text = self.replacement_text
                if self.WN_instance.window_mode == "windowed":
                    WN.replace_text(self.WN_instance, 
                                    self.search_text, 
                                    self.replacement_text)
                elif self.WN_instance.window_mode == "tabbed":
                    WN.replace_text_tab(self.WN_instance, 
                                        self.search_text, 
                                        self.replacement_text)
            return None


    def close(self):
        self.root.destroy()



def _save(username, settings, **kwargs):
    with open(os.path.dirname(__file__) + r'\configsettings.py', 
              "w+") as configfile:
        global _config
        for arg in kwargs:
            _config[username][settings][arg] = kwargs[arg]
        configfile.write("import os\n\nconfig  =  " + str(_config))


def _load(app, username, settings):
    if tkmb.askyesno("Warning", 
                     "WARNING - All user-defined settings will be restored "
                     "to the last saved settings for this user.  Continue?", 
                     icon="warning"):
        for k in _config[username][settings]:
            _config[username][settings][k] = \
                configsettings.config[username][settings][k]
        text = app.text_entry.get(1.0, "end")
        App = lambda:WN(app.username, 
                        text, 
                        app.saved, 
                        app.file_name, 
                        app.window_set, 
                        app.master)
        app.root.destroy()
        App()
        

def _default(app, username, settings):
    if tkmb.askyesno("Warning", 
                     "WARNING - All user-defined font settings will be "
                     "restored to their default values.  Continue?", 
                     icon="warning"):
        for k in _config[username][settings]:
            _config[username][settings][k] = \
                configsettings.config['default'][settings][k]
        with open("ocnfigsettings.py", "w+") as configfile:
            configfile.write("import os\n\nconfig  =  " + str(_config))
            text = app.text_entry.get(1.0, "end")
            App = lambda:WN(app.username, 
                            text, 
                            app.saved, 
                            app.file_name, 
                            app.window_set, 
                            app.master)
            app.root.destroy()
            App()        


def _external_unlock(Joshython_instance, WN_instance):
    """Unlock method associated with the Joshython class"""

    entered_password = Joshython_instance.unlock_password_entry.get()
    Joshython_instance.unlock_password_entry.delete(0, tk.END)
    user_password = jtlcd.lcd[Joshython_instance.username][0]
    if jt._hashcheck(entered_password, 
                     1,
                     Joshython_instance,
                     Joshython_instance.username) == user_password:
        jt.LOCKED = False
        Joshython_instance.unlock()
        if WN_instance.window_mode == "windowed":
            WN_instance.unlock(None, True)
        elif WN_instance.window_mode == "tabbed":
            WN_instance.unlock_tab_mode(None, True)
        WN_instance.master.root.iconify()
        return None
    else:
        tkmb.showinfo("Authentication Failure", "The password entered was "
                      "not correct.  Feel free to try again.  Alternatively, "
                      "you could try only accessing your own documents in "
                      "future.", icon="warning")
        with open("loglogginglogins.txt", "a+") as file:
            file.write("File unlock failed for user: " + 
                       Joshython_instance.username + 
                       " : Password entered: " + 
                       Joshython_instance.unlock_password_entry.get() + 
                       "\n")        
        Joshython_instance.unlock_password_entry.delete(0, "end")
        return None



class WN():
 # Main Class for the App.
    def __init__(self, 
                 username="default", 
                 file_contents="", 
                 saved=False, 
                 file_name="",
                 window_set = {},
                 tab_set = {},
                 pushed_tags = {},
                 custom_fonts = {},                 
                 master=None):
        if username not in _config:
            self.username = 'default'
        else:
            self.username = username
        # If force opened standalone, image loading fails as there is 
        # no tk.Tk() master available - one must exist.
        if not master:
            master=jt.Joshython(username)
            master.iconify()
        self.file_contents = file_contents
        self.saved = saved
        self.file_name = file_name
        self.whiteboard_contents = []
        self.hl_images = {}
        
        self.image_library = {}
        self.image_library["hly"] = "resources\\highlightyellow.bmp"
        self.image_library["hlo"] = "resources\\highlightorange.bmp"
        self.image_library["hlg"] = "resources\\highlightgreen.bmp"
        self.image_library["hlp"] = "resources\\highlightpink.bmp"
        self.image_library["cut"] = "resources\\scissors.bmp"
        self.image_library["paste"] = "resources\\paste.bmp"
        self.image_library["copy"] = "resources\\copy.bmp"
        self.image_library["wb"] = "resources\\whiteboard.bmp"
        self.image_library["cd"] = "resources\\chevdown.bmp"
        self.image_library["cl"] = "resources\\chevleft.bmp"
        self.image_library["undo"] = "resources\\undoarrow.bmp"
        self.image_library["home"] = "resources\\homemenu.bmp"
        self.image_library["save"] = "resources\\save.bmp"
        self.image_library["exit"] = "resources\\exit.bmp"
        self.image_library["open"] = "resources\\open.bmp"
        self.image_library["lock"] = "resources\\lock.bmp"
        self.hl_y_img = Image.open(self.image_library["hly"]).resize((40, 40))
        self.hl_o_img = Image.open(self.image_library["hlo"]).resize((40, 40))
        self.hl_g_img = Image.open(self.image_library["hlg"]).resize((40, 40))
        self.hl_p_img = Image.open(self.image_library["hlp"]).resize((40, 40))
        self.cut_img = Image.open(self.image_library["cut"]).resize((40, 40))
        self.copy_img = \
            Image.open(self.image_library["copy"]).resize((40, 40))
        self.paste_img = \
            Image.open(self.image_library["paste"]).resize((40, 40))
        self.wb_img = Image.open(self.image_library["wb"]).resize((40, 40))
        self.cd_img = Image.open(self.image_library["cd"]).resize((20, 20))
        self.cl_img = Image.open(self.image_library["cl"]).resize((20, 20))
        self.undo_img = \
            Image.open(self.image_library["undo"]).resize((40, 40))
        self.home_img = \
            Image.open(self.image_library["home"]).resize((40, 40))
        self.save_img = \
            Image.open(self.image_library["save"]).resize((40, 40))
        self.exit_img = \
            Image.open(self.image_library["exit"]).resize((40, 40))
        self.open_img = \
            Image.open(self.image_library["open"]).resize((40, 40))
        self.lock_img = \
            Image.open(self.image_library["lock"]).resize((40, 40))
        self.hl_images["yellow"] = ImageTk.PhotoImage(self.hl_y_img)
        self.hl_images["orange"] = ImageTk.PhotoImage(self.hl_o_img)
        self.hl_images["pink"] = ImageTk.PhotoImage(self.hl_p_img)
        self.hl_images["green"] = ImageTk.PhotoImage(self.hl_g_img)
        self.cut_image = ImageTk.PhotoImage(self.cut_img)
        self.copy_image = ImageTk.PhotoImage(self.copy_img)
        self.paste_image = ImageTk.PhotoImage(self.paste_img)
        self.wb_image = ImageTk.PhotoImage(self.wb_img)
        self.fb_button_image = ImageTk.PhotoImage(self.cd_img)
        self.eb_button_image = ImageTk.PhotoImage(self.cd_img)
        self.sb_button_image = ImageTk.PhotoImage(self.cd_img)
        self.cl_image = ImageTk.PhotoImage(self.cl_img)
        self.undo_image = ImageTk.PhotoImage(self.undo_img)
        self.home_image = ImageTk.PhotoImage(self.home_img)
        self.save_image = ImageTk.PhotoImage(self.save_img)
        self.exit_image = ImageTk.PhotoImage(self.exit_img)
        self.open_image = ImageTk.PhotoImage(self.open_img)
        self.lock_image = ImageTk.PhotoImage(self.lock_img)

        self.checksum_text = self.file_contents.encode("utf-8")
        self.checksum = hashlib.md5(self.checksum_text)
        self.window_set = window_set
        self.pushed_tags = pushed_tags
        self.master = master
        self.view_mode = "standard"
        self.find_dialogue = None
        self.replace_dialogue = None
        self.TextColourDialogue = None
        self.text_colour = "black"
        self.non_font_tags = {"sel" : ("",),
                              "left" : ("",),
                              "center" : ("",),
                              "right" : ("",),
                              "yellow" : ("",),
                              "orange" : ("",),
                              "pink" : ("",),
                              "green" : ("",),
                              "superscript" : ("",),
                              "subscript" : ("",)}
        self.text_colour_tags = {}
        for tag in self.pushed_tags:
            if tag.startswith("#"):
                self.text_colour_tags[tag] = self.pushed_tags[tag][1]
        self.highlight_colour = tk.StringVar(value="yellow")
        self.chev_angle = 0
        self.in_banner_displacement = 0
        self.banners_list = []
        self._iter_count = 0
        self.repack_queue = {}
        self.window_mode = "windowed"
        self.tab_set = tab_set
        self.custom_fonts_dict = custom_fonts
        
        self.initUI()


    def __repr__(self):
        """Creates a text editing app.
        One required argument - username, four optional positional 
        arguments - file_contents, saved, file_name, window_set.  
        Username is the name of the logged in user, auto-populated 
        during the login process.  file_contents is the raw text 
        content of the file - set by the functions save_file(), 
        save_file_as(), open_file() and open_new().  saved is a Boolean
        variable used to determine whether or not the file contents 
        have been changed since the last save.  file_name is the file 
        system name of the file, as set by the Operating System and 
        controlled by save_file, save_file_as, open_file and open_new. 
        window_set is a list of currently open instances of the window,
        used to determine the number of closures needed for the 
        mainmenu function.  Called using 'wordnote.WN()'
        """
        return self.__repr__.__doc__


    def __str__(self):
        """Creates a text editing app.
        One required argument - username, four optional positional 
        arguments - file_contents, saved, file_name, window_set.  
        Username is the name of the logged in user, auto-populated 
        during the login process.  file_contents is the raw text 
        content of the file - set by the functions save_file(), 
        save_file_as(), open_file() and open_new().  saved is a Boolean
        variable used to determine whether or not the file contents 
        have been changed since the last save.  file_name is the file 
        system name of the file, as set by the Operating System and 
        controlled by save_file, save_file_as, open_file and open_new. 
        window_set is a list of currently open instances of the window,
        used to determine the number of closures needed for the 
        mainmenu function.  Called using 'wordnote.WN()'
        """
        return self.__str__.__doc__ 


    def __iter__(self):
        return self
    def __next__(self):
        self._items = self.text_entry.get("1.0", "end").split()
        try:
            self._next = self._items[self._iter_count]
        except IndexError:
            self._iter_count = 0
            raise StopIteration
        else:
            self._iter_count += 1
            return self._next
        


    def __eq__(self, other):
        if self.master == other.master and \
                self.window_set[self.count] == other.window_set[other.count]:
            return True
        else:
            return False


    def __ne__(self, other):
        if self.master is not other.master or \
                self.window_set[self.count] != other.window_set[other.count]:
            return True
        else:
            return False


    def initUI(self):
     # Defines and initialises the UI.
        self.root = tk.Toplevel()
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        self.x_pos = str(int(self.screen_x / 2) - 200)
        self.y_pos = str(int(self.screen_y / 2) - 225)
        self.window_size = "+".join(["401x451", self.x_pos, self.y_pos])
        if self.file_name is not "":
            self.root.title("".join(["Wordnote",
                                     " - ",
                                     os.path.basename(self.file_name)]))
        else:
            self.root.title("Wordnote")
        self.root.geometry(self.window_size)

        self.custom_font = tkf.nametofont("TkTextFont")
        self.custom_fonts_dict["custom_font"] = self.custom_font
        user_font_settings = _config[self.username]['font']
        self.custom_font.configure(family=user_font_settings['family'], 
                                   size=user_font_settings['size'], 
                                   weight=user_font_settings['weight'], 
                                   slant=user_font_settings['slant'], 
                                   overstrike=user_font_settings['overstrike'], 
                                   underline=user_font_settings['underline'])

        self.tag_font = tkf.Font(family="Arial", size="12")
        self.image_library['bg'] = _config[self.username]['images']['bg']
        self.bg_img = Image.open(self.image_library["bg"]).resize((480, 491))
        self.bg_image = ImageTk.PhotoImage(self.bg_img)
        self.img_canvas = tk.Canvas(self.root, 
                                    width="401", 
                                    height="491", 
                                    bg="white")
        self.img_canvas.create_image(200, 
                                     225, 
                                     image=self.bg_image, 
                                     tags='img')
        x1, y1 = self.img_canvas.coords('img')
        self.img_canvas.tag_raise('img')

        # Banners
        self.back_banner_canvas = tk.Canvas(self.root,
                                            width=52,
                                            height=390)
        self.vertscroll_banner = tk.Scrollbar(self.root)
        self.back_banner_canvas.config(yscrollcommand=
                                       self.vertscroll_banner.set)
        self.banner_frame = tk.Frame(self.back_banner_canvas)
        self.vertscroll_banner.config(command=self.back_banner_canvas.yview)
        self.back_banner_canvas.create_window((21, 0),
                                              width="52",
                                              height="150",
                                              window=self.banner_frame,
                                              anchor="nw",
                                              tags="banner_frame")
        self.file_banner_button = tk.Button(self.banner_frame,
                                            text="File",
                                            width="52",
                                            relief="raised",
                                            image="",
                                            compound="right",
                                            command=self.file_banner_display)
        self.file_banner_canvas = tk.Canvas(self.banner_frame,
                                            width="52",
                                            height="5",
                                            bg="white")
        self.banners_list.append(self.file_banner_canvas)
        self.file_banner_canvas.create_image(22,
                                             -180,
                                             image=self.open_image,
                                             tags="open")
        self.file_banner_canvas.create_image(22,
                                             -140,
                                             image=self.save_image,
                                             tags="save")
        self.file_banner_canvas.create_image(22,
                                             -100,
                                             image=self.lock_image,
                                             tags="lock")
        self.file_banner_canvas.create_image(22,
                                             -60,
                                             image=self.home_image,
                                             tags="home")
        self.file_banner_canvas.create_image(22,
                                             -20,
                                             image=self.exit_image,
                                             tags="exit")
        self.file_banner_canvas.tag_bind("open",
                                         "<1>",
                                         self.open_file,
                                         add="+")
        self.file_banner_canvas.tag_bind("save",
                                         "<1>",
                                         self.save_file,
                                         add="+")
        self.file_banner_canvas.tag_bind("lock", "<1>", self.lock, add="+")
        self.file_banner_canvas.tag_bind("home", "<1>", self.mainmenu, add="+")
        self.file_banner_canvas.tag_bind("exit", "<1>", self.exit, add="+")
        self.edit_banner_button = tk.Button(self.banner_frame,
                                            text="Edit",
                                            width="52",
                                            relief="raised",
                                            image="",
                                            compound="right",
                                            command=self.edit_banner_display)
        self.edit_banner_canvas = tk.Canvas(self.banner_frame,
                                            width="52",
                                            height="5",
                                            bg="white")
        self.banners_list.append(self.edit_banner_canvas)
        self.edit_banner_canvas.create_image(22,
                                             -220,
                                             image=self.hl_images["yellow"],
                                             tags=("yellow", "highlight"))
        self.edit_banner_canvas.create_image(22,
                                             -220,
                                             image=self.hl_images["orange"],
                                             tags=("orange", "highlight"))
        self.edit_banner_canvas.create_image(22,
                                             -220,
                                             image=self.hl_images["pink"],
                                             tags=("pink", "highlight"))
        self.edit_banner_canvas.create_image(22,
                                             -220,
                                             image=self.hl_images["green"],
                                             tags=("green", "highlight"))
        self.edit_banner_canvas.create_image(22,
                                             -180,
                                             image=self.undo_image,
                                             tags="undo")
        self.edit_banner_canvas.create_image(22,
                                             -140,
                                             image=self.cut_image,
                                             tags="cut")
        self.edit_banner_canvas.create_image(22,
                                             -100,
                                             image=self.copy_image,
                                             tags="copy")
        self.edit_banner_canvas.create_image(22,
                                             -60,
                                             image=self.paste_image,
                                             tags="paste")
        self.edit_banner_canvas.create_image(22,
                                             -20,
                                             image=self.wb_image,
                                             tags="wb")
        self.edit_banner_canvas.tag_raise("orange")
        self.edit_banner_canvas.tag_raise("green")
        self.edit_banner_canvas.tag_raise("pink")
        self.edit_banner_canvas.tag_raise("yellow")
        self.edit_banner_canvas.tag_raise("cut")
        self.edit_banner_canvas.tag_raise("copy")
        self.edit_banner_canvas.tag_raise("paste")
        self.edit_banner_canvas.tag_raise("undo")
        self.edit_banner_canvas.tag_raise("wb")
        self.edit_banner_canvas.tag_bind("undo", "<1>", self.undo, add="+")
        self.edit_banner_canvas.tag_bind("paste", "<1>", self.paste, add="+")
        self.edit_banner_canvas.tag_bind("copy", "<1>", self.copy, add="+")
        self.edit_banner_canvas.tag_bind("cut", "<1>", self.cut, add="+")
        self.edit_banner_canvas.tag_bind("highlight", 
                                         "<1>", 
                                         self.highlight, 
                                         add="+")
        self.edit_banner_canvas.tag_bind("wb", 
                                         "<1>", 
                                         self.add_to_whiteboard, 
                                         add="+")
        self.style_banner_button = tk.Button(self.banner_frame,
                                            text="Style",
                                            width="52",
                                            relief="raised",
                                            image="",
                                            compound="right",
                                            command=self.style_banner_display)
        self.style_banner_canvas = tk.Canvas(self.banner_frame,
                                             width="52",
                                             height="5",
                                             bg="white")
        self.banners_list.append(self.style_banner_canvas)
        self.style_banner_canvas.create_text(22,
                                             -180,
                                             text="B",
                                             font="Times 32 bold roman",
                                             tags="bold")
        self.style_banner_canvas.create_text(22,
                                             -140,
                                             text="I",
                                             font="Times 32 normal italic",
                                             tags="italic")
        self.style_banner_canvas.create_text(22,
                                             -100,
                                             text="U",
                                             font="Times 32 normal "
                                                  "roman underline",
                                             tags="underline")
        self.style_banner_canvas.create_text(22,
                                             -60,
                                             text="S",
                                             font="Times 32 normal "
                                                  "roman overstrike",
                                             tags="strikethrough")
        for canvas_item in self.style_banner_canvas.find_all():
            self.style_banner_canvas.tag_bind(canvas_item,
                                              "<Button>",
                                             self.style_canvas_font_toggle,
                                             add="+")
        self.style_banner_canvas.create_text(22,
                                             -20,
                                             text="  A\nB  C",
                                             font="Times 14 normal roman",
                                             fill=self.text_colour,
                                             tags="text_colour")
        self.style_banner_canvas.tag_bind("text_colour",
                                          "<1>",
                                          self.change_text_colour,
                                          add="+")
        self.menu_bar = tk.Menu(self.root, tearoff=0)
        self.dummy_menu = tk.Menu(self.root, tearoff=0)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Window", 
                                   accelerator="Ctrl+N", 
                                   command=self.new)
        self.file_menu.add_command(label="Open", 
                                   accelerator="Ctrl+O", 
                                   command=self.open_file)
        self.file_menu.add_command(label="Open in new window", 
                                   accelerator="Ctrl+Shift+O", 
                                   command=self.open_new)
        self.file_menu.add_command(label="Duplicate", 
                                   accelerator="Ctrl+D", 
                                   command=self.duplicate)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", 
                                   accelerator="Ctrl+S", 
                                   command=self.save_file)
        self.file_menu.add_command(label="Save As", 
                                   accelerator="Ctrl+Shift+S", 
                                   command=self.save_file_as)
        self.file_menu.add_command(label="Print", 
                                   accelerator="Ctrl+P", 
                                   command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Lock File", 
                                   accelerator="Ctrl+L", 
                                   command=self.lock)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Main Menu", 
                                   accelerator="Ctrl+M", 
                                   command=self.mainmenu)
        self.file_menu.add_command(label="Close", 
                                   accelerator="Ctrl+Q", 
                                   command=self.close)
        self.file_menu.add_command(label="Close Others",
                                   accelerator="Ctrl+Shift+Q",
                                   command=self.close_others)
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo",
                                   accelerator="Ctrl+Z",
                                   command=self.undo)
        self.edit_menu.add_command(label="Redo",
                                   accelerator="Ctrl+Y",
                                   command=self.redo)
        self.edit_menu.add_command(label="Clear", 
                                   accelerator="F5", 
                                   command=self.reset)
        self.edit_menu.add_command(label="Select All", 
                                   accelerator="Ctrl+A", 
                                   command=self.select_all)
        self.hl_menu = tk.Menu(self.root, tearoff=0)
        self.hl_menu.add_command(label="Green", 
                                 command=lambda:self.highlight(colour=
                                                               "green"))
        self.hl_menu.add_command(label="Orange", 
                                 command=lambda:self.highlight(colour=
                                                               "orange"))
        self.hl_menu.add_command(label="Pink", 
                                 command=lambda:self.highlight(colour=
                                                               "pink"))
        self.hl_menu.add_command(label="Yellow", 
                                 command=lambda:self.highlight(colour=
                                                               "yellow"))
        self.edit_menu.add_command(label="Highlight Text", 
                                   command=self.highlight)
        self.edit_menu.add_command(label="Remove Highlight", 
                                   command=self.remove_highlight)
        self.edit_menu.add_cascade(label="Change Highlight Colour", 
                                   menu=self.hl_menu)
        self.edit_menu.add_command(label="Copy", 
                                   accelerator="Ctrl+C", 
                                   command=self.copy)
        self.edit_menu.add_command(label="Cut", 
                                   accelerator="Ctrl+X", 
                                   command=self.cut)
        self.edit_menu.add_command(label="Paste", 
                                   accelerator="Ctrl+V", 
                                   command=self.paste)
        self.edit_menu.add_command(label="Find", 
                                   accelerator="Ctrl+F", 
                                   command=self.find)
        self.edit_menu.add_command(label="Replace", 
                                   accelerator="Ctrl+R", 
                                   command=self.replace)
        self.whiteboard = tk.Menu(self.edit_menu, tearoff=0)
        self.whiteboard.add_command(label="Add to Whiteboard", 
                                    accelerator="Ctrl+W", 
                                    command=self.add_to_whiteboard)
        self.whiteboard.add_command(label="Clear Whiteboard", 
                                    command=self.clear_whiteboard)
        self.edit_menu.add_command(label="Fix Text", 
                                   command=lambda:self.fix_text(
                                   self.text_entry)
                                   )
        self.edit_menu.add_cascade(label="Whiteboard", menu=self.whiteboard)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # Toolbars Submenu
        self.toolbars_menu = tk.Menu(self.root, tearoff=0)
        self.toolbars_menu.add_command(label="Show Menu Bar", 
                                       command=self.show_menu_bar)
        self.toolbars_menu.add_command(label="Show Banner Bar", 
                                       command=self.show_button_banner)
        self.toolbars_menu.add_command(label="Hide Menu Bar", 
                                       command=self.hide_menu_bar)
        self.toolbars_menu.add_command(label="Hide Banner Bar", 
                                       command=self.hide_button_banner)

        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Standard", 
                                   accelerator="F8", 
                                   command=lambda:self.view_change(
                                   "standard"))
        self.view_menu.add_command(label="Fullscreen", 
                                   accelerator="F11", 
                                   command=lambda:self.view_change(
                                   "fullscreen"))
        self.view_menu.add_command(label="Left Panel", 
                                   accelerator="F9", 
                                   command=lambda:self.view_change(
                                   "left panel"))
        self.view_menu.add_command(label="Right Panel", 
                                   accelerator="F10", 
                                   command=lambda:self.view_change(
                                   "right panel"))
        self.view_menu.add_separator()
        self.window_mode_menu = tk.Menu(self.view_menu, tearoff=0)
        self.window_mode_menu.add_command(label="Tab Mode",
                                          accelerator="F6",
                                          command=lambda:\
                                              self.switch_window_mode(
                                          "tabbed"))
        self.window_mode_menu.add_command(label="Window Mode",
                                          accelerator="F7",
                                          command=lambda:\
                                              self.switch_window_mode(
                                          "windowed"))
        self.view_menu.add_cascade(label="Window Mode", 
                                   menu=self.window_mode_menu)
        self.view_menu.add_separator()
        self.view_menu.add_cascade(label="Toolbars", menu=self.toolbars_menu)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Options Menu
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.font_size = tk.Menu(self.options_menu, tearoff=0)
        def size_selection(size):
            self.font_size.add_command(label=str(size), 
                                       command=lambda: \
                                           self.font_size_change(str(size)))
            return None
        for num in range(2, 21, 2):
            size_selection(num)
        self.options_menu.add_command(label="Font Options", 
                                      command=lambda:FontDialogue(self))
        self.options_menu.add_command(label="Layout Options",
                                      command=self.layout_options)
        self.options_menu.add_command(label="Change Text Colour",
                                      command=self.change_text_colour)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Save Font Settings", 
                                      command=lambda:_save(self.username, 
                                      'font', 
                                      size=self.custom_font["size"], 
                                      family=self.custom_font["family"], 
                                      slant=self.custom_font["slant"], 
                                      overstrike=self.custom_font["overstrike"], 
                                      underline=self.custom_font["underline"], 
                                      weight=self.custom_font["weight"]))
        self.options_menu.add_command(label="Load Font Settings", 
                                      command=lambda:_load(self, 
                                                           self.username, 
                                                           'font'))
        self.options_menu.add_command(label="Restore Default Font Settings", 
                                      command=lambda:_default(self, 
                                                              self.username, 
                                                              'font'))
        self.options_menu.add_cascade(label="Font Size", menu=self.font_size)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Entertainment", 
                                      command=self.super_sound)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        # Context Menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Undo",
                                      accelerator="Ctrl+Z",
                                      command=self.undo)
        self.context_menu.add_command(label="Redo",
                                      accelerator="Ctrl+Y",
                                      command=self.redo)
        self.context_menu.add_command(label="Copy", 
                                      accelerator="Ctrl+C", 
                                      command=self.copy)
        self.context_menu.add_command(label="Cut", 
                                      accelerator="Ctrl+X", 
                                      command=self.cut)
        self.context_menu.add_command(label="Paste", 
                                      accelerator="Ctrl+V", 
                                      command=self.paste)
        self.context_menu.add_separator()
        self.context_menu.add_cascade(label="Whiteboard", 
                                      menu=self.whiteboard)
        self.context_menu.add_separator()
        self.context_menu.add_cascade(label="Toolbars", 
                                      menu=self.toolbars_menu)

        # Initialise and configure widgets.
        self.tab_labels_frame = tk.Canvas(self.root)
        self.text_frame = tk.Frame(self.root, relief="sunken")
        self.active_text_frame = self.text_frame
        self.text_entry = tk.Text(self.root, 
                                  font=self.custom_font, 
                                  wrap="word",
                                  undo="True",
                                  maxundo="5", 
                                  height="20", 
                                  width="40")
        self.text_entry.insert("end", self.file_contents)

        self.text_entry.tag_add("custom_font", "1.0", "end")
        self.text_entry.tag_config("custom_font", font=self.custom_font)
        self.vertscroll = tk.Scrollbar(self.root)
        self.text_entry.config(yscrollcommand=self.vertscroll.set)
        self.vertscroll.config(command=self.text_entry.yview)
        self.root.config(menu=self.dummy_menu)

        # Key combination ("shortcut") binds.
        self.windowed_text_entry_keybinds(self.text_entry)
        self.back_banner_canvas.bind("<Enter>", self.update_geometry)
        self.root.bind_all("<Alt-KeyPress-F4>", "")
        self.root.bind_all("<Alt-KeyPress-F4>", self.close)
        self.root.bind_all("<F10>", "")
        self.root.bind_all("<KeyPress-F6>", 
                           lambda e:self.switch_window_mode("tabbed"))
        self.root.bind_all("<KeyPress-F7>",
                           lambda e:self.switch_window_mode("windowed"))
        self.root.bind("<KeyPress-F8>", 
                       lambda e:self.view_change("standard"))
        self.root.bind("<KeyPress-F9>", 
                       lambda e:self.view_change("left panel"))
        self.root.bind("<KeyPress-F10>", 
                       lambda e:self.view_change("right panel"))
        self.root.bind("<KeyPress-F11>", 
                       lambda e:self.view_change("fullscreen"))
        self.root.bind("<Button-3>", self.show_context_menu)
        self.file_banner_button.bind("<Enter>", self.banner_expand)
        self.file_banner_button.bind("<Leave>", self.banner_collapse)
        self.edit_banner_button.bind("<Enter>", self.banner_expand)
        self.edit_banner_button.bind("<Leave>", self.banner_collapse)
        self.style_banner_button.bind("<Enter>", self.banner_expand)
        self.style_banner_button.bind("<Leave>", self.banner_collapse)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind_all("<Control-KeyPress-#>", self.test)
        self.back_banner_canvas.bind("<Configure>", self._update_scroll)

        
        # Pack widgets and start event loop.
        self.img_canvas.pack(fill="both", expand="1")
        global count
        self.window_set[count] = self
        print(self.window_set[count].text_frame)
        self.count = count
        count += 1
        
        if len(self.window_set) == 1:
            x = 0.0
            self.root.attributes('-alpha', x)
            self.root.iconbitmap(_config[self.username]['images']['icon'])
            for n in range(20):
                x += 0.05
                self.root.after(75, self.root.attributes('-alpha', x))
                self.root.update()
            self.root.after(1000, self.launch)
        else:
            self.launch()
        self.text_entry.focus_force()
        if self.count == 0:
            self.root.mainloop()
        
        
    def launch(self):
    # Would be nice if the Text widget could already be present behind 
    # the image as it scrolls out of view.  Also, need to work on a 
    # 'reel' movement type - image does not move, but gets cut off 
    # slowly, could be done by placing image in a label that is reduced
    # in vertical size rapidly.
        self.back_banner_canvas.pack(anchor="n",
                                     side="right",
                                     fill="both",
                                     expand=1)
        self.file_banner_button.pack(in_=self.banner_frame)
        self.edit_banner_button.pack(in_=self.banner_frame)
        self.style_banner_button.pack(in_=self.banner_frame)
        self.root.update_idletasks()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        self.root.update()
        self.text_frame.pack(anchor="e", side="top", fill="both", expand="1")
        self.vertscroll.pack(side="right", fill="y", in_=self.text_frame)
        self.text_entry.pack(fill="both", expand="1", in_=self.text_frame)
        self.active_text_frame = self.text_frame
        self.banner_frame_children = self.banner_frame.winfo_children()
        for child in self.banner_frame_children:
            self.repack_queue[child] = [False, {}]
            if child.winfo_ismapped():
                self.repack_queue[child][1] = child.pack_info()
            else:
                continue
        self.repack_queue[self.vertscroll_banner] = [None, {}]
        self.repack_queue[self.back_banner_canvas] = [True,
                              self.back_banner_canvas.pack_info()]
        try:
            if len(self.window_set) == 1:
                for n in range(0, 116):
                    self.root.after(10, self.img_canvas.move('img', 0, -4))
                    self.root.update()
                self._repack()
                self.img_canvas.destroy()
            else:
                self._repack()
                self.img_canvas.destroy()
        except tk.TclError:
            raise LaunchFailureError(self)
        else:
            self.root.config(menu=self.menu_bar)
            self.text_entry.tag_add("left", "1.0", "end")
            self.root.update()
            for font in self.custom_fonts_dict:
                if font is "custom_font":
                    continue
                for font_range in range(0, len(self.pushed_tags[font][0]), 2):
                    self.text_entry.tag_add(font, 
                                          self.pushed_tags[font][0][font_range],
                                          self.pushed_tags[font][0][font_range+1])
                    self.text_entry.tag_config(font,
                                               font=self.custom_fonts_dict[font])
            for colour in self.text_colour_tags:
                for c_range in range(0, len(self.pushed_tags[colour][0]), 2):
                    self.text_entry.tag_add(colour,
                                           self.pushed_tags[colour][0][c_range],
                                           self.pushed_tags[colour][0][c_range+1])
                    self.text_entry.tag_config(colour, foreground=colour)
            for tag in self.pushed_tags:
                if tag is "sel":
                    continue
                elif tag in ["left", "center", "right"]:
                    for just in range(0, len(self.pushed_tags[tag][0]), 2):
                        self.text_entry.tag_add(tag,
                                                self.pushed_tags[tag][0][just],
                                                self.pushed_tags[tag][0][just+1])
                        self.text_entry.tag_config(tag, justify=tag)
                        self.non_font_tags[tag] = self.text_entry.tag_ranges(tag)
                elif tag in ["yellow", "green", "orange", "pink"]:
                    for hl in range(0, len(self.pushed_tags[tag][0]), 2):
                        self.text_entry.tag_add(tag,
                                                self.pushed_tags[tag][0][hl],
                                                self.pushed_tags[tag][0][hl+1])
                        self.text_entry.tag_config(tag, background=tag)
                        self.non_font_tags[tag] = self.text_entry.tag_ranges(tag)
                elif tag in ["superscript", "subscript"]:
                    for offset in range(0, len(self.pushed_tags[tag][0]), 2):
                        self.text_entry.tag_add(tag,
                                               self.pushed_tags[tag][0][offset],
                                               self.pushed_tags[tag][0][offset+1])
                        self.text_entry.tag_config(tag,
                                        offset=self.pushed_tags[tag][1]["offset"])
                        self.non_font_tags[tag] = self.text_entry.tag_ranges(tag)
            if jt.LOCKED:
               self.lock()
        finally:
            return None


    def windowed_text_entry_keybinds(self, text_entry):
        print("called windowed_text_entry_keybinds")
        text_entry.bind("<Control-KeyPress-w>", self.add_to_whiteboard)
        text_entry.bind("<Control-KeyPress-z>", self.undo)
        text_entry.bind("<Control-KeyPress-y>", self.redo)
        text_entry.bind("<Control-KeyPress-c>", self.copy)
        text_entry.bind("<Control-KeyPress-x>", self.cut)
        text_entry.bind("<Control-KeyPress-v>", self.paste)
        text_entry.bind("<Control-KeyPress-f>", self.find)
        text_entry.bind("<Control-KeyPress-r>", self.replace)
        text_entry.bind("<Control-KeyPress-d>", self.duplicate)
        text_entry.bind("<Control-KeyPress-p>", self.print_file)
        text_entry.bind("<Control-KeyPress-m>", self.mainmenu)
        text_entry.bind("<Control-KeyPress-q>", self.close)
        text_entry.bind("<Control-Shift-KeyPress-Q>", self.close_others)
        text_entry.bind("<KeyPress-F5>", self.reset)
        text_entry.bind("<Control-KeyPress-a>", self.select_all)
        text_entry.bind("<Control-KeyPress-s>", self.save_file)
        text_entry.bind("<Control-KeyPress-o>", self.open_file)
        text_entry.bind("<Control-Shift-KeyPress-S>", self.save_file_as)
        text_entry.bind("<Control-Shift-KeyPress-O>", self.open_new)
        text_entry.bind("<Control-KeyPress-n>", self.new)
        text_entry.bind("<Control-KeyPress-l>", self.lock)
        text_entry.bind("<Enter>", self.update_geometry)
        text_entry.bind("<Control-KeyPress-4>", 
                        lambda e:self.fix_text(text_entry=self.text_entry))
        return None


    def tabbed_text_entry_keybinds(self, tab):
        print("called tabbed_text_entry_keybinds")
        text_entry = tab[0].winfo_children()[0]
        text_entry.bind("<Control-KeyPress-w>", self.add_to_whiteboard)
        text_entry.bind("<Control-KeyPress-z>", self.undo)
        text_entry.bind("<Control-KeyPress-y>", self.redo)
        text_entry.bind("<Control-KeyPress-c>", self.copy)
        text_entry.bind("<Control-KeyPress-x>", self.cut)
        text_entry.bind("<Control-KeyPress-v>", self.paste)
        text_entry.bind("<Control-KeyPress-f>", self.find)
        text_entry.bind("<Control-KeyPress-r>", self.replace)
        text_entry.bind("<Control-KeyPress-d>", self.duplicate_tab)
        text_entry.bind("<Control-KeyPress-p>", self.print_file)
        text_entry.bind("<Control-KeyPress-m>", self.mainmenu)
        text_entry.bind("<Control-KeyPress-q>", self.close_tab)
        text_entry.bind("<Control-Shift-KeyPress-Q>", self.close_other_tabs)
        text_entry.bind("<KeyPress-F5>", self.reset_tab)
        text_entry.bind("<Control-KeyPress-a>", self.select_all)
        text_entry.bind("<Control-KeyPress-s>", self.save_file_tab)
        text_entry.bind("<Control-KeyPress-o>", self.open_file_tab)
        text_entry.bind("<Control-Shift-KeyPress-S>", self.save_file_as_tab)
        text_entry.bind("<Control-Shift-KeyPress-O>", self.open_new_tab)
        text_entry.bind("<Control-KeyPress-n>", self.create_new_tab)
        text_entry.bind("<Control-KeyPress-l>", self.lock)
        text_entry.bind("<Enter>", self.update_geometry)
        text_entry.bind("<Control-KeyPress-4>", 
                        lambda e:self.fix_text(text_entry=self.text_entry))
        return None


    def update_geometry(self, event):
        """Tracks window movement, for view_change."""
        if self.view_mode == "standard":
            self.new_window_pos = self.root.geometry()
            self.root.update()
        return None


    def reset(self, event=None):
     # Deletes all text, with no save prompt
        self.text_entry.delete(1.0, "end")
        return None


    def reset_tab(self, event=None):
     # Deletes all text in the selected tab, with no save prompt
        tab = self.get_active_tab()
        tab[0].winfo_children()[0].delete(1.0, "end")
        return None


    def new(self, event=None):
     # Create new window with a blank document.
        new_app = WN(self.username, 
                     window_set=self.window_set, 
                     master=self.master)
        return None


    def open_file(self, event=None):
     # Calls Tkinter Windows 'Open' dialogue
     # Checks to see whether there are unsaved changes to the file and 
     # prompts to save if there are.
        try:
            if not self._validate():
                with filedialog.askopenfile(mode="r") as file:
                    if tkmb.askokcancel("Warning", 
                                        "You will lose any unsaved changes "
                                        "to this document if you continue.  "
                                        "If you click 'Cancel', you will be "
                                        "prompted to save the file."):
                        if file.name.endswith(".wnx"):
                            self.open_WN_file(file.name)
                        else:
                            file_contents = file.read()
                            self.text_entry.delete(1.0, "end")
                            self.text_entry.insert("end-1c", file_contents)
                            file_contents = file_contents.encode("utf-8")
                            self.checksum_text = file_contents
                        self.checksum = hashlib.md5(self.checksum_text)
                        self.saved = True
                        self.file_name = file.name
                        self.root.title("".join(["Wordnote",
                                        " - ",
                                        os.path.basename(self.file_name)]))
                        self.root.update()
                    else:
                        self.save_file_as()
            else:
                with filedialog.askopenfile(mode="r") as file:
                    if file.name.endswith(".wnx"):
                        self.open_WN_file(file.name)
                    else:
                        file_contents = file.read()
                        self.text_entry.delete(1.0, "end")
                        self.text_entry.insert("end-1c", file_contents)
                        file_contents = file_contents.encode("utf-8")
                        self.checksum_text = file_contents
                    self.checksum = hashlib.md5(self.checksum_text)
                    self.saved = True
                    self.file_name = file.name
                    self.root.title("".join(["Wordnote",
                                    " - ",
                                    os.path.basename(self.file_name)]))
                    self.root.update()
        except TypeError as e:
            print(e)
        finally:
            return None


    def open_file_tab(self, event=None):
        tab = self.get_active_tab()
        try:
            if not self._validate_tab(tab):
                with filedialog.askopenfile(mode="r") as file:
                    if tkmb.askokcancel("Warning", 
                                        "You will lose any unsaved changes "
                                        "to this document if you continue.  "
                                        "If you click 'Cancel', you will be "
                                        "prompted to save the file."):
                        if file.name.endswith(".wnx"):
                            self.open_WN_file_tab(tab, file.name)
                        else:
                            file_contents = file.read()
                            tab[1].delete(1.0, "end")
                            tab[1].insert("end-1c", file_contents)
                            file_contents = file_contents.encode("utf-8")
                            tab[5] = file_contents
                        tab[6] = hashlib.md5(self.checksum_text)
                        tab[7] = True
                        tab[8] = file.name
                        tab[3].config(label=tab[8])
                        self.root.title("".join(["Wordnote",
                                        " - ",
                                        os.path.basename(self.file_name)]))
                        self.root.update()
                    else:
                        self.save_file_as_tab(tab)
            else:
                with filedialog.askopenfile(mode="r") as file:
                    if file.name.endswith(".wnx"):
                        self.open_WN_file_tab(tab, file.name)
                    else:
                        file_contents = file.read()
                        tab[1].delete(1.0, "end")
                        tab[1].insert("end-1c", file_contents)
                        file_contents = file_contents.encode("utf-8")
                        tab[5] = file_contents
                    tab[6] = hashlib.md5(self.checksum_text)
                    tab[7] = True
                    tab[8] = file.name
                    self.root.title("".join(["Wordnote",
                                    " - ",
                                    os.path.basename(self.file_name)]))
                    self.root.update()
        except TypeError as e:
            print(e)
        finally:
            return None


    def open_WN_file(self, file):
        etree = ET.parse(file)
        root_node = etree.getroot()
        self.text_entry.delete("1.0", "end")
        self.text_entry.insert("1.0", root_node[1].text)
        for child in root_node[0][0]:
            name = child.attrib['name']
            font_config = child[0].attrib
            self.custom_fonts_dict[name] = tkf.Font(font=font_config)
            for attr in font_config:
                self.custom_fonts_dict[name][attr] = font_config[attr]
        for tag in root_node[0][1]:
            ranges = [_[1:-1:] for _ in tag.attrib['range'][1:-1:].split(", ")]
            config = tag.attrib['config'][1:-1:].split("=")
            config_dict = {config[0]:config[1]}
            if tag.attrib['name'] in self.custom_fonts_dict:
                for index in range(0, len(ranges), 2):
                    self.text_entry.tag_add(tag.attrib['name'],
                                            ranges[index],
                                            ranges[index+1])
                    self.text_entry.tag_config(tag.attrib['name'],
                              font=self.custom_fonts_dict[tag.attrib['name']])
            else:
                for index in range(0, len(ranges), 2):
                    self.text_entry.tag_add(tag.attrib['name'],
                                            ranges[index],
                                            ranges[index+1])
                    self.text_entry.tag_config(tag.attrib['name'],
                                               config_dict)
                if tag.attrib['name'].startswith("#"):
                    self.text_colour_tags[tag] = \
                        self.text_entry.tag_ranges(tag)
        self.checksum_text = self.text_entry.get("1.0", "end").encode("utf-8")
        
        self.root.update()


        def open_WN_file_tab(self, file):
            etree = ET.parse(file)
            root_node = etree.getroot()
            tab[1].delete("1.0", "end")
            tab[1].insert("1.0", root_node[1].text)
            for child in root_node[0][0]:
                name = child.attrib['name']
                font_config = child[0].attrib
                tab[9][name] = tkf.Font(font=font_config)
                for attr in font_config:
                    tab[9][name][attr] = font_config[attr]
            for tag in root_node[0][1]:
                ranges = [_[1:-1:] for _ in tag.attrib['range'][1:-1:].split(", ")]
                config = tag.attrib['config'][1:-1:].split("=")
                config_dict = {config[0]:config[1]}
                if tag.attrib['name'] in tab[9]:
                    for index in range(0, len(ranges), 2):
                        tab[1].tag_add(tag.attrib['name'],
                                       ranges[index],
                                       ranges[index+1])
                        tab[1].tag_config(tag.attrib['name'],
                                  font=tab[9][tag.attrib['name']])
                else:
                    for index in range(0, len(ranges), 2):
                        tab[9].tag_add(tag.attrib['name'],
                                       ranges[index],
                                       ranges[index+1])
                        tab[1].tag_config(tag.attrib['name'],
                                          config_dict)
                    if tag.attrib['name'].startswith("#"):
                        self.text_colour_tags[tag] = \
                            tab[1].tag_ranges(tag)
            tab[6] = tab[1].get("1.0", "end").encode("utf-8")
            
            self.root.update()


    def open_new(self, event=None):
     # Opens a previously saved file in a new window.
        new_app = WN
        try:        
            with filedialog.askopenfile(mode="r") as file:
                if file.name.endswith(".wnx"):
                    new_app.open_WN_file(new_app(username=self.username,
                                                 saved=True,
                                                 file_name=file.name,
                                                 window_set=self.window_set,
                                                 master=self.master),
                                         file.name)
                else:
                    file_contents = str(file.read())
                    new_app(username=self.username, 
                            file_contents=file_contents, 
                            saved=True, 
                            file_name=file.name,
                            window_set=self.window_set,
                            master=self.master)
        except AttributeError:
            try:
                new_app.close()
            except TypeError:
                new_app.close(new_app)
        finally:
            return None


    def open_new_tab(self, event=None):
        new_tab = create_new_tab()
        self.open_file_tab()
        return None


    def save_file(self, event=None):
     # Uses Tkinter Windows save dialogue to save the file.  Checks 
     # to see whether or not the file has previously been saved, and 
     # saves the file under the known name if it has - this also 
     # applies if the file was opened by Wordnote but created 
     # elsewhere.  Ideally Wordnote will allow the adding of 
     # encryption, a new 'save encrypted' version, which will convert 
     # 'file_contents' to something else and then call 'save_file' on 
     # that.  Could re-arrange this one to do a lock-check, each time, 
     # to reduce methods, maybe.
        if not self.saved:
            self.save_file_as()
            
        else:
            if self.file_name.endswith(".wnx"):
                self.save_WN_file(self.file_name)
                return None
            else:
                with open(self.file_name, "w") as file:
                    file_contents = str(self.text_entry.get(1.0, "end-1c"))
                    file.write(file_contents)
                    file_contents = file_contents.encode("utf-8")
                    self.checksum_text = file_contents
                    self.checksum = hashlib.md5(file_contents)
                    self.saved = True
                return None


    def save_file_tab(self, tab=None, event=None):
        if tab is None:
            tab = self.get_active_tab()
        if not tab[7]:
            self.save_file_as_tab(tab) 
        else:
            if self.file_name.endswith(".wnx"):
                self.save_WN_file(self.file_name)
                return None
            else:
                with open(tab[8], "w") as file:
                    file_contents = str(self.text_entry.get(1.0, "end-1c"))
                    file.write(file_contents)
                    file_contents = file_contents.encode("utf-8")
                    self.checksum_text = file_contents
                    self.checksum = hashlib.md5(file_contents)
                    self.saved = True
                return None


    def save_file_as(self, event=None, contents=None):
        """ Calls a built-in Tkinter Windows 'save file as' dialogue, 
        and stores a md5 hash of current file contents as a checksum to 
        check against if another file is opened in this same window.
        Provides a failsafe for occasions where the file is closed but 
        the dialogue remains open - the file will be saved intact in 
        this instance.
        """
        if contents is not None:
            file_contents = contents
        else:
            file_contents = str(self.text_entry.get(1.0, "end-1c"))
        try:
            with filedialog.asksaveasfile(mode="w", 
                                          defaultextension="txt") as file:
                if file.name.endswith(".wnx"):
                    self.save_WN_file(file.name)
                    return None
                else:
                    file.write(file_contents)
                    self.file_name = file.name
        except AttributeError:
         # AttributeError is raised if the cancel button is clicked on the 
         # savefileas dialogue
            if tkmb.askyesno("Warning!",
                             "If you continue, your file will not be saved!  "
                             "Continue?"):
                return None
            else:
                self.save_file_as(contents=file_contents)
        else:
            file_contents = file_contents.encode("utf-8")
            self.checksum_text = file_contents
            self.checksum = hashlib.md5(file_contents)
            self.saved = True
            self.root.title("".join(["Wordnote",
                                     " - ",
                                     os.path.basename(self.file_name)]))
            self.root.update()


    def save_file_as_tab(self, tab=None, event=None, contents=None):
        """ Calls a built-in Tkinter Windows 'save file as' dialogue, 
        and stores a md5 hash of current file contents as a checksum to 
        check against if another file is opened in this same window.
        Provides a failsafe for occasions where the file is closed but 
        the dialogue remains open - the file will be saved intact in 
        this instance.
        """
        if tab is None:
            tab = self.get_active_tab()
        file_contents = tab[1].get("1.0", "end")
        try:
            with filedialog.asksaveasfile(mode="w", 
                                          defaultextension="txt") as file:
                if file.name.endswith(".wnx"):
                    self.save_WN_file_tab(file.name, tab)
                    return None
                else:
                    file.write(file_contents)
                    tab[8] = file.name
                    self.tab_set[file.name] = tab
        except AttributeError:
         # AttributeError is raised if the cancel button is clicked on the 
         # savefileas dialogue
            if tkmb.askyesno("Warning!",
                             "If you continue, your file will not be saved!  "
                             "Continue?"):
                return None
            else:
                self.save_file_as_tab(tab)
        else:
            file_contents = file_contents.encode("utf-8")
            tab[5] = file_contents
            tab[6] = hashlib.md5(file_contents)
            tab[7] = True
            tab[3].config(text=tab[8])
            self.root.title("".join(["Wordnote",
                                     " - ",
                                     os.path.basename(tab[8])]))
            self.root.update()


    def save_WN_file(self, file):
        root_node = ET.Element("file")
        data_node = ET.SubElement(root_node, "data")
        body_node = ET.SubElement(root_node, "body")
        fonts_node = ET.SubElement(data_node, "fonts")
        tags_node = ET.SubElement(data_node, "tags")
        for key in self.custom_fonts_dict:
            font_node = ET.SubElement(fonts_node, "font", name=key)
            config_node = ET.SubElement(font_node, "fontconfig")
            for attr in self.custom_fonts_dict[key].actual():
                config_node.set(attr,
                              str(self.custom_fonts_dict[key].actual()[attr]))
        for tag in self.text_entry.tag_names():
            if tag == "sel" or tag == "custom_font":
                continue
            print(tag)
            range = tuple([str(i) for i in self.text_entry.tag_ranges(tag)])
            if range:
                print(range)
                print(repr(range[0]))
            else:
                continue
            tag_node = ET.SubElement(tags_node,
                                     "tag",
                                     name=tag,
                                     range=range)
            if tag in self.custom_fonts_dict:
                tag_node.set("config", "{font=%s}" % tag)
            elif tag in ["yellow", "orange", "pink", "green"]:
                tag_node.set('config', "{background=%s}" % tag)
            elif tag in ["left", "center", "right"]:
                tag_node.set('config', "{justify=%s}" % tag)
            elif tag in ["superscript", "subscript"]:
                tag_offset = self.text_entry.tag_config(tag)["offset"][4]
                tag_node.set("config", "{offset=%s}" % tag_offset)
            elif tag.startswith("#"):
                tag_node.set("config", "{foreground=%s}" % tag)
        body_node.text = self.text_entry.get("1.0", "end-1c")
        tree = ET.ElementTree(root_node)
        tree.write(file,
                   encoding="utf-8",
                   xml_declaration=True,
                   short_empty_elements=False)
        self.file_name = file
        with open(file, "r") as file_contents:
            self.checksum_text = file_contents.read()
        self.checksum_text = self.checksum_text.encode("utf-8")
        self.checksum = hashlib.md5(self.checksum_text)
        self.saved = True
        self.root.title("".join(["Wordnote",
                                 " - ",
                                 os.path.basename(self.file_name)]))
        self.root.update()
        return None


    def save_WN_file_tab(self, file, tab):
        root_node = ET.Element("file")
        data_node = ET.SubElement(root_node, "data")
        body_node = ET.SubElement(root_node, "body")
        fonts_node = ET.SubElement(data_node, "fonts")
        tags_node = ET.SubElement(data_node, "tags")
        for key in tab[9]:
            font_node = ET.SubElement(fonts_node, "font", name=key)
            config_node = ET.SubElement(font_node, "fontconfig")
            for attr in tab[9][key].actual():
                config_node.set(attr,
                              str(tab[9][key].actual()[attr]))
        for tag in tab[1].tag_names():
            if tag == "sel" or tag == "custom_font":
                continue
            print(tag)
            range = tuple([str(i) for i in tab[1].tag_ranges(tag)])
            if range:
                print(range)
                print(repr(range[0]))
            else:
                continue
            tag_node = ET.SubElement(tags_node,
                                     "tag",
                                     name=tag,
                                     range=range)
            if tag in tab[9]:
                tag_node.set("config", "{font=%s}" % tag)
            elif tag in ["yellow", "orange", "pink", "green"]:
                tag_node.set('config', "{background=%s}" % tag)
            elif tag in ["left", "center", "right"]:
                tag_node.set('config', "{justify=%s}" % tag)
            elif tag in ["superscript", "subscript"]:
                tag_offset = tab[1].tag_config(tag)["offset"][4]
                tag_node.set("config", "{offset=%s}" % tag_offset)
            elif tag.startswith("#"):
                tag_node.set("config", "{foreground=%s}" % tag)
        body_node.text = tab[1].get("1.0", "end-1c")
        tree = ET.ElementTree(root_node)
        tree.write(file,
                   encoding="utf-8",
                   xml_declaration=True,
                   short_empty_elements=False)
        tab[8] = file
        with open(file, "r") as file_contents:
            tab[5] = file_contents.read()
        tab[5] = tab[5].encode("utf-8")
        tab[6] = hashlib.md5(self.checksum_text)
        tab[7] = True
        self.root.title("".join(["Wordnote",
                                 " - ",
                                 os.path.basename(tab[8])]))
        self.root.update()
        return None


    def print_file(self, event=None):
     # Prints the current text to the default printer.  Future updates 
     # will allow for a printing options dialogue.
        default_printer = win32print.GetDefaultPrinter()
        file_contents = bytes(self.text_entry.get(1.0, "end"), "utf-8")
        self.printer = win32print.OpenPrinter(default_printer)
        print_job = win32print.StartDocPrinter(self.printer, 
                                               1, 
                                               (self.file_name, None, "RAW"))
        win32print.StartPagePrinter(self.printer)
        win32print.WritePrinter(self.printer, bytes("\n", "utf-8"))
        win32print.WritePrinter(self.printer, file_contents)
        win32print.WritePrinter(self.printer, bytes("\f", "utf-8"))
        win32print.EndPagePrinter(self.printer)
        win32print.EndDocPrinter(self.printer)
        win32print.ClosePrinter(self.printer)
        return None


    def print_file_tab(self, event=None):
     # Prints the current text to the default printer.  Future updates 
     # will allow for a printing options dialogue.  Tab mode.
        default_printer = win32print.GetDefaultPrinter()
        file_contents = bytes(self.get_active_tab()[1].get(1.0, "end"), 
                              "utf-8")
        self.printer = win32print.OpenPrinter(default_printer)
        print_job = win32print.StartDocPrinter(self.printer, 
                                               1, 
                                               (self.file_name, 
                                                None, 
                                                "RAW")
                                                )
        win32print.StartPagePrinter(self.printer)
        win32print.WritePrinter(self.printer, bytes("\n", "utf-8"))
        win32print.WritePrinter(self.printer, file_contents)
        win32print.WritePrinter(self.printer, bytes("\f", "utf-8"))
        win32print.EndPagePrinter(self.printer)
        win32print.EndDocPrinter(self.printer)
        win32print.ClosePrinter(self.printer)
        return None


    def _update_repack_queue(self):
        try:
            for child in self.banner_frame_children:
                if child.winfo_ismapped():
                    self.repack_queue[child][1] = child.pack_info()
                else:
                    continue
            return None
        except AttributeError: # windows made from tabs throw errors
            return None


    def _update_scroll(self, event):
        widget = event.widget
        widget.config(scrollregion=widget.bbox("all"))
        self.root.update_idletasks()
        self.root.update()
        return None
        

    def _repack(self):
        number_packed = 0
        if self.window_mode == "tabbed":
            for tab in self.tab_set:
                self.tab_set[tab][0].pack_forget()
        elif self.window_mode == "windowed":
            self.text_frame.pack_forget()
        for child in self.banner_frame_children:
            if self.repack_queue[child][0]:
                child.pack(self.repack_queue[child][1])
                self.repack_queue[child][0] = False
                self.root.update()
            else:
                pass
            if child.winfo_ismapped():
                number_packed += 1
            else:
                continue
        if self.window_mode == "tabbed":
            self.active_text_frame.pack(anchor="e",
                                        side="top",
                                        fill="both",
                                        expand="1")
        elif self.window_mode == "windowed":
            self.text_frame.pack(anchor="e",
                                 side="top",
                                 fill="both",
                                 expand="1")    
        self.root.update()
        if number_packed >= 4:
            if self.window_mode == "tabbed":
                for tab in self.tab_set:
                    self.tab_set[tab][0].pack_forget()
            elif self.window_mode == "windowed":
                self.text_frame.pack_forget()
            self.vertscroll_banner.pack(side="right",
                                        fill="y",
                                        in_=self.root)
            self.repack_queue[self.vertscroll_banner][0] = True
            if not self.repack_queue[self.vertscroll_banner][1]:
                self.repack_queue[self.vertscroll_banner][1] = \
                                  self.vertscroll_banner.pack_info()
            self.back_banner_canvas.config(width=72)
            self.window_size = "+".join(["411x451", self.x_pos, self.y_pos])
            self.view_change(self.view_mode)
            if self.window_mode == "tabbed":
                self.active_text_frame.pack(anchor="e",
                                            side="top",
                                            fill="both",
                                            expand="1")
            elif self.window_mode == "windowed":
                self.text_frame.pack(anchor="e",
                                     side="top",
                                     fill="both",
                                     expand="1")
            self.root.update_idletasks()
            self.root.update()
        else:
            if self.window_mode == "tabbed":
                for tab in self.tab_set:
                    self.tab_set[tab][0].pack_forget()
            elif self.window_mode == "windowed":
                self.text_frame.pack_forget()
            self.vertscroll_banner.pack_forget()
            self.repack_queue[self.vertscroll_banner][0] = None
            self.window_size = "+".join(["401x451", self.x_pos, self.y_pos])
            self.view_change(self.view_mode)
            if self.window_mode == "tabbed":
                self.active_text_frame.pack(anchor="e",
                                            side="top",
                                            fill="both",
                                            expand="1")
            elif self.window_mode == "windowed":
                self.text_frame.pack(anchor="e",
                                     side="top",
                                     fill="both",
                                     expand="1")
        self.root.update_idletasks()
        self.root.update()


    def _validate(self):
     # Checks current file contents against known saved file contents, 
     # using md5 hashes of each.
        current_contents = self.text_entry.get(1.0, "end-1c").encode("utf-8")
        current_contents = hashlib.md5(current_contents)
        self.checksum = hashlib.md5(self.checksum_text)
        if current_contents.hexdigest() == self.checksum.hexdigest():
            return True
        else:
            return False


    def _validate_tab(self, tab):
     # Checks current file contents against known saved file contents, 
     # using md5 hashes of each.
        current_contents = tab[1].get(1.0, "end-1c").encode("utf-8")
        current_contents = hashlib.md5(current_contents)
        tab[6] = hashlib.md5(tab[5])
        if current_contents.hexdigest() == tab[6].hexdigest():
            return True
        else:
            return False


    def hashcheck(self, text, salt):
     # Produces a sha256 hash of the entered password.
        text = str(text).encode("utf-8")
        salt = str(salt).encode("utf-8")
        result = salt + text
        for i in range(200001):
            result = hashlib.sha256(result).hexdigest().encode("utf-8")
        return result.decode("utf-8")


    def lock(self, event=None):
     # Locks the current window - requires the logged in user's 
     # password to unlock.
        jt.LOCKED = True
        self.master.lock(self)
        self.text_entry.config(state="disabled")
        if self.repack_queue[self.vertscroll_banner][0]:
            self.vertscroll_banner.pack_forget()
        if self.repack_queue[self.back_banner_canvas][0]:
            self.back_banner_canvas.pack_forget()
        self.text_frame.pack_forget()
        self.lock_screen = tk.Frame(self.root)
        
        # Create the password request widgets.
        self.password_request = tk.Label(self.lock_screen, 
                                         text="Enter your password to "
                                         "unlock the document: ")
        self.unlock_password_entry = tk.Entry(self.lock_screen, 
                                              width=15, 
                                              show="*",
                                              exportselection="False", 
                                              justify="center")
        self.unlock_button = tk.Button(self.lock_screen, 
                                       text="Unlock", 
                                       command=self.unlock)
        
        self.lock_screen.pack(fill="both", expand="1")
        self.password_request.pack()
        self.unlock_password_entry.pack()
        self.unlock_button.pack()
        
        # Disable all non-unlock widgets, including menus and banners.
        self.root.config(menu=self.dummy_menu)
        self.root.bind("<Button-3>", "")
        self.lock_screen.lift(aboveThis=None)
        self.unlock_password_entry.bind("<Return>", self.unlock)
        self.unlock_password_entry.focus_force()
        
        self.lock_screen.mainloop()


    def lock_tab_mode(self, event=None):
         # Best way of doing this is probably either:
         # disable the other tabs and do exactly what lock does with 
         # the current one, OR
         # create a new frame so that the tabs can remain active, but
         # can't be seen or clicked on - saves everything breaking 
         # when tabs are disabled/re-enabled, but might look weird
         # Locks all tabs - requires the logged in user's 
         # password to unlock.
        jt.LOCKED = True
        self.master.lock(self)
        current_tab = self.get_active_tab()
        current_tab[1].config(state="disabled")
        for tab, tab_structure in self.tab_set.items():
            tab_structure[1].config(state="disabled")
            tab_structure[0].pack_forget()
            tab_structure[3].bind("<Button-1>", "")
        self.tab_labels_frame.pack_forget()
        if self.repack_queue[self.vertscroll_banner][0]:
            self.vertscroll_banner.pack_forget()
        if self.repack_queue[self.back_banner_canvas][0]:
            self.back_banner_canvas.pack_forget()
            
        self.lock_screen = tk.Frame(self.root)
        
        # Create the password request widgets.
        self.password_request = tk.Label(self.lock_screen, 
                                         text="Enter your password to "
                                         "unlock the document: ")
        self.unlock_password_entry = tk.Entry(self.lock_screen, 
                                              width=15, 
                                              show="*",
                                              exportselection="False", 
                                              justify="center")
        self.unlock_button = tk.Button(self.lock_screen, 
                                       text="Unlock", 
                                       command=self.unlock_tab_mode)
        
        self.lock_screen.pack(fill="both", expand="1")
        self.password_request.pack()
        self.unlock_password_entry.pack()
        self.unlock_button.pack()
        
        # Disable all non-unlock widgets, including menus and banners.
        self.root.config(menu=self.dummy_menu)
        self.root.bind("<Button-3>", "")
        self.lock_screen.lift(aboveThis=None)
        self.unlock_password_entry.bind("<Return>", self.unlock_tab_mode)
        self.unlock_password_entry.focus_force()
        
        self.lock_screen.mainloop()
        
        return None


    def unlock(self, event=None, _external=False):
        """Unlock method associated with the Lock method"""

        def unlock_window():
            self.lock_screen.destroy()
            try:
                if self.repack_queue[self.vertscroll_banner][0]:
                    self.vertscroll_banner.pack(side="right",
                                                fill="y",
                                                in_=self.root)
                if self.repack_queue[self.back_banner_canvas][0]:
                    self.back_banner_canvas.pack(anchor="n",
                                                 side="right",
                                                 fill="both",
                                                 expand=1)
                self.text_frame.pack(anchor="e",
                                     side="top",
                                     fill="both",
                                     expand="1")
                self.root.config(menu=self.menu_bar)
                self.root.bind("<Button-3>", self.show_context_menu)
                self.text_entry.config(state="normal")
            except tk.TclError:
                pass  # TODO: Create proper Exception for this.
            else:
                if self.master.locked_frame.winfo_manager():
                    jt.LOCKED = False
                    self.master.unlock()
                    return None
                else:
                    return None
        user_password = jtlcd.lcd[self.username][0]
        if _external:
            unlock_window()
            return None
        elif self.hashcheck(self.unlock_password_entry.get(), 
                            jtlcd.lcd[self.username][1]) == user_password:
            unlock_window()
            return None
        else:
            tkmb.showinfo("Authentication Failure", "The password entered "
                          "was not correct.  Feel free to try again.  "
                          "Alternatively, you could try only accessing your "
                          "own documents in future.")
            with open("loglogginglogins.txt", "a+") as file:
                file.write("File unlock failed for user: " + 
                           self.username + 
                           " : Password entered: " + 
                           self.unlock_password_entry.get() + 
                           "\n")        
            self.unlock_password_entry.delete(0, "end")
            return None


    def unlock_tab_mode(self, event=None, _external=False):
        """Unlock method associated with the Lock method, for tab mode"""

        def unlock_tabs():
            self.lock_screen.destroy()
            try:
                if self.repack_queue[self.vertscroll_banner][0]:
                    self.vertscroll_banner.pack(side="right",
                                                fill="y",
                                                in_=self.root)
                if self.repack_queue[self.back_banner_canvas][0]:
                    self.back_banner_canvas.pack(anchor="n",
                                                 side="right",
                                                 fill="both",
                                                 expand=1)
                self.tab_labels_frame.pack(side="top", fill="x")
                current_tab = self.get_active_tab()
                for tab, tab_structure in self.tab_set.items():
                    tab_structure[1].config(state="normal")
                    tab_structure[0].pack(anchor="n", 
                                          side="top", 
                                          fill="both", 
                                          expand=1)
                    tab_structure[3].bind("<Button-1>", self.change_tab)
                self.root.config(menu=self.menu_bar)
                self.root.bind("<Button-3>", self.show_context_menu)
                self._repack()
                current_tab[1].config(state="normal")
            except tk.TclError:
                pass  # TODO: Create proper Exception for this.
            else:
                if self.master.locked_frame.winfo_manager():
                    jt.LOCKED = False
                    self.master.unlock()
                    return None
                else:
                    return None
        user_password = jtlcd.lcd[self.username][0]
        if _external:
            unlock_tabs()
            return None
        elif self.hashcheck(self.unlock_password_entry.get(), 
                            jtlcd.lcd[self.username][1]) == user_password:
            unlock_tabs()
            return None
        else:
            tkmb.showinfo("Authentication Failure", "The password entered "
                          "was not correct.  Feel free to try again.  "
                          "Alternatively, you could try only accessing your "
                          "own documents in future.")
            with open("loglogginglogins.txt", "a+") as file:
                file.write("File unlock failed for user: " + 
                           self.username + 
                           " : Password entered: " + 
                           self.unlock_password_entry.get() + 
                           "\n")        
            self.unlock_password_entry.delete(0, "end")
            return None


    def add_to_whiteboard(self, event=None):
     # Function controlling the key feature of the program - the 
     # Whiteboard.  This is similar to the Windows clipboard but can 
     # contain multiple items, each of which can be accessed separately
     # as and when required.  Checks whether a new item is already in 
     # the Whiteboard or not before addition.
        if self.text_entry.tag_ranges("sel"):
            new_wb_contents = str(self.text_entry.get("sel.first", 
                                                      "sel.last"))
            if new_wb_contents not in self.whiteboard_contents:
                self.whiteboard_contents.append(new_wb_contents)
                new_item_index = self.whiteboard_contents.index\
                                 (new_wb_contents)
                self.whiteboard.add_command(\
                    label=self.whiteboard_contents[new_item_index], 
                    command=lambda:self.paste_from_whiteboard(\
                    self.whiteboard_contents[new_item_index]))
                self.root.update()
                return None
            else:
                return None
        else:
            return None


    def add_to_whiteboard_tab(self, event=None):
     # Function controlling the key feature of the program - the 
     # Whiteboard.  This is similar to the Windows clipboard but can 
     # contain multiple items, each of which can be accessed separately
     # as and when required.  Checks whether a new item is already in 
     # the Whiteboard or not before addition.
        if self.get_active_tab()[1].tag_ranges("sel"):
            new_wb_contents = str(self.get_active_tab()[1].get("sel.first", 
                                                             "sel.last"))
            if new_wb_contents not in self.whiteboard_contents:
                self.whiteboard_contents.append(new_wb_contents)
                new_item_index = self.whiteboard_contents.index\
                                 (new_wb_contents)
                self.whiteboard.add_command(\
                    label=self.whiteboard_contents[new_item_index], 
                    command=lambda:self.paste_from_whiteboard(\
                    self.whiteboard_contents[new_item_index]))
                self.root.update()
                return None
            else:
                return None
        else:
            return None


    def paste_from_whiteboard(self, text):
        if self.window_mode =="windowed":
            self.paste_from_whiteboard_window()
        elif self.window_mode -- "tabbed":
            self.paste_from_whiteboard_tab()
        return None


    def paste_from_whiteboard_window(self, text):
     # Keybound function to paste the last item saved to the Whiteboard
     # into the document at the cursor location,erasing any selected 
     # text.
        if self.text_entry.tag_ranges("sel"):
            self.text_entry.delete("sel.first", "sel.last")
            self.text_entry.insert("insert", text)
            self.text_entry.delete("end-1c", "end")
            return None
        else:
            self.text_entry.insert("insert", text)
            self.text_entry.delete("end-1c", "end")
            return None


    def paste_from_whiteboard_tab(self, text):
     # Keybound function to paste the last item saved to the Whiteboard
     # into the document at the cursor location,erasing any selected 
     # text.
        if self.get_active_tab()[1].tag_ranges("sel"):
            self.get_active_tab()[1].delete("sel.first", "sel.last")
            self.get_active_tab()[1].insert("insert", text)
            self.get_active_tab()[1].delete("end-1c", "end")
            return None
        else:
            self.get_active_tab()[1].insert("insert", text)
            self.get_active_tab()[1].delete("end-1c", "end")
            return None


    def clear_whiteboard(self):
     # Function to clear the Whiteboard - keybound and located in the 
     # Edit Menu.  Deletes all items irreversibly.
        stop = len(self.whiteboard_contents) + 2
        for item in range(stop, 2, -1):
            self.whiteboard.delete(item)
        self.whiteboard_contents = []
        self.root.update()
        return None


    def duplicate(self, event=None):
     # Creates a new window with an identical document - allows for 
     # easy reversal of changes without multiple copies existing of a 
     # document.  Both copies can be saved individually.
        if self.file_name.endswith(".wnx"):
            root_node = ET.Element("file")
            data_node = ET.SubElement(root_node, "data")
            body_node = ET.SubElement(root_node, "body")
            fonts_node = ET.SubElement(data_node, "fonts")
            tags_node = ET.SubElement(data_node, "tags")
            for key in self.custom_fonts_dict:
                font_node = ET.SubElement(fonts_node, "font", name=key)
                config_node = ET.SubElement(font_node, "fontconfig")
                for attr in self.custom_fonts_dict[key].actual():
                    config_node.set(attr,
                              str(self.custom_fonts_dict[key].actual()[attr]))
            for tag in self.text_entry.tag_names():
                if tag == "sel" or tag == "custom_font":
                    continue
                print(tag)
                range = tuple([str(i) for i in self.text_entry.tag_ranges(tag)])
                if range:
                    print(range)
                    print(repr(range[0]))
                else:
                    continue
                tag_node = ET.SubElement(tags_node,
                                         "tag",
                                         name=tag,
                                         range=range)
                if tag in self.custom_fonts_dict:
                    tag_node.set("config", "{font=%s}" % tag)
                elif tag in ["yellow", "orange", "pink", "green"]:
                    tag_node.set('config', "{background=%s}" % tag)
                elif tag in ["left", "center", "right"]:
                    tag_node.set('config', "{justify=%s}" % tag)
                elif tag in ["superscript", "subscript"]:
                    tag_offset = self.text_entry.tag_config(tag)["offset"][4]
                    tag_node.set("config", "{offset=%s}" % tag_offset)
                elif tag.startswith("#"):
                    tag_node.set("config", "{foreground=%s}" % tag)
            body_node.text = self.text_entry.get("1.0", "end-1c")
            tree = ET.ElementTree(root_node)
            tree.write("tmp.wnx",
                       encoding="utf-8",
                       xml_declaration=True,
                       short_empty_elements=False)
            new_app = WN
            new_app.open_WN_file(new_app(username=self.username,
                                         saved=True,
                                         file_name=self.file_name,
                                         window_set=self.window_set,
                                         master=self.master),
                                 "tmp.wnx")
            os.remove("tmp.wnx")
        else:
            copy_contents = self.text_entry.get(1.0, "end-1c")
            tags_to_push = {}
            for tag in self.text_entry.tag_names():
                tags_to_push[tag] = [self.text_entry.tag_ranges(tag),
                                     self.text_entry.tag_config(tag)]
            new_window = WN(self.username,
                            file_contents=copy_contents,
                            saved=self.saved,
                            file_name=self.file_name,
                            window_set=self.window_set,
                            pushed_tags=tags_to_push,
                            custom_fonts=self.custom_fonts_dict,
                            master = self.master)
            return None


    def duplicate_tab(self, event=None):
        tab = self.get_active_tab()
        if tab[8].endswith(".wnx"):
            root_node = ET.Element("file")
            data_node = ET.SubElement(root_node, "data")
            body_node = ET.SubElement(root_node, "body")
            fonts_node = ET.SubElement(data_node, "fonts")
            tags_node = ET.SubElement(data_node, "tags")
            for key in tab[9]:
                font_node = ET.SubElement(fonts_node, "font", name=key)
                config_node = ET.SubElement(font_node, "fontconfig")
                for attr in tab[9][key].actual():
                    config_node.set(attr,
                              str(tab[9][key].actual()[attr]))
            for tag in tab[1].tag_names():
                if tag == "sel" or tag == "custom_font":
                    continue
                print(tag)
                range = tuple([str(i) for i in tab[1].tag_ranges(tag)])
                if range:
                    print(range)
                    print(repr(range[0]))
                else:
                    continue
                tag_node = ET.SubElement(tags_node,
                                         "tag",
                                         name=tag,
                                         range=range)
                if tag in tab[9]:
                    tag_node.set("config", "{font=%s}" % tag)
                elif tag in ["yellow", "orange", "pink", "green"]:
                    tag_node.set('config', "{background=%s}" % tag)
                elif tag in ["left", "center", "right"]:
                    tag_node.set('config', "{justify=%s}" % tag)
                elif tag in ["superscript", "subscript"]:
                    tag_offset = tab[1].tag_config(tag)["offset"][4]
                    tag_node.set("config", "{offset=%s}" % tag_offset)
                elif tag.startswith("#"):
                    tag_node.set("config", "{foreground=%s}" % tag)
            body_node.text = tab[1].get("1.0", "end-1c")
            tree = ET.ElementTree(root_node)
            tree.write("tmp.wnx",
                       encoding="utf-8",
                       xml_declaration=True,
                       short_empty_elements=False)
            new_tab = self.create_new_tab()
            self.open_WN_file_tab("tmp.wnx")
            new_tab[4] = tab[4]
            new_tab[5] = tab[5]
            new_tab[6] = tab[6]
            new_tab[7] = tab[7]
            new_tab[8] = tab[8]
            new_tab[9] = tab[9]
            new_tab[10] = tab[10]
            new_tab[11] = tab[11]
            new_tab[12] = tab[12]
            new_tab[13] = tab[13]
            new_tab[14] = tab[14]
            os.remove("tmp.wnx")
        else:
            copy_contents = tab[1].get(1.0, "end-1c")
            tags_to_push = {}
            for tag in tab[1].tag_names():
                tags_to_push[tag] = [tab[1].tag_ranges(tag),
                                     tab[1].tag_config(tag)]
            new_tab = self.create_new_tab()
            new_tab[1].insert(1.0, copy_contents)
            new_tab[4] = tab[4]
            new_tab[5] = tab[5]
            new_tab[6] = tab[6]
            new_tab[7] = tab[7]
            new_tab[8] = tab[8]
            new_tab[9] = tab[9]
            new_tab[10] = tab[10]
            new_tab[11] = tab[11]
            new_tab[12] = tab[12]
            new_tab[13] = tab[13]
            new_tab[14] = tab[14]
        self.root.update()    
        return None


    def select_all(self, event=None):
     # Selects all text in the widget, highlighting it.
        if event:
            self.text_entry.tag_add("sel", "1.0", "end-1c")
            return 'break'
        else:
            self.text_entry.tag_add("sel", "1.0", "end-1c")
        return None


    def select_all_tab(self, event=None):
     # Selects all text in the widget, highlighting it.
        if event:
            self.get_active_tab()[1].tag_add("sel", "1.0", "end-1c")
            return 'break'
        else:
            self.get_active_tab()[1].tag_add("sel", "1.0", "end-1c")
        return None


    def highlight(self, event=None, colour=None):
        if not colour:
            colour = self.highlight_colour.get()
        else:
            self.highlight_colour.set(colour)
            self.edit_banner_canvas.tag_raise(colour)
            self.root.update()
        hl_colour = self.highlight_colour.get()
        try:
            self.text_entry.tag_add(hl_colour, "sel.first", "sel.last")
        except tk.TclError:
            raise TextNotSelectedError("Select text to highlight first.")
        else:
            self.text_entry.tag_raise("sel")
            self.text_entry.tag_remove("sel", "sel.first", "sel.last")
            self.text_entry.tag_configure(hl_colour, 
                                          background=hl_colour)
            self.root.update()
            self.non_font_tags[hl_colour] = \
                self.text_entry.tag_ranges(hl_colour)
        finally:
            return None


    def highlight_tab(self, event=None, colour=None):
        if not colour:
            colour = self.highlight_colour.get()
        else:
            self.highlight_colour.set(colour)
            self.edit_banner_canvas.tag_raise(colour)
            self.root.update()
        hl_colour = self.highlight_colour.get()
        try:
            self.get_active_tab()[1].tag_add(hl_colour, 
                                           "sel.first", 
                                           "sel.last")
        except tk.TclError:
            raise TextNotSelectedError("Select text to highlight first.")
        else:
            self.get_active_tab()[1].tag_raise("sel")
            self.get_active_tab()[1].tag_remove("sel", 
                                                "sel.first", 
                                                "sel.last")
            self.get_active_tab()[1].tag_configure(hl_colour, 
                                                 background=hl_colour)
            self.root.update()
            self.non_font_tags[hl_colour] = \
                self.get_active_tab()[1].tag_ranges(hl_colour)
        finally:
            return None
        

    def remove_highlight(self):
        for tag in self.text_entry.tag_names():
            if tag in ["yellow", "orange", "green", "pink"]:
                if self.text_entry.tag_ranges("sel"):
                    self.text_entry.tag_remove(tag, "sel.first", "sel.last")
                else:
                    self.text_entry.tag_remove(tag, "1.0", "end")
            else:
                continue
        return None


    def remove_highlight_tab(self):
        for tag in self.get_active_tab()[1].tag_names():
            if tag in ["yellow", "orange", "green", "pink"]:
                if self.get_active_tab()[1].tag_ranges("sel"):
                    self.get_active_tab()[1].tag_remove(tag, 
                                                      "sel.first", 
                                                      "sel.last")
                else:
                    self.get_active_tab()[1].tag_remove(tag, "1.0", "end")
            else:
                continue
        return None


    def change_text_colour(self, event=None):
        if event:
            return self.text_colour_change(self.text_colour)
        else:
            new_colour=tkcc.askcolor(self.text_colour,
                                     title="Text Colour",
                                     parent=self.root)
            if new_colour is (None, None):
                return None
            else:
                return self.text_colour_change(new_colour[1])


    def change_text_colour_tab(self, event=None):
        if event:
            return self.text_colour_change_tab(self.text_colour)
        else:
            new_colour=tkcc.askcolor(self.text_colour,
                                     title="Text Colour",
                                     parent=self.root)
            if new_colour is (None, None):
                return None
            else:
                return self.text_colour_change_tab(new_colour[1])


    def text_colour_change(self, new_colour):
        self.text_colour = new_colour
        if self.text_entry.tag_ranges("sel"):
            self.text_entry.tag_add(self.text_colour,
                                    "sel.first",
                                    "sel.last")
            self.text_entry.tag_raise(self.text_colour)
            self.text_entry.tag_config(self.text_colour,
                                       foreground=self.text_colour)
            self.text_colour_tags[self.text_colour] = \
                self.text_entry.tag_ranges(self.text_colour)
        else:
            for key in self.text_colour_tags:
                self.text_entry.tag_remove(key, "1.0", "end")
            self.text_entry.config(foreground=self.text_colour)
            self.text_colour_tags = {}
        self.style_banner_canvas.itemconfig("text_colour",
                                            fill=self.text_colour)
        return None


    def text_colour_change_tab(self, new_colour):
        self.text_colour = new_colour
        if self.get_active_tab()[1].tag_ranges("sel"):
            self.get_active_tab()[1].tag_add(self.text_colour,
                                           "sel.first",
                                           "sel.last")
            self.get_active_tab()[1].tag_raise(self.text_colour)
            self.get_active_tab()[1].tag_config(self.text_colour,
                                              foreground=self.text_colour)
            self.text_colour_tags[self.text_colour] = \
                self.get_active_tab()[1].tag_ranges(self.text_colour)
        else:
            for key in self.text_colour_tags:
                self.get_active_tab()[1].tag_remove(key, "1.0", "end")
            self.get_active_tab()[1].config(foreground=self.text_colour)
            self.text_colour_tags = {}
        self.style_banner_canvas.itemconfig("text_colour",
                                            fill=self.text_colour)
        return None

    
    def copy(self, event=None):
     # Identical to Windows 'Copy' function - ensures identical function
     # cross-platform.
        if self.text_entry.tag_ranges("sel"):
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text_entry.get("sel.first", 
                                                               "sel.last"))
                return "break"
            except tk.TclError:
                return None
        else:
            return None


    def copy_tab(self, event=None):
     # Identical to Windows 'Copy' function - ensures identical function
     # cross-platform.
        if self.get_active_tab()[1].tag_ranges("sel"):
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.get_active_tab()[1].get\
                    ("sel.first", "sel.last"))
                return "break"
            except tk.TclError:
                return None
        else:
            return None


    def undo(self, event=None):
     # Provides event handling for 'undo' option in menus.
        try:
            self.text_entry.edit_undo()
        except tk.TclError:
            return None
        else:
            return "break"


    def undo_tab(self, event=None):
     # Provides event handling for 'undo' option in menus.
        try:
            self.get_active_tab()[1].edit_undo()
        except tk.TclError:
            return None
        else:
            return "break"


    def redo(self, event=None):
     # Provides event handling for 'redo' option in menus.
        try:
            self.text_entry.edit_redo()
        except tk.TclError:
            return None
        else:
            return "break"


    def redo_tab(self, event=None):
     # Provides event handling for 'redo' option in menus.
        try:
            self.get_active_tab()[1].edit_redo()
        except tk.TclError:
            return None
        else:
            return "break"


    def cut(self, event=None):
     # Identical to Windows 'Cut' function - ensures identical function
     # cross-platform.
        if self.text_entry.tag_ranges("sel"):
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.text_entry.get("sel.first", 
                                                               "sel.last"))
                self.text_entry.delete("sel.first", "sel.last")
            except tk.TclError:
                return None
            else:
                return "break"
        else:
            return None


    def cut_tab(self, event=None):
     # Identical to Windows 'Cut' function - ensures identical function
     # cross-platform.
        if self.get_active_tab()[1].tag_ranges("sel"):
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.get_active_tab()[1].get\
                    ("sel.first", "sel.last"))
                self.get_active_tab()[1].delete("sel.first", "sel.last")
            except tk.TclError:
                return None
            else:
                return "break"
        else:
            return None


    def paste(self, event=None):
     # Identical to Windows 'Paste' function - ensures identical function
     # cross-platform.
        try:
            if self.text_entry.tag_ranges("sel"):
                self.text_entry.delete("sel.first", "sel.last")
                self.text_entry.insert("insert", 
                                       self.root.selection_get\
                                       (selection="CLIPBOARD"))
                return "break"
            else:
                self.text_entry.insert("insert", 
                                       self.root.selection_get\
                                       (selection="CLIPBOARD"))
                self.text_entry.delete("end-1c", "end")
                return "break"
        except tk.TclError:
            return None


    def paste_tab(self, event=None):
     # Identical to Windows 'Paste' function - ensures identical function
     # cross-platform.
        try:
            if self.get_active_tab()[1].tag_ranges("sel"):
                self.get_active_tab()[1].delete("sel.first", "sel.last")
                self.get_active_tab()[1].insert("insert", 
                                              self.root.selection_get\
                                              (selection="CLIPBOARD"))
                return "break"
            else:
                self.get_active_tab()[1].insert("insert", 
                                              self.root.selection_get\
                                              (selection="CLIPBOARD"))
                self.get_active_tab()[1].delete("end-1c", "end")
                return "break"
        except tk.TclError:
            return None


    def mainmenu(self, event=None):
     # Returns to the Main Menu, closing all currently opened windows.
     # Restores the minimised launcher window.
        if tkmb.askyesno("Warning!", 
                         "If you continue, any unsaved changes to this or "
                         "any other open WordNote window will be lost.  "
                         "Please ensure you have saved any work which you "
                         "wish to keep before continuing.  Would you like "
                         "to continue closing all WordNote windows?", 
                         icon="warning"):
            for key, value in self.window_set.items():
                self.window_set[key].root.destroy()
            self.window_set = {}
            self.master.root.deiconify()
            return True
        else:
            return False


    def mainmenu_tab(self, event=None):
     # Returns to the Main Menu, closing all currently opened windows.
     # Restores the minimised launcher window.
        if tkmb.askyesno("Warning!", 
                         "If you continue, any unsaved changes to this or "
                         "any other open WordNote window will be lost.  "
                         "Please ensure you have saved any work which you "
                         "wish to keep before continuing.  Would you like "
                         "to continue closing all WordNote windows?", 
                         icon="warning"):
            self.master.root.deiconify()
            self.root.destroy()
            return True
        else:
            return False


    def close(self, event=None):
     # Closes a single instance of the App.  Restores the minimised 
     # launcher window if there are no other WN App instances.
        if not self._validate():
            if tkmb.askyesno("Warning", 
                             "If you continue, changes to the current file "
                             "will be lost.  Would you like to save changes "
                             "before continuing?", 
                             icon="warning"):
                self.save_file()
        self.root.destroy()
        try:
            del self.window_set[self.count]
        except KeyError:
            pass # Expected errors caused by previous deletions ignored
        if self.window_set == {}:
            self.master.root.deiconify()
            return None
        else:
            return None


    def close_others(self, event=None):
        for key in self.window_set:
            if key is not self.count:
                if self.window_set[key]._validate():
                    self.window_set[key].root.destroy()
                else:
                    self.window_set[key].text_entry.focus_set()
                    if tkmb.askyesno("Warning", 
                             "One of the windows being closed has unsaved "
                             "changes.  Would you like to save changes "
                             "before continuing?", 
                             icon="warning"):
                        self.window_set[key].save_file()
                    else:
                        self.window_set[key].root.destroy()
            else:
                continue
        self.window_set = {}
        self.window_set[self.count] = self
        return None
            

    def exit(self, event=None):
     # Exits the program, calling the top-level widgets 'exit' function
     # to force-close all App windows.
        if self.mainmenu():
            jt.sys.exit()
            return None
        else:
            return None


    def find(self, event=None):
     # Creates instance of 'Find' dialogue
        self.find_dialogue = TextSearch(self)
        return None


    def search_text(self, search_text, search_index="1.0"):
     # Searches for text from the text_search object, adding it to the 
     # "sel" tag and re-focusing on the main window.  "Find" dialogue 
     # remains open.
        start = self.text_entry.search(search_text, 
                                       search_index)
        end = "".join([start, "+", str(len(search_text)), "c"])
        self.text_entry.focus_force()
        try:
            self.text_entry.see(start)
        except tk.TclError:
            raise TextNotFoundError
            self.find_dialogue.root.destroy()
            self.find_dialogue = TextSearch(self)
            self.find_dialogue.search_field.insert("end", search_text)
        else:
            self.text_entry.tag_remove("sel", 1.0, "end")
            self.text_entry.tag_add("sel", start, end)
            self.last_search_result = self.text_entry.tag_ranges("sel")
            return self.last_search_result
        finally:
            return None


    def search_text_tab(self, search_text, search_index="1.0"):
     # Searches for text from the text_search object, adding it to the 
     # "sel" tag and re-focusing on the main window.  "Find" dialogue 
     # remains open.
        start = self.get_active_tab()[1].search(search_text, 
                                                search_index)
        end = "".join([start, "+", str(len(search_text)), "c"])
        self.get_active_tab()[1].focus_force()
        try:
            self.get_active_tab()[1].see(start)
        except tk.TclError:
            raise TextNotFoundError
            self.find_dialogue.root.destroy()
            self.find_dialogue = TextSearch(self)
            self.find_dialogue.search_field.insert("end", search_text)
        else:
            self.get_active_tab()[1].tag_remove("sel", 1.0, "end")
            self.get_active_tab()[1].tag_add("sel", start, end)
            self.last_search_result = self.get_active_tab()[1].tag_ranges\
                ("sel")
            return self.last_search_result
        finally:
            return None


    def replace(self, event=None):
     # Creates instance of 'Replace' dialogue
        self.replace_dialogue = TextReplace(self)
        return None


    def replace_text(self, search_text, replacement_text, search_index="1.0"):
     # Searches for text, and replaces with text, from the TextReplace 
     # object, then re-focuses on the main window. "Find and Replace" 
     # dialogue remains open.
        search_start = self.text_entry.search(search_text, 
                                              search_index)
        search_end = "".join([search_start, "+", str(len(search_text)), "c"])
        self.text_entry.focus_force()
        try:
            self.text_entry.see(search_start)
        except tk.TclError:
            raise TextNotFoundError
            self.replace_dialogue.root.destroy()
            self.replace_dialogue = TextReplace(self)
            self.replace_dialogue.search_field.insert("end", search_text)
            self.replace_dialogue.replace_field.insert("end",
                                                       replacement_text)
        else:
            if self.text_entry.tag_ranges("sel"):
                    self.text_entry.tag_remove("sel", 1.0, "end")
            self.text_entry.delete(search_start, search_end)
            self.text_entry.insert(search_start, replacement_text)
            replace_start = search_start
            replace_end = "".join([replace_start,
                                   "+",
                                   str(len(replacement_text)),
                                   "c"])
            self.text_entry.tag_add("sel", replace_start, replace_end)
            self.last_search_result = self.text_entry.tag_ranges("sel")
            self.last_replacement_text = replacement_text
            return self.last_replacement_text_result
        finally:
            return None


    def replace_text_tab(self, 
                         search_text, 
                         replacement_text, 
                         search_index="1.0"):
     # Searches for text, and replaces with text, from the TextReplace 
     # object, then re-focuses on the main window. "Find and Replace" 
     # dialogue remains open.
        search_start = self.get_active_tab()[1].search(search_text, 
                                                       search_index)
        search_end = "".join([search_start, "+", str(len(search_text)), "c"])
        self.get_active_tab()[1].focus_force()
        try:
            self.get_active_tab()[1].see(search_start)
        except tk.TclError:
            raise TextNotFoundError
            self.replace_dialogue.root.destroy()
            self.replace_dialogue = TextReplace(self)
            self.replace_dialogue.search_field.insert("end", search_text)
            self.replace_dialogue.replace_field.insert("end",
                                                       replacement_text)
        else:
            if self.get_active_tab()[1].tag_ranges("sel"):
                self.get_active_tab()[1].tag_remove("sel", 1.0, "end")
            self.get_active_tab()[1].delete(search_start, search_end)
            self.get_active_tab()[1].insert(search_start, replacement_text)
            replace_start = search_start
            replace_end = "".join([replace_start,
                                   "+",
                                   str(len(replacement_text)),
                                   "c"])
            self.get_active_tab()[1].tag_add("sel", 
                                           replace_start, 
                                           replace_end)
            self.last_search_result = self.get_active_tab()[1].tag_ranges\
                    ("sel")
            self.last_replacement_text = replacement_text
            return self.last_replacement_text_result
        finally:
            return None
            

    def font_size_change(self, new_size):
        self.font_change({"size" : new_size}, offset=None)
        return None


    def font_size_change_tab(self, new_size):
        self.font_change_tab({"size" : new_size}, offset=None)
        return None


    def font_change(self, new_font, offset=None):
        def change(font, new_font):
            for key in new_font:
                try:
                    if key is "strikethrough_change":
                        if new_font[key]:
                            font["overstrike"] = new_font["overstrike"]
                    elif key is "underline_change":
                        if new_font[key]:
                            font["underline"] = new_font["underline"]
                    else:
                        if new_font[key]:
                            font[key] = new_font[key]
                except KeyError:
                    continue
            else:
                return font
        if self.text_entry.tag_ranges("sel"):
            sel_length = len(self.text_entry.get("sel.first", "sel.last"))
            for i in range(sel_length):
                start_index = "sel.first+" + str(i) + "c"
                stop_index = "sel.first+" + str(i+1) + "c"
                for tag in self.text_entry.tag_names(start_index):
                    if tag not in self.non_font_tags and tag not in \
                            self.text_colour_tags:
                        font = self.custom_fonts_dict[tag].copy()
                        self.custom_fonts_dict[font.name] = font.copy()
                        self.text_entry.tag_remove(tag,
                                                   start_index,
                                                   stop_index)
                        self.text_entry.tag_add(font.name,
                                                start_index,
                                                stop_index)
                        self.text_entry.tag_raise(font.name)
                        changed_font = change(font, new_font)
                        self.text_entry.tag_config(font.name, 
                                                   font=changed_font)
                        self.custom_fonts_dict[font.name] = changed_font.copy()
                        break
                    else:
                        continue
                else:
                    font = self.custom_fonts_dict["custom_font"].copy()
                    self.custom_fonts_dict[font.name] = font.copy()
                    self.text_entry.tag_add(font.name,
                                            start_index,
                                            stop_index)
                    self.text_entry.tag_raise(font.name)
                    changed_font = change(font, new_font)
                    self.text_entry.tag_config(font.name,
                                               font=changed_font)
                    self.custom_fonts_dict[font.name] = changed_font.copy()
            if offset is not None:
                self.text_entry.tag_remove("superscript",
                                           "sel.first",
                                           "sel.last")
                self.text_entry.tag_remove("subscript",
                                           "sel.first",
                                           "sel.last")
                if offset == 20:
                    self.text_entry.tag_add("superscript",
                                            "sel.first",
                                            "sel.last")
                    self.text_entry.tag_config("superscript", offset=offset)
                elif offset == -20:
                    self.text_entry.tag_add("subscript",
                                            "sel.first",
                                            "sel.last")
                    self.text_entry.tag_config("subscript", offset=offset)
                else:
                    return None
            else:
                return None
        else:
        # Changes only the following text.
        # Changing all text is accomplished by highlighting all text.
            self.custom_font = change(self.custom_font, new_font)
            changed_font = self.custom_font.copy()
            self.text_entry.tag_add(changed_font.name, "end-1c", "end")
            self.text_entry.tag_config(changed_font.name, font=changed_font)
            self.custom_fonts_dict[changed_font.name] = changed_font.copy()
            self.text_entry.tag_lower(changed_font.name)
            self.custom_fonts_dict["custom_font"] = self.custom_font.copy()
            if offset is not None:
                self.text_entry.tag_remove("superscript", "end-1c", "end")
                self.text_entry.tag_remove("subscript", "end-1c", "end")
                if offset == 20:
                    self.text_entry.tag_add("superscript", "end-1c", "end")
                    self.text_entry.tag_config("superscript", offset=offset)
                elif offset == -20:
                    self.text_entry.tag_add("subscript", "end-1c", "end")
                    self.text_entry.tag_config("subscript", offset=offset)
                else:
                    return None
            else:
                return None


    def font_change_tab(self, new_font, offset=None):
        def change(font, new_font):
            for key in new_font:
                try:
                    if key is "strikethrough_change":
                        if new_font[key]:
                            font["overstrike"] = new_font["overstrike"]
                    elif key is "underline_change":
                        if new_font[key]:
                            font["underline"] = new_font["underline"]
                    else:
                        if new_font[key]:
                            font[key] = new_font[key]
                except KeyError:
                    continue
            else:
                return font
        if self.get_active_tab()[1].tag_ranges("sel"):
            sel_length = len(self.get_active_tab()[1].get("sel.first", 
                                                        "sel.last"))
            for i in range(sel_length):
                start_index = "sel.first+" + str(i) + "c"
                stop_index = "sel.first+" + str(i+1) + "c"
                for tag in self.get_active_tab()[1].tag_names(start_index):
                    if tag not in self.non_font_tags and tag not in \
                            self.text_colour_tags:
                        font = self.custom_fonts_dict[tag].copy()
                        self.custom_fonts_dict[font.name] = font.copy()
                        self.get_active_tab()[1].tag_remove(tag,
                                                          start_index,
                                                          stop_index)
                        self.get_active_tab()[1].tag_add(font.name,
                                                       start_index,
                                                       stop_index)
                        self.get_active_tab()[1].tag_raise(font.name)
                        changed_font = change(font, new_font)
                        self.get_active_tab()[1].tag_config(font.name, 
                                                          font=changed_font)
                        self.custom_fonts_dict[font.name] = \
                                changed_font.copy()
                        break
                    else:
                        continue
                else:
                    font = self.custom_fonts_dict["custom_font"].copy()
                    self.custom_fonts_dict[font.name] = font.copy()
                    self.get_active_tab()[1].tag_add(font.name,
                                                     start_index,
                                                     stop_index)
                    self.get_active_tab()[1].tag_raise(font.name)
                    changed_font = change(font, new_font)
                    self.get_active_tab()[1].tag_config(font.name,
                                                        font=changed_font)
                    self.custom_fonts_dict[font.name] = changed_font.copy()
            if offset is not None:
                self.get_active_tab()[1].tag_remove("superscript",
                                                    "sel.first",
                                                    "sel.last")
                self.get_active_tab()[1].tag_remove("subscript",
                                                    "sel.first",
                                                    "sel.last")
                if offset == 20:
                    self.get_active_tab()[1].tag_add("superscript",
                                                     "sel.first",
                                                     "sel.last")
                    self.get_active_tab()[1].tag_config("superscript", 
                                                        offset=offset)
                elif offset == -20:
                    self.get_active_tab()[1].tag_add("subscript",
                                                     "sel.first",
                                                     "sel.last")
                    self.get_active_tab()[1].tag_config("subscript", 
                                                        offset=offset)
                else:
                    return None
            else:
                return None
        else:
        # Changes only the following text.
        # Changing all text is accomplished by highlighting all text.
            self.custom_font = change(self.custom_font, new_font)
            changed_font = self.custom_font.copy()
            self.get_active_tab()[1].tag_add(changed_font.name, 
                                             "end-1c", 
                                             "end")
            self.get_active_tab()[1].tag_config(changed_font.name, 
                                                font=changed_font)
            self.custom_fonts_dict[changed_font.name] = changed_font.copy()
            self.get_active_tab()[1].tag_lower(changed_font.name)
            self.custom_fonts_dict["custom_font"] = self.custom_font.copy()
            if offset is not None:
                self.get_active_tab()[1].tag_remove("superscript", 
                                                    "end-1c", 
                                                    "end")
                self.get_active_tab()[1].tag_remove("subscript", 
                                                    "end-1c", 
                                                    "end")
                if offset == 20:
                    self.get_active_tab()[1].tag_add("superscript", 
                                                     "end-1c", 
                                                     "end")
                    self.get_active_tab()[1].tag_config("superscript", 
                                                        offset=offset)
                elif offset == -20:
                    self.get_active_tab()[1].tag_add("subscript", 
                                                     "end-1c", 
                                                     "end")
                    self.get_active_tab()[1].tag_config("subscript", 
                                                        offset=offset)
                else:
                    return None
            else:
                return None


    def style_canvas_font_toggle(self, event=None):
        clicked_item = self.style_banner_canvas.find_withtag("current")
        if "bold" in self.style_banner_canvas.gettags(clicked_item):
            self.font_change({"weight":"bold"} if event.num == 1 \
                else {"weight":"normal"})
        elif "italic" in self.style_banner_canvas.gettags(clicked_item):
            self.font_change({"slant":"italic"} if event.num == 1 \
                else {"slant":"roman"})
        elif "underline" in self.style_banner_canvas.gettags(clicked_item):
            self.font_change({"underline":"1"} if event.num is 1 \
                else {"underline":"0"})
        elif "strikethrough" in self.style_banner_canvas.gettags(clicked_item):
            self.font_change({"overstrike":"1"} if event.num is 1 \
                else {"overstrike":"0"})
        else:
            pass
        return None


    def layout_options(self):
        LayoutDialogue(self)
        return None


    def layout_changes(self, justification=None):
        if justification is not None:
            if self.text_entry.tag_ranges("sel"):
                self.text_entry.tag_add(justification, 
                                        "sel.first", 
                                        "sel.last")
                self.text_entry.tag_config(justification,
                                           justify=justification)
                self.text_entry.tag_remove("sel", "sel.first", "sel.last")
                self.non_font_tags[justification] = \
                    self.text_entry.tag_ranges(justification)
            else:
                for tag in self.text_entry.tag_names():
                    if tag in ["left", "center", "right"]:
                        self.text_entry.tag_remove(tag, "1.0", "end")
                self.text_entry.tag_add(justification, "1.0", "end")
                self.text_entry.tag_config(justification, 
                                           justify=justification)
                self.non_font_tags[justification] = \
                    self.text_entry.tag_ranges(justification)
            return None
        else:
            return None


    def layout_changes_tab(self, justification=None):
        if justification is not None:
            if self.get_active_tab()[1].tag_ranges("sel"):
                self.get_active_tab()[1].tag_add(justification, 
                                                 "sel.first", 
                                                 "sel.last")
                self.get_active_tab()[1].tag_config(justification,
                                                    justify=justification)
                self.get_active_tab()[1].tag_remove("sel", 
                                                    "sel.first", 
                                                    "sel.last")
                self.non_font_tags[justification] = \
                    self.get_active_tab()[1].tag_ranges(justification)
            else:
                for tag in self.get_active_tab()[1].tag_names():
                    if tag in ["left", "center", "right"]:
                        self.get_active_tab()[1].tag_remove(tag, "1.0", "end")
                self.get_active_tab()[1].tag_add(justification, "1.0", "end")
                self.get_active_tab()[1].tag_config(justification, 
                                           justify=justification)
                self.non_font_tags[justification] = \
                    self.get_active_tab()[1].tag_ranges(justification)
            return None
        else:
            return None


    def fix_text(self, text_entry, event=None):
        text_entry.delete(1.0, "end")
        text_entry.insert("end", 
                          "It was the best of times, it was the blurst of "
                          "times.  ")
        text_entry.config(maxundo=0, undo=0)
        return None


    def fix_text_tab(self, text_entry, event=None):
        get_active_tab()[1].delete(1.0, "end")
        get_active_tab()[1].insert("end", 
                                  "It was the best of times, it was the "
                                  "blurst of times.  ")
        get_active_tab()[1].config(maxundo=0, undo=0)
        return None


    def view_change(self, mode, event=None):
     # Changes between several view modes, based on system-generated 
     # text input.  Standard mode is a small, centralised window.  
     # Left-panel mode appears on the left side of the screen, modelled
     # after the Windows 8 app left-side attachment.  Right-panel mode 
     # is the same as left-panel mode, but on the right-hand side of 
     # the screen.  Fullscreen mode uses the built-in "fullscreen" 
     # attribute to remove the title bar from the window and force it 
     # to take up the entire screen.  All modes use sizes calculated 
     # from derived screen size, so should function identically on all 
     # devices that can run the App.
        self.back_banner_canvas.pack_forget()
        if mode == "standard":
            if self.view_mode != "standard":
                try:
                    self.new_window_pos = "".join(["401x451",
                                                   self.new_window_pos[7::]])
                except AttributeError:
                    self.new_window_pos = "401x451+%s+%s" % (self.x_pos,
                                                             self.y_pos)
            self.root.attributes("-fullscreen", False)
            self.root.update()
            try:
                if self.new_window_pos[:7:] is "401x451":
                    self.root.geometry(self.new_window_pos)
                else:
                    self.new_window_pos = "".join(["401x451",
                                                   self.new_window_pos[7::]])
                    self.root.geometry(self.new_window_pos)
            except AttributeError:
                self.root.geometry(self.window_size)
        elif mode == "fullscreen":
            self.root.attributes("-fullscreen", True)
            self.root.update()
            if self.img_canvas:
                self.img_canvas.destroy()
        elif mode == "left panel":
            self.root.attributes("-fullscreen", False)
            self.root.update()
            window_dimensions = "x".join([str(int(self.screen_x / 2)),
                                          str(int(self.screen_y))])
            self.left_panel = "+".join([window_dimensions, 
                                        "0",
                                        "0"])
            self.root.geometry(self.left_panel)
            if self.img_canvas:
                self.img_canvas.destroy()
        elif mode == "right panel":
            self.root.attributes("-fullscreen", False)
            self.root.update()
            window_dimensions = "x".join([str(int(self.screen_x / 2)),
                                          str(int(self.screen_y))])
            self.right_panel = "+".join([window_dimensions,
                                         str(int(self.screen_x / 2) - 2), 
                                         "0"])
            self.root.geometry(self.right_panel)
            if self.img_canvas:
                self.img_canvas.destroy()
        self.view_mode = mode
        self.back_banner_canvas.pack(anchor="n",
                                     side="right",
                                     fill="both")
        self.banner_expand()
        self.banner_collapse()
        self.root.update()
        try:
            text = self.find_dialogue.search_field.get()
        except (AttributeError, tk.TclError):
            pass # Because all that means is that there is no 'Find' dialogue
        else:
            self.find_dialogue.root.destroy()
            self.find_dialogue = TextSearch(self)
            self.find_dialogue.search_field.insert("insert", string=text)
        try:
            text = self.replace_dialogue.search_field.get()
        except (AttributeError, tk.TclError):
            return None # or 'Replace' dialogue
        else:
            self.replace_dialogue.root.destroy()
            self.replace_dialogue = TextReplace(self)
            self.replace_dialogue.search_field.insert("insert", string=text)
            return None


    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
        return None


    def show_menu_bar(self):
        self.root.config(menu=self.menu_bar)
        self.root.update()
        return None
 
 
    def show_button_banner(self):
        if self.back_banner_canvas.winfo_ismapped():
            return None
        else:
            self.active_text_frame.pack_forget()
            if self.repack_queue[self.vertscroll_banner][0] is False:
                self.vertscroll_banner.pack(side="right",
                                            fill="y",
                                            in_=self.root)
                self.repack_queue[self.vertscroll_banner][0] = True
            self.back_banner_canvas.pack(anchor="n",
                                         side="right",
                                         fill="both",
                                         expand=1)
            self.repack_queue[self.back_banner_canvas][0] = True
            self.active_text_frame.pack(anchor="e",
                                 side="top",
                                 fill="both",
                                 expand="1")
            return None
 
 
    def hide_menu_bar(self):
        self.root.config(menu=self.dummy_menu)
        self.root.update()
        return None
 
 
    def hide_button_banner(self):
        if self.back_banner_canvas.winfo_ismapped():
            self.repack_queue[self.back_banner_canvas][0] = False
            self.back_banner_canvas.pack_forget()
            if self.repack_queue[self.vertscroll_banner][0]:
                self.repack_queue[self.vertscroll_banner][0] = False
                self.vertscroll_banner.pack_forget()
            return None
        else:
            return None
 
 
    def banner_expand(self, event=None):
        if not (self.file_banner_canvas.winfo_ismapped() or \
                self.edit_banner_canvas.winfo_ismapped() or \
                self.style_banner_canvas.winfo_ismapped()):
            self.active_text_frame.pack_forget()
            self.back_banner_canvas.config(width="52")
            self.file_banner_button.config(image=self.fb_button_image)
            self.edit_banner_button.config(image=self.eb_button_image)
            self.style_banner_button.config(image=self.sb_button_image)
            self.active_text_frame.pack(anchor="e", 
                                 side="top", 
                                 fill="both", 
                                 expand="1")
        self._update_repack_queue()
        self.root.update_idletasks()
        self.root.update()
        return None


    def forced_banner_expansion(self):
        self.active_text_frame.pack_forget()
        self.back_banner_canvas.config(width="52")
        self.file_banner_button.config(image=self.fb_button_image)
        self.edit_banner_button.config(image=self.eb_button_image)
        self.style_banner_button.config(image=self.sb_button_image)
        self.active_text_frame.pack(anchor="e", 
                             side="top", 
                             fill="both", 
                             expand="1")
        self._update_repack_queue()
        self.root.update_idletasks()
        self.root.update()
 
 
    def banner_collapse(self, event=None):
        if not (self.file_banner_canvas.winfo_ismapped() or \
                self.edit_banner_canvas.winfo_ismapped() or \
                self.style_banner_canvas.winfo_ismapped()):
            self.back_banner_canvas.config(width="52")
            self.file_banner_button.config(image="")
            self.edit_banner_button.config(image="")
            self.style_banner_button.config(image="")
        self.root.update_idletasks()
        self.root.update()
        return None


    def fb_rotation(self):
        image = \
            Image.open(\
                "resources\\chevdown.png").resize(\
                    (20, 20)).rotate(self.chev_angle)
        self.fb_button_image = ImageTk.PhotoImage(image)
        return None


    def fc_movement(self, *image_tags):
        banner_frame = self.back_banner_canvas.find_withtag("banner_frame")[0]
        self.back_banner_canvas.itemconfig(banner_frame, 
            height=(int(self.back_banner_canvas.itemcget(banner_frame, 
                                                         "height")) + 
            (self.in_banner_displacement/5)))
        for tag in image_tags:
            self.file_banner_canvas.move(tag, 0, self.in_banner_displacement)
        return None


    def eb_rotation(self):
        image = \
            Image.open(\
                "resources\\chevdown.png").resize(\
                    (20, 20)).rotate(self.chev_angle)
        self.eb_button_image = ImageTk.PhotoImage(image)
        return None


    def ec_movement(self, *image_tags):
        banner_frame = self.back_banner_canvas.find_withtag("banner_frame")[0]
        self.back_banner_canvas.itemconfig(banner_frame, 
            height=(int(self.back_banner_canvas.itemcget(banner_frame, 
                                                         "height")) + 
            (self.in_banner_displacement/5)))
        for tag in image_tags:
            self.edit_banner_canvas.move(tag, 0, self.in_banner_displacement)
        return None


    def sb_rotation(self):
        image = \
            Image.open(\
                "resources\\chevdown.png").resize(\
                    (20, 20)).rotate(self.chev_angle)
        self.sb_button_image = ImageTk.PhotoImage(image)
        return None


    def sc_movement(self, *image_tags):
        banner_frame = self.back_banner_canvas.find_withtag("banner_frame")[0]
        self.back_banner_canvas.itemconfig(banner_frame, 
            height=(int(self.back_banner_canvas.itemcget(banner_frame, 
                                                         "height")) + 
            (self.in_banner_displacement/5)))
        for tag in image_tags:
            self.style_banner_canvas.move(tag, 0, self.in_banner_displacement)
        return None
        


    def file_banner_display(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 0
        self.file_banner_canvas.pack(anchor="n",
                                     side="top",
                                     in_=self.banner_frame)
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.file_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.forced_banner_expansion()
        for n in range(18):
            self.chev_angle += 10
            self.root.after(1, self.fb_rotation())
            self.file_banner_button.config(image=self.fb_button_image, 
                                           command=self.file_banner_hide)
            self.root.update()
        for i in range(0, 57, 2):
            self.in_banner_displacement = 10
            if i <= 47:
                self.root.after(1, self.fc_movement("exit"))
                new_height = int(self.file_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.file_banner_canvas.config(height=new_height)
                self.root.update()
            if i >= 3 and i <= 48:
                self.root.after(1, self.fc_movement("home"))
                self.root.update()
            if i >= 7 and i <= 50:
                self.root.after(1, self.fc_movement("lock"))
                self.root.update()
            if i >= 12 and i <= 53:
                self.root.after(1, self.fc_movement("save"))
                self.root.update()
            if i >= 18:
                self.root.after(1, self.fc_movement("open"))
                self.root.update()
        self.root.update_idletasks()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        return None


    def file_banner_hide(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 180
        for n in range(18):
            self.chev_angle -= 10
            self.root.after(1, self.fb_rotation())
            self.file_banner_button.config(image=self.fb_button_image, 
                                           command=self.file_banner_display)
            self.root.update()
        for i in range(0, 65, 2):
            self.in_banner_displacement = -10
            if i <= 39:
                self.root.after(1, self.fc_movement("open"))
                self.root.update_idletasks()
            if i >= 3 and i <= 44:
                self.root.after(1, self.fc_movement("save"))
                self.root.update_idletasks()
            if i >= 7 and i <= 50:
                self.root.after(1, self.fc_movement("lock"))
                self.root.update_idletasks()
            if i >= 12 and i <= 57:
                self.root.after(1, self.fc_movement("home"))
                self.root.update_idletasks()
            if i >= 18:
                self.root.after(1, self.fc_movement("exit"))
                new_height = int(self.file_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.file_banner_canvas.config(height=new_height)
                self.root.update_idletasks()
            self.root.update()
        self.file_banner_canvas.pack_forget()
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.file_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        self.banner_collapse()
        return None


    def edit_banner_display(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 0
        self.edit_banner_canvas.pack(anchor="n",
                                     side="top",
                                     in_=self.banner_frame)
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.edit_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.forced_banner_expansion()
        for n in range(18):
            self.chev_angle += 10    
            self.root.after(1, self.eb_rotation())
            self.edit_banner_button.config(image=self.eb_button_image, 
                                           command=self.edit_banner_hide)
            self.root.update()
        for i in range(0, 75, 2):
            self.in_banner_displacement = 10
            if i <= 59:
                self.root.after(1, self.ec_movement("wb"))
                new_height = int(self.edit_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.edit_banner_canvas.config(height=new_height)
                self.root.update()
            if i >= 3 and i <= 60:
                self.root.after(1, self.ec_movement("paste"))
                self.root.update()
            if i >= 7 and i <= 62:
                self.root.after(1, self.ec_movement("copy"))
                self.root.update()
            if i >= 12 and i <= 65:
                self.root.after(1, self.ec_movement("cut"))
                self.root.update()
            if i >= 18 and i <= 68:
                self.root.after(1, self.ec_movement("undo"))
                self.root.update()
            if i >= 25:
                self.root.after(1, self.ec_movement("highlight"))
                self.root.update()
        self.root.update_idletasks()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        return None


    def edit_banner_hide(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 180
        for n in range(18):
            self.chev_angle -= 10
            self.root.after(1, self.eb_rotation())
            self.edit_banner_button.config(image=self.eb_button_image, 
                                           command=self.edit_banner_display)
            self.root.update()
        for i in range(0, 85, 2):
            self.in_banner_displacement = -10
            if i <= 49:
                self.root.after(1, self.ec_movement("highlight"))
                self.root.update_idletasks()
            if i >= 3 and i <= 54:
                self.root.after(1, self.ec_movement("undo"))
                self.root.update_idletasks()
            if i >= 7 and i <= 60:
                self.root.after(1, self.ec_movement("cut"))
                self.root.update_idletasks()
            if i >= 12 and i <= 67:
                self.root.after(1, self.ec_movement("copy"))
                self.root.update_idletasks()
            if i >= 18 and i <= 75:
                self.root.after(1, self.ec_movement("paste"))
                self.root.update_idletasks()
            if i >= 25:
                self.root.after(1, self.ec_movement("wb"))
                new_height = int(self.edit_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.edit_banner_canvas.config(height=new_height)
                self.root.update_idletasks()
            self.root.update()
        self.edit_banner_canvas.pack_forget()
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.edit_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        self.banner_collapse()
        return None


    def style_banner_display(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 0
        self.style_banner_canvas.pack(anchor="n",
                                     side="top",
                                     in_=self.banner_frame)
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.style_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.forced_banner_expansion()
        for n in range(18):
            self.chev_angle += 10
            self.root.after(1, self.sb_rotation())
            self.style_banner_button.config(image=self.sb_button_image, 
                                           command=self.style_banner_hide)
            self.root.update()
        for i in range(0, 57, 2):
            self.in_banner_displacement = 10
            if i <= 47:
                self.root.after(1, self.sc_movement("text_colour"))
                new_height = int(self.style_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.style_banner_canvas.config(height=new_height)
                self.root.update()
            if i >= 3 and i <= 48:
                self.root.after(1, self.sc_movement("strikethrough"))
                self.root.update()
            if i >= 7 and i <= 50:
                self.root.after(1, self.sc_movement("underline"))
                self.root.update()
            if i >= 12 and i <= 53:
                self.root.after(1, self.sc_movement("italic"))
                self.root.update()
            if i >= 18:
                self.root.after(1, self.sc_movement("bold"))
                self.root.update()
        self.root.update_idletasks()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        pass


    def style_banner_hide(self):
        if self.window_mode == "windowed":
            self.text_entry.focus_set()
        elif self.window_mode == "tabbed":
            swelf.get_active_tab()[1].focus_set()
        self.chev_angle = 180
        for n in range(18):
            self.chev_angle -= 10
            self.root.after(1, self.sb_rotation())
            self.style_banner_button.config(image=self.sb_button_image, 
                                           command=self.style_banner_display)
            self.root.update()
        for i in range(0, 65, 2):
            self.in_banner_displacement = -10
            if i <= 39:
                self.root.after(1, self.sc_movement("bold"))
                new_height = int(self.style_banner_canvas.cget("height")) + \
                    self.in_banner_displacement
                self.style_banner_canvas.config(height=new_height)
                self.root.update()
            if i >= 3 and i <= 44:
                self.root.after(1, self.sc_movement("italic"))
                self.root.update()
            if i >= 7 and i <= 50:
                self.root.after(1, self.sc_movement("underline"))
                self.root.update()
            if i >= 12 and i <= 57:
                self.root.after(1, self.sc_movement("strikethrough"))
                self.root.update()
            if i >= 18:
                self.root.after(1, self.sc_movement("text_colour"))
                self.root.update()
        # TODO: Add specific banner item movements
        self.style_banner_canvas.pack_forget()
        self._update_repack_queue()
        for child in self.banner_frame_children[\
                self.banner_frame_children.index(self.style_banner_canvas)::]:
            if child.winfo_ismapped():
                self.repack_queue[child][0] = True
                child.pack_forget()
            else:
                continue
        self._repack()
        self.back_banner_canvas.config(scrollregion=
                                       self.back_banner_canvas.bbox("all"))
        self.banner_collapse()
        pass
        
    def switch_window_mode(self, mode, event=None):
        if mode == "tabbed":
            if self.window_mode == "windowed":
                self.window_mode = "tabbed"
                self.tab_set = {}
                untitled_tab_count = 0
                global count
                count = 0
                for key, window in self.window_set.items():
                    print("window: ", key, window.text_frame)
                for key, window in self.window_set.items():
                    if self.tab_set:
                        self.previous_tab = self.get_active_tab()
                    text = window.text_entry.get(1.0, "end")
                    tags_to_push = {}
                    for tag in window.text_entry.tag_names():
                        tags_to_push[tag] = [window.text_entry.tag_ranges(tag),
                                             window.text_entry.tag_config(tag)]
                    if window.file_name is not "":
                        tab_name = window.file_name
                        print(window.file_name, untitled_tab_count)
                    else:
                        if untitled_tab_count == 0:
                            tab_name = "Untitled"
                        else:
                            tab_name = "Untitled(" + str(untitled_tab_count) + ")"
                        print(window.file_name, untitled_tab_count)
                        untitled_tab_count += 1
                    new_tab = self.create_tab(text, 
                                              tags_to_push, 
                                              tab_name, 
                                              window
                                              )
                    self.tab_set[new_tab[12]] = new_tab
                    for key, value in self.tab_set.items():
                        print(key, self.tab_set[key][3])
                    for tab, widgets in self.tab_set.items():
                        self.tab_set[tab][3].config(relief="raised")
                    new_tab[3].config(relief="sunken")
                    self._repack()
                    new_tab[1].focus_force()
                self.switch_menus_to_tab_mode()
                self.active_text_frame.bind("<Control-KeyPress-n>", 
                                            self.create_new_tab)
                for key, window in self.window_set.copy().items():
                    try:
                        del self.window_set[window.count]
                    except KeyError:
                        pass
                self.window_set = {}
                return None
            else:
                return None
        elif mode == "windowed":
            if self.window_mode == "tabbed":
                self.window_mode = "windowed"
                self.window_set = {}
                count = 1
                print(len(list(self.tab_set.keys())))
                for key, tab in self.tab_set.items():
                    if tab[12] == self.count:
                        self.window_set[0] = self
                        self.active_text_frame = self.text_frame
                        print("tab to window")
                        continue
                    else:
                        tab[4] = tab[1].get("1.0", "end")
                        tags_to_push = {}
                        for tag in tab[1].tag_names():
                            tags_to_push[tag] = [tab[1].tag_ranges(tag),
                                                 tab[1].tag_config(tag)]
                        new_window = WN(self.username,
                                        file_contents=tab[4],
                                        saved=tab[7],
                                        file_name=tab[8],
                                        window_set=self.window_set,
                                        pushed_tags=tags_to_push,
                                        custom_fonts=tab[9],
                                        master = self.master)
                        new_window.new_window_pos = tab[14]
                        new_window.view_change(tab[10])
                        print("tab to window")
                for key, tab in self.tab_set.copy().items():
                    if tab[12] == self.count:
                        for widget in tab[:4]:
                            widget.pack_forget()
                            widget.destroy()
                        continue
                    else:
                        self.tab_to_window_cleanup(self.tab_set[key])
                self.tab_set = {}
                if self.tab_labels_frame.winfo_ismapped():
                    self.tab_labels_frame.pack_forget()
                self.switch_menus_to_window_mode()
                self._repack()
                self.active_text_frame.bind("<Control-KeyPress-n>", self.new)
                self.windowed_text_entry_keybinds(self.text_entry)
                return None
            else:
                return None

    def create_tab(self, text, pushed_tags, tab_name, window):
        global count
        if not self.active_text_frame:
            self.active_text_frame = self.text_frame
        self.active_text_frame.pack_forget()
        if not self.tab_labels_frame.winfo_ismapped():
            self.tab_labels_frame.pack(side="top", fill="x")
        new_tab = [None, None, None, None]
        new_tab[0] = tk.Frame(self.root, relief="sunken")
        new_tab[1] = tk.Text(new_tab[0], 
                             font=self.custom_font, 
                             wrap="word",
                             undo="True",
                             maxundo="5", 
                             height="20", 
                             width="40")
        new_tab[1].insert("end", text)
        new_tab[1].tag_add("custom_font", 1.0, "end")
        new_tab[1].tag_config("custom_font", font=self.custom_font)
        new_tab[2] = tk.Scrollbar(self.root)
        new_tab[1].config(yscrollcommand=new_tab[2].set)
        new_tab[2].config(command=new_tab[1].yview)
        new_tab[3] = tk.Label(self.root, text=tab_name, relief="sunken")
        new_tab[0].pack(anchor="n", side="top", fill="both", expand="1")
        new_tab[3].pack(side="left", in_=self.tab_labels_frame)
        new_tab[2].pack(side="right", fill="y", in_=new_tab[0])
        new_tab[1].pack(fill="both", expand="1", in_=new_tab[0])
        self.active_text_frame = new_tab[0]
        new_tab[1].tag_add("left", "1.0", "end")
        new_tab.append(text) # tab[4]
        new_tab.append(window.checksum_text) # tab[5]
        new_tab.append(window.checksum) # tab[6]
        new_tab.append(window.saved) # tab[7]
        new_tab.append(tab_name) # tab[8]
        new_tab.append(window.custom_fonts_dict) # tab[9]
        new_tab.append(window.text_colour_tags) # tab[10]
        new_tab.append(window.non_font_tags) # tab[11]
        new_tab.append(count) # tab[12]
        new_tab.append(window.view_mode) # tab[13]
        new_tab.append(window.root.geometry()) # tab[14]
        self.active_text_frame.pack_forget()
        self.root.update()
        count += 1
        for font in window.custom_fonts_dict:
            if font is "custom_font":
                continue
            for font_range in range(0, len(pushed_tags[font][0]), 2):
                new_tab[1].tag_add(font, 
                                    pushed_tags[font][0][font_range],
                                    pushed_tags[font][0][font_range+1])
                new_tab[1].tag_config(font,
                                      font=window.custom_fonts_dict[font])
        for colour in window.text_colour_tags:
            for c_range in range(0, len(pushed_tags[colour][0]), 2):
                new_tab[1].tag_add(colour,
                                   pushed_tags[colour][0][c_range],
                                   pushed_tags[colour][0][c_range+1])
                new_tab[1].tag_config(colour, foreground=colour)
        for tag in pushed_tags:
            if tag is "sel":
                continue
            elif tag in ["left", "center", "right"]:
                for just in range(0, len(pushed_tags[tag][0]), 2):
                    new_tab[1].tag_add(tag,
                                       pushed_tags[tag][0][just],
                                       pushed_tags[tag][0][just+1])
                    new_tab[1].tag_config(tag, justify=tag)
                    self.non_font_tags[tag] = new_tab[1].tag_ranges(tag)
            elif tag in ["yellow", "green", "orange", "pink"]:
                for hl in range(0, len(pushed_tags[tag][0]), 2):
                    new_tab[1].tag_add(tag,
                                       pushed_tags[tag][0][hl],
                                       pushed_tags[tag][0][hl+1])
                    new_tab[1].tag_config(tag, background=tag)
                    self.non_font_tags[tag] = new_tab[1].tag_ranges(tag)
            elif tag in ["superscript", "subscript"]:
                for offset in range(0, len(pushed_tags[tag][0]), 2):
                    new_tab[1].tag_add(tag,
                                       pushed_tags[tag][0][offset],
                                       pushed_tags[tag][0][offset+1])
                    new_tab[1].tag_config(tag,
                                    offset=pushed_tags[tag][1]["offset"])
                    self.non_font_tags[tag] = new_tab[1].tag_ranges(tag)
        if window is not self:
            window.root.destroy()
        new_tab[1].bind("<Enter>", self.update_geometry)
        new_tab[3].bind("<1>", self.change_tab)
        new_tab[3].bind("<3>", self.close_tab)
        new_tab[1].bind("<Control-KeyPress-4>", 
                       lambda e:self.fix_text(text_entry=new_tab[1]))
        return new_tab


    def create_new_tab(self, event=None):
        if not self.active_text_frame:
            self.active_text_frame = self.text_frame
        self.previous_tab = self.get_active_tab()
        self.active_text_frame.pack_forget()
        if not self.tab_labels_frame.winfo_ismapped():
            self.tab_labels_frame.pack(side="top", fill="x")
        new_tab = [None, None, None, None]
        new_tab[0] = tk.Frame(self.root, relief="sunken")
        new_tab[1] = tk.Text(new_tab[0], 
                             font=self.custom_font, 
                             wrap="word",
                             undo="True",
                             maxundo="5", 
                             height="20", 
                             width="40")
        new_tab[1].tag_add("custom_font", 1.0, "end")
        new_tab[1].tag_config("custom_font", font=self.custom_font)
        new_tab[2] = tk.Scrollbar(self.root)
        new_tab[1].config(yscrollcommand=new_tab[2].set)
        new_tab[2].config(command=new_tab[1].yview)
        new_tab[3] = tk.Label(self.root, text="Untitled", relief="sunken")
        new_tab[0].pack(anchor="n", side="top", fill="both", expand="1")
        new_tab[3].pack(side="left", in_=self.tab_labels_frame)
        new_tab[2].pack(side="right", fill="y", in_=new_tab[0])
        new_tab[1].pack(fill="both", expand="1", in_=new_tab[0])
        self.active_text_frame = new_tab[0]
        new_tab[1].tag_add("left", "1.0", "end")
        new_tab.append("") # tab[4]
        new_tab.append("") # tab[5]
        new_tab[5] = new_tab[5].encode("utf-8")
        new_tab.append("") # tab[6]
        new_tab.append(True) # tab[7]
        new_tab.append("Untitled") # tab[8]
        new_tab.append({}) # tab[9]
        new_tab.append({}) # tab[10]
        new_tab.append({}) # tab[11]
        global count
        new_tab.append(count) # tab[12]
        new_tab.append("standard") # tab[13]
        new_tab.append("+".join(["401x451", 
                                 str(int(self.screen_x / 2) - 200), 
                                 str(int(self.screen_y / 2) - 225)
                                ])
                       ) # tab[14]
        self._repack()
        self.tabbed_text_entry_keybinds(new_tab)
        new_tab[3].bind("<1>", self.change_tab)
        new_tab[3].bind("<3>", self.close_tab)
        new_tab[1].focus_force()
        self.root.update()
        self.tab_set[count] = new_tab
        print(count, self.tab_set[count])
        for key, tab in self.tab_set.items():
            if key == count:
                continue
            else:
                tab[3].config(relief="raised")
        count += 1
        return new_tab


    def switch_menus_to_tab_mode(self):
     # might have to pass active_text_frame as the argument to all tab methods
     #   text_entry = new_tab[0].winfo_children()[0]
        self.file_menu.entryconfigure(0, 
                                      label="New Tab", 
                                      accelerator="Ctrl+N",
                                      command=self.create_new_tab
                                      )
        self.file_menu.entryconfigure(1,
                                      command=self.open_file_tab)
        self.file_menu.entryconfigure(2,
                                      label="Open in new tab",
                                      command=self.open_new_tab)
        self.file_menu.entryconfigure(3,
                                      label="Duplicate tab",
                                      command=self.duplicate_tab)
        self.file_menu.entryconfigure(5,
                                      command=self.save_file_tab)
        self.file_menu.entryconfigure(6,
                                      command=self.save_file_as_tab)
        self.file_menu.entryconfigure(9,
                                      label="Lock window",
                                      command=self.lock_tab_mode)
        self.file_menu.entryconfigure(12,
                                      command=lambda:self.close_tab(
                tab=self.get_active_tab()))
        self.file_menu.entryconfigure(13,
                                      command=self.close_other_tabs)
        self.edit_menu.entryconfigure(0,
                                      command=self.undo_tab)
        self.edit_menu.entryconfigure(1,
                                      command=self.redo_tab)
        self.edit_menu.entryconfigure(2,
                                      command=self.reset_tab)
        self.edit_menu.entryconfigure(3,
                                      command=self.select_all_tab)
        self.edit_menu.entryconfigure(4,
                                      command=self.highlight_tab)
        self.edit_menu.entryconfigure(5,
                                      command=self.remove_highlight_tab)
        self.edit_menu.entryconfigure(7,
                                      command=self.copy_tab)
        self.edit_menu.entryconfigure(8,
                                      command=self.cut_tab)
        self.edit_menu.entryconfigure(9,
                                      command=self.paste_tab)
        self.edit_menu.entryconfigure(12,
                                      command=lambda:self.fix_text_tab(
                self.active_text_frame.winfo_children()[0]))
        self.whiteboard.entryconfigure(0,
                                       command=self.add_to_whiteboard_tab)
        return None


    def switch_menus_to_window_mode(self):
        # placeholder - currently not required as new instances
        # are created instead of actually converting tabs to 
        # windows
        self.file_menu.entryconfigure(0,
                                      label="New Window", 
                                      accelerator="Ctrl+N", 
                                      command=self.new)
        self.file_menu.entryconfigure(1,
                                      command=self.open_file)
        self.file_menu.entryconfigure(2,
                                      label="Open in new window",
                                      command=self.open_new)
        self.file_menu.entryconfigure(3,
                                      label="Duplicate",
                                      command=self.duplicate)
        self.file_menu.entryconfigure(5,
                                      command=self.save_file)
        self.file_menu.entryconfigure(6,
                                      command=self.save_file_as)
        self.file_menu.entryconfigure(9,
                                      label="Lock window",
                                      command=self.lock)
        self.file_menu.entryconfigure(12, command=lambda:self.close)
        self.file_menu.entryconfigure(13,
                                      command=self.close_others)
        self.edit_menu.entryconfigure(0,
                                      command=self.undo)
        self.edit_menu.entryconfigure(1,
                                      command=self.redo)
        self.edit_menu.entryconfigure(2,
                                      command=self.reset)
        self.edit_menu.entryconfigure(3,
                                      command=self.select_all)
        self.edit_menu.entryconfigure(4,
                                      command=self.highlight)
        self.edit_menu.entryconfigure(5,
                                      command=self.remove_highlight)
        self.edit_menu.entryconfigure(7,
                                      command=self.copy)
        self.edit_menu.entryconfigure(8,
                                      command=self.cut)
        self.edit_menu.entryconfigure(9,
                                      command=self.paste)
        self.edit_menu.entryconfigure(12,
                                      command=lambda:self.fix_text(
                self.active_text_frame.winfo_children()[0]))
        self.whiteboard.entryconfigure(0,
                                       command=self.add_to_whiteboard)
        return None

        
    def change_tab(self, event=None):
        print(event.widget)
        for key, value in self.tab_set.items():
            print(key, self.tab_set[key][3])
            if event.widget in self.tab_set[key]:
                selected_tab = self.tab_set[key]
            else:
                try:
                    self.tab_set[key][3].config(relief="raised")
                except tk.TclError: # closed tab not garbage-collected
                    continue
            if self.active_text_frame in self.tab_set[key]:
                self.previous_tab = self.tab_set[key]
        event.widget.config(relief="sunken")
        self.active_text_frame = selected_tab[0]
        self._repack()
        self.tabbed_text_entry_keybinds(selected_tab)
        selected_tab[1].focus_force()
        return None


    def select_previous_tab(self):
        old_tab = self.get_active_tab()
        if old_tab is None:
            old_tab = self.tab_set[min(self.tab_set.keys())]
        try:
            self.previous_tab[3].config(relief="sunken")
            
        except AttributeError as e:
            self.previous_tab = None
            return None
        else:
            self.active_text_frame = self.previous_tab[0]
            new_tab = self.previous_tab
            self.previous_tab = old_tab
            for key, tab in self.tab_set.items():
                if self.tab_set[key][0] is self.active_text_frame:
                    continue
                else:
                    self.tab_set[key][3].config(relief="raised")
            self._repack()
            self.tabbed_text_entry_keybinds(new_tab)
            new_tab[1].focus_force()
            return None


    def get_active_tab(self, event=None):
        for key, tab in self.tab_set.items():
            if self.active_text_frame in self.tab_set[key]:
                return self.tab_set[key]
            else:
                continue
        return None
                
        
    def close_tab(self, event=None, tab=None):
        invalid_previous_tab = False
        if tab is not None:
            tab_to_close = tab
        else:
            for key, value in self.tab_set.items():
                if event.widget in self.tab_set[key]:
                    tab_to_close = self.tab_set[key]
        self.select_previous_tab()
        if self.previous_tab is None:
            self.master.root.deiconify()
            self.root.destroy()
            return None
        else:
            if self.previous_tab == tab_to_close:
                invalid_previous_tab = True
            if self._validate_tab(tab_to_close):
                for widget in tab_to_close[:4]:
                    widget.pack_forget()
                    widget.destroy()
                del self.tab_set[tab_to_close[12]]
            else:
                if tkmb.askyesno("Warning", 
                                 "If you continue, changes to the current "
                                 "file will be lost.  Would you like to "
                                 "save changes before continuing?", 
                                 icon="warning"):
                    self.save_file_tab(tab_to_close)
                for widget in tab_to_close[:4]:
                    widget.pack_forget()
                    widget.destroy()
                try:
                    del self.tab_set[tab_to_close[12]]
                except KeyError:
                    pass
            if invalid_previous_tab:
                try:
                    self.previous_tab = self.tab_set[min(self.tab_set.keys())]
                except ValueError: # empty set for min() call
                    pass
            if self.tab_set == {}:
                self.root.destroy()
                self.master.root.deiconify()
                return None
            else:
                return None    


    def close_other_tabs(self, event=None):
        tab_to_keep = self.get_active_tab()
        for key, tab in self.tab_set.copy().items():
            if tab is not tab_to_keep:
                self.close_tab(tab=tab)
        return None
            
            
    def tab_to_window_cleanup(self, tab, event=None):
        for widget in tab[:4]:
            widget.pack_forget()
            widget.destroy()
        try:
            del self.tab_set[tab[12]]
        except KeyError:
            pass
        return None


    def super_sound(self):
        winsound.PlaySound(
            os.path.dirname(__file__)+r"\resources\explosia.wav",
            winsound.SND_FILENAME)
        return None


#############################################################################            
##                DEBUG function, used for various testing.                ##    
#############################################################################
    def test(self, event=None):
        print(event.widget)
        pass



if __name__ == "__main__":
    platform = jt.JTLauncher()