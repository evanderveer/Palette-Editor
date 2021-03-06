from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser 
from tkinter import filedialog
from tkinter import messagebox

class Elements():
    def __init__(self, root, element_options, frame_options):
        self.frame = ttk.Frame(root)
        self.frame.grid(**frame_options)

        

        self.end_color = StringVar(value='#FFFFFF', name='end_color')
        self.start_color = StringVar(value='#FFFFFF', name='start_color')
        self.file_name = StringVar(name='file_name')
        self.steps = IntVar(value=256, name='steps')
        
        menubar = Menu(root)
        menubar.add_command(label='File')
        menubar.add_command(label='About')
        menubar.add_command(label='Quit', command=root.destroy)
        root.config(menu=menubar)
        
        start_label = ttk.Label(self.frame, text='Starting color: ')
        start_label.grid(column=0,row=0, **element_options)

        self.start_button = Button(self.frame, text="", command=lambda: root.change_color(self.start_color), width=2)
        self.start_button.grid(column=1,row=0, **element_options)

        self.end_label = ttk.Label(self.frame, text='Final color: ')
        self.end_label.grid(column=0,row=1, **element_options)

        self.end_button = Button(self.frame, text="", command=lambda: root.change_color(self.end_color), width=2)
        self.end_button.grid(column=1,row=1, **element_options)

        self.start_button.config(bg=self.start_color.get())
        self.start_color.trace('w', lambda *args: root.change_color_button(self.start_button, self.start_color))

        self.end_button.config(bg=self.end_color.get())
        self.end_color.trace('w', lambda *args: root.change_color_button(self.end_button, self.end_color))

        self.file_label = ttk.Label(self.frame, text='File name: ')
        self.file_label.grid(column=0,row=2, **element_options)

        self.file_name_button = ttk.Button(self.frame, text='Save as', command=lambda: root.get_file_name(self.file_name))
        self.file_name_button.grid(column=1,row=2, **element_options)

        self.steps_label = ttk.Label(self.frame, text='Number of steps: ')
        self.steps_label.grid(column=0,row=3, **element_options)

        self.steps_entry = ttk.Entry(self.frame, textvariable=self.steps)
        self.steps_entry.grid(column=1,row=3, **element_options)

        self.generate_button = ttk.Button(self.frame, text="Generate", command=root.generate)
        self.generate_button.grid(column=0,row=4, **element_options)

        self.file_name_label = ttk.Label(self.frame, text='Select a file')
        self.file_name_label.grid(column=0, columnspan=2,row=5, **element_options)
        
        self.file_gen_label = ttk.Label(self.frame, text='')
        self.file_gen_label.grid(column=0, columnspan=2,row=6, **element_options)