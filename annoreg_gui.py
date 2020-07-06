#!/usr/bin/python

from annoreg import *
import tkinter as tk
from tkinter import filedialog

def get_output():
    global output
    global root
    root.withdraw()
    output = filedialog.asksaveasfilename(parent=root, filetypes=(('tsv file','*.txt'),('all files','*.*')),
                                          defaultextension='.txt')
    root.destroy()

# Create tkinter window
root = tk.Tk()
root.title('export settings')
root.resizable(width=False, height=False)

frame = tk.Frame(root, padx=5, pady=5)
frame.pack()

# prepare parameters
sort = tk.BooleanVar()
substract = tk.IntVar()

tk.Checkbutton(frame, text='sort index entries', var=sort, onvalue=True,
               offvalue=False).pack(anchor='nw')
spbox = tk.Frame(frame)
spbox.pack()
tk.Label(spbox, text='title pages: ').pack(side=tk.LEFT)
tk.Spinbox(spbox, from_=0, to=255, width=5,
           textvariable=substract).pack(side=tk.LEFT)
tk.Button(frame, text='Export', command=get_output).pack()

# Hide root window while file selection is in progress
root.withdraw()

# choose pdf document
doc = filedialog.askopenfilename(parent=root,
                                 filetypes=(('pdf document','*.pdf'),
                                            ('all files','*.*')),
                                 defaultextension='.pdf')

# show root window, select other stuff
root.deiconify()

root.mainloop()

# export
export_tsv(process_annotations(get_annotations(doc, substract.get()),
                               sort.get()), output)
