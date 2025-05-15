import tkinter as tk
from tkinter import ttk

def create_slider(parent, label_text, min_val, max_val, default_val, row, col_offset):
    """Create a slider with a label showing its current value"""
    ttk.Label(parent, text=label_text).grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")
    var = tk.IntVar(value=default_val)
    slider = ttk.Scale(parent, from_=min_val, to=max_val, variable=var, orient="horizontal", length=200)
    slider.grid(row=row, column=col_offset+1, padx=5, pady=5)
    
    # Add a label to show the current value
    value_label = ttk.Label(parent, text=str(default_val))
    value_label.grid(row=row, column=col_offset+1, padx=(210, 0), pady=5, sticky="w")
    
    # Update the label when the slider changes
    def update_label(event):
        value_label.config(text=str(int(slider.get())))
    
    slider.bind("<Motion>", update_label)
    slider.bind("<ButtonRelease-1>", update_label)
    
    return var

def setup_treeview(parent, columns, headings, column_widths=None):
    """Create and configure a treeview widget"""
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    
    for i, col in enumerate(columns):
        tree.heading(col, text=headings[i])
        if column_widths and i < len(column_widths):
            tree.column(col, width=column_widths[i])
    
    tree.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    return tree