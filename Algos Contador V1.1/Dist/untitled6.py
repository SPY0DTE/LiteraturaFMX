# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:16:32 2024

@author: FVFENTANES
"""

import tkinter as tk

# Sample list of items
items = [f"Item {i}" for i in range(1, 101)]  # A list with 100 items

# Create the main window
root = tk.Tk()
root.title("List with Scrollbar")

# Create a frame to hold the Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a Listbox
listbox = tk.Listbox(frame, width=50, height=20)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Insert items into the Listbox
for item in items:
    listbox.insert(tk.END, item)

# Create a Scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the Listbox and Scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Run the Tkinter event loop
root.mainloop()