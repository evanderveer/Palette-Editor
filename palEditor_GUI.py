from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser 
from tkinter import filedialog
from tkinter import messagebox

import palEditor
import os


class App(Tk):

    def __init__(self):
        super().__init__()
        from palEditorElements import Elements
        
        self.geometry('300x250')
        self.title("Palette generator")
        self.resizable(False,False)
        
        element_options = {'padx': 5, 'pady':5, 'sticky': 'W'}
        frame_options = {'padx': 10, 'pady': 5}
        self.elements = Elements(self, element_options, frame_options)
        
        style = ttk.Style(self)
        #style.configure('TButton', foreground='red')
    
    def change_color_button(self, button, color):
        button.config(bg=color.get())
    
    def change_color(self, color):
        new_color = colorchooser.askcolor(title='Pick a color')[1]
        if(new_color != None):
            color.set(new_color)
            
    def generate(self):
    
        #Construct the color points list
        color_list = ((0, self.elements.start_color.get()), (1, self.elements.end_color.get()))
        
        try:
            palEditor.mainfunction(palette_file=self.elements.file_name.get(), gradient_steps=self.elements.steps.get(), color_list=color_list)
            self.elements.file_gen_label.config(text='Palette generated')
        except FileNotFoundError as error:
            messagebox.showerror('No file selected', 'Please select a file.')
        
    def get_file_name(self, file_name):
        new_file_name = filedialog.asksaveasfilename(title = "Select file",filetypes = [("palette files","*.pal")])
        if(new_file_name == ""):
            return
        file_name.set(new_file_name)
        if(file_name.get()[-4:] != '.pal'):
            file_name.set(file_name.get() + '.pal')
       
        self.elements.file_name_label.config(text=file_name.get())

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
   