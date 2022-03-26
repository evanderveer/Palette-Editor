from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser 
from tkinter import filedialog
from tkinter import messagebox
from argparse import Namespace

import palEditor
import os


class App(Tk):

    def __init__(self):
        super().__init__()
        from palEditorElements import Elements
        
        self.geometry('300x250')
        self.title("Palette generator")
        self.resizable(False,False)
        
        grid_options = {'padx': 5, 'pady':5, 'sticky': 'W'}
        self.elements = Elements(self, grid_options)
        
        style = ttk.Style(self)
        print(style.theme_names())
        #style.configure('TButton', foreground='red')
    
    def change_color_button(self, button, color):
        button.config(bg=color.get())
    
    def change_color(self, color):
        new_color = colorchooser.askcolor(title='Pick a color')[1]
        if(new_color != None):
            color.set(new_color)
            
    def generate(self):
        command_string = Namespace(palette_name=self.elements.file_name.get(), start_color=self.elements.start_color.get(), end_color=self.elements.end_color.get(), gradient_steps=self.elements.steps.get(), color_points=None, interpolation_function='linear', color_space='lab')
        try:
            palEditor.mainfunction(command_string)
        except FileNotFoundError as error:
            messagebox.showerror('No file selected', 'Please select a file.')
        
    def get_file_name(self, file_name):
        new_file_name = filedialog.asksaveasfilename(title = "Select file",filetypes = [("palette files","*.pal")])
        if(new_file_name == ""):
            return
        file_name.set(new_file_name)
        print(file_name.get())
        if(file_name.get()[-4:] != '.pal'):
            file_name.set(file_name.get() + '.pal')
        print(file_name.get())
       
        self.elements.file_name_label.config(text=file_name.get())

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
   